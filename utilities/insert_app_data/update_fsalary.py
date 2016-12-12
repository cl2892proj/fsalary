from private_settings import *
import sqlalchemy
import pandas as pd
import numpy as np
import unittest
import pdb
import glob
import re
import logging
import datetime
import pytz
import os
import geocoder

#LOGGING SETUP
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('fsalary_update.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_conn_str(FILING):
    """
    GIVEN FILING TYPE, RETURN THE CONNECTION STRING
    """

    if FILING == 'H1B':
        return FRANKSALARY_INSERT_CONNSTR_H1B
    elif FILING == 'H2A':
        return FRANKSALARY_INSERT_CONNSTR_H2A
    elif FILING == 'H2B':
        return FRANKSALARY_INSERT_CONNSTR_H2B
    elif FILING == 'PERM':
        return FRANKSALARY_INSERT_CONNSTR_PERM
    elif FILING == 'PW':
        return FRANKSALARY_INSERT_CONNSTR_PW
    else:
        print 'INCORRECT ARGUMENT'
        return 0

def update_raw_indv(FILING, YEAR, ID=1):
    """
    GIVEN FILING TYPE, THE YEAR OF THE FILING, AND THE ID OF THE FILING IF MORE THAN 1
    INSERT/UPDATE THE FILE TO THE INDIVIDUAL TABLE IN THE RAW DATABASE
    RETURN 1 IF THERE'S any update, RETURN 0 IF THERE'S NO Update
    """

    EXCEL_PATH= glob.glob('excel/{0}/*{1}*'.format(FILING,YEAR))[-1]
    YR = 2000 + YEAR
    print EXCEL_PATH

    INDIV_DB_CONNSTR= get_conn_str(FILING)
    if INDIV_DB_CONNSTR== 0: 
        return 0

    engine = sqlalchemy.create_engine(INDIV_DB_CONNSTR)
    conn = engine.connect()

    df = pd.read_excel(EXCEL_PATH)
    df.columns=[x.lower().replace(' ','_') for x in df.columns]

    #types
    dt = {}
    for index, row in df.dtypes.reset_index().iterrows():
        k = row['index']
        v = row[0]

        if v in (np.dtype('<M8[ns]'),):
            v = sqlalchemy.types.Date
        elif v in (np.dtype('float64'),):
            v = sqlalchemy.types.Float()
        elif v in (np.dtype('O'),):
            df[k] = df[k].str.strip()
            searchObj = re.search(r'(\b|[^a-z])date(\b|[^a-z])',k,re.M|re.I)
            #searchObj = re.search(r'(\b|[^a-z])(date|start|end)(\b|[^a-z])',k,re.M|re.I)
            if searchObj:
                #print k
                df[k] = pd.to_datetime(df[k], errors='coerce')
                v = sqlalchemy.types.Date
            else:
                v = sqlalchemy.types.Text()
        elif v in (np.dtype('int64'),):
            v = sqlalchemy.types.Integer
        else:
            pass

        dt[k] = v

    df = df.replace({r'(\b|[^a-z])N/A(\b|[^a-z])':''}, regex=True)
    df = df.replace({'\t':' '}, regex=True)
    df = df.replace({'\r':' '}, regex=True)
    df = df.replace({'\n':' '}, regex=True)
    df = df.replace({'\\\\':' '}, regex=True)
    df = df.replace({'\$':''}, regex=True)
    df = df.replace({'^#+$':''}, regex=True)

    if ID != 1:
        TABLE_NAME = 'yr{0}_{1}'.format(YR, ID)
    else:
        TABLE_NAME = 'yr{0}'.format(YR)

    
    # ONLY INSERT IF THE RECORD COUNTS IN THE DATAFRAME IS DIFFERENT FROM THE DATABASE
    count_df = df.shape[0]
    
    try:
        sql = 'select count(*) from {0}'.format(TABLE_NAME)
        count_db = pd.read_sql(sql,con=engine).iat[0,0]
    except:
        #if table doesn't exist
        count_db = 0

    #pdb.set_trace()

    if count_db == count_df:
        logger.info("FILING {0} TABLE {1} with the same records already exists".format(FILING, TABLE_NAME))
        print "FILING {0} TABLE {1} with the same records already exists".format(FILING, TABLE_NAME)
        return 0
    else:
        df.head().to_sql(name=TABLE_NAME,con=engine, if_exists='append', index=False, dtype=dt)

        #bulk insert to DB
        #http://stackoverflow.com/questions/31997859/bulk-insert-a-pandas-dataframe-using-sqlalchemy
        import cStringIO
        output = cStringIO.StringIO()
        df.to_csv(output, sep='\t', header=False, index=False, encoding='utf-8')
        output.seek(0)
        contents = output.getvalue()
        connection = engine.raw_connection()
        cur = connection.cursor()
        cur.execute('truncate {0}'.format(TABLE_NAME))
        connection.commit()
        cur.copy_from(output, TABLE_NAME, sep='\t', null="")
        connection.commit()
        return 1




def update_raw_consolidate(FILING, YEAR, ID=1):
    """
    GIVEN FILING TYPE, THE YEAR OF THE FILING 
    INSERT/UPDATE THE CONSOLIDATED TABLE FROM THE INDIVIDUAL TABLE
    """

    INDIV_DB_CONNSTR= get_conn_str(FILING)
    if INDIV_DB_CONNSTR== 0: 
        return 0

    engine = sqlalchemy.create_engine(INDIV_DB_CONNSTR)
    engine_con = sqlalchemy.create_engine(FRANKSALARY_INSERT_CONNSTR_CONSOLIDATE)

    # the table that'll be updated in the consolidated database
    table_name = FILING.lower()


    sql =   """
                select * from column_std_name 
            """
    # a mapping from orig_col to std_col 
    all_map = pd.read_sql(sql, engine_con).set_index('orig_col')['std_col'].to_dict()

    # standard header names that the consolidated table uses
    sql =   """
                SELECT 	column_name, data_type
                FROM 	information_schema.columns
                WHERE 	table_name = '{0}'
                ORDER BY ordinal_position
            """
    con_df = pd.read_sql(sql.format(table_name), engine_con)
    std_hdrs = con_df['column_name'].tolist()
    std_types = con_df['data_type'].tolist()
    double_hdrs = con_df[con_df['data_type'] == 'double precision']['column_name'].tolist()

    START_QUERY =(
                    'select * \n'
                    'from dblink( \n'
                    '\'dbname=raw_{0}_data user={1} password={2}\',\n'
                    '\'select \n'
                 ).format(FILING.lower(), FRANKSALARY_DATABASE_USER,FRANKSALARY_DATABASE_PWD)

    COLS_QUERY = ',\n'.join(map(lambda x: x[0] + ' ' + x[1],zip(std_hdrs, std_types))) + '\n'

    END_QUERY = (
                    'as T( \n'
                    + COLS_QUERY +
                    ') \n'
                )

    if ID != 1:
        INDV_TABLE_NAME = 'yr{0}_{1}'.format(2000+YEAR, ID)
    else:
        INDV_TABLE_NAME = 'yr{0}'.format(2000+YEAR)

    sql =   """
                select column_name, data_type
                from information_schema.columns
                where table_name = '{0}'
            """
    #for each individual table, the non-standard headers and their data type
    indv_df = pd.read_sql(sql.format(INDV_TABLE_NAME), engine)
    cols = indv_df.set_index('column_name')['data_type'].to_dict()

    # check every raw_column header has a corresponding standardized version in the consolidated
    #all_mapped = True
    #for raw_cn in indv_df['column_name']:
    #    try:
    #        all_map[raw_cn]
    #    except:
    #        print raw_cn
    #        all_mapped = False
    #assert(all_mapped)


    indv_std2raw_map = {} #from std_col to raw_table_header
    for col in cols:
        try:
            indv_std2raw_map[all_map[col]] = col
        except:
            pass

    each_line = []


    wage_to_1_inserted = False
    for x in std_hdrs:
        if x == 'employment_confirmed':
            each_line.append('case when lower({0}) in (\'certification\', \'certified\', \'certified - full\', \'certified - partial\', \'partial certification\') then \'True\' else \'false\' end as {1}'.format(indv_std2raw_map[x], x))
        elif x == 'table_name':
            each_line.append('\'{0}\' as table_name'.format(INDV_TABLE_NAME))
        elif x in indv_std2raw_map:
            if x == 'employer_postal_code':
                each_line.append('lpad('+indv_std2raw_map[x]+'::text, 5, \'0\') as ' + x)
            elif x == 'wage_from_1' and cols[indv_std2raw_map[x]] == 'text': #case 20,000 - 50,000
                query = ('cast( \n'
                        'case \n'
                        '   when position(\'-\' in ' + indv_std2raw_map[x] + ') = 1 then null \n'
                        '   when position(\'-\' in ' + indv_std2raw_map[x] + ') > 0 \n'
                        '       then substring(' + indv_std2raw_map[x] + ', 1,position(\'-\' in ' + indv_std2raw_map[x] + ')-1) \n'
                        '   else ' + indv_std2raw_map[x] + ' \n'
                        'end as float) as wage_from_1')
                each_line.append(query)

                if not wage_to_1_inserted:
                    query = ('cast( \n'
                            'case'
                            '   when position(\'-\' in ' + indv_std2raw_map[x] + ') > 0 \n then'
                            '   case \n'
                            '       when trim(both ' ' from reverse(substring(reverse('+ indv_std2raw_map[x] +'),1,position(\'-\' in reverse('+ indv_std2raw_map[x] +'))-1))) = \'\' then null \n'
                            '       else reverse(substring(reverse('+ indv_std2raw_map[x] +'),1,position(\'-\' in reverse('+ indv_std2raw_map[x] +'))-1)) \n'
                            '   end \n'
                            '   else null \n'
                            'end as float) as wage_to_1')
                    each_line.append(query)
                    wage_to_1_inserted = True
            elif x in double_hdrs and cols[indv_std2raw_map[x]] == 'text':
                each_line.append('case when isnumeric({0}) then cast({1} as float) else null end as {2}'.format(indv_std2raw_map[x], indv_std2raw_map[x], x))
            else:
                each_line.append(indv_std2raw_map[x]+' as ' + x)
        else:
            if x == 'wage_to_1' and wage_to_1_inserted:
                continue
            else:
                each_line.append('null as ' + x)


    each_line = map(lambda s: s.replace('\'', '\'\''), each_line)

    select_statement = START_QUERY + ',\n'.join(each_line) + ' from {} \')'.format(INDV_TABLE_NAME) + END_QUERY

    query1 = 'DELETE FROM {0} WHERE table_name = \'{1}\';\n'.format(table_name, INDV_TABLE_NAME)
    query2 = 'CREATE EXTENSION IF NOT EXISTS dblink; \n'
    query3 = 'insert into {0} '.format(table_name) + \
        '(\n' + ',\n'.join(std_hdrs) + \
        ')\n (' + select_statement +  '\n);'


    with open('query_update_raw_consolidate.log','w') as text_file:
        text_file.write(query1)
        text_file.write(query2)
        text_file.write(query3)

    # Now execute the queries
    conn = engine_con.connect()
    conn.execute(query1)
    conn.execute(query2)
    conn.execute(query3)
    conn.close()
    
def update_app_data(FILING, YEAR):
    # IF THE RECORD IS DIFFERENT (including different count) THEN UPDATE THE COUNT AND TIMESTAMP
    # IF THE RECORD DOESN'T EXIST, THEN INSERT THE RECORD
    """
    MOVE GROUPED DATA FROM CONSOLIDATED TABLE TO THE APPLICATION DATABASE

    RETURN VALUE: the timestamp after which new records need to be updated
    """

    #table name in the applicaton database
    table_app = 'reviews_hires_{0}'.format(FILING.lower())
    #table name in the consolidated raw database
    table_con = FILING.lower()


    engine_app = sqlalchemy.create_engine(FRANKSALARY_INSERT_CONNSTR)
    engine_con = sqlalchemy.create_engine(FRANKSALARY_INSERT_CONNSTR_CONSOLIDATE)

    
    sql =   """
                SELECT 	column_name, data_type
                FROM 	information_schema.columns
                WHERE 	table_name = '{0}' AND column_name not in ('pid', 'count', 'updated_time')
                ORDER BY ordinal_position
            """

    df = pd.read_sql(sql.format(table_app), engine_app)
    std_hdrs = df['column_name'].tolist()
    std_types = df['data_type'].tolist()

    idx_cols = map(  lambda x: 'coalesce(' + x[0] + ',{0})'.format(
                                '\'\'' if x[1] == 'text' 
                                    else '\'1900-01-01\'' if x[1] == 'date'
                                        else 0.0 if x[1] == 'double precision'
                                            else 'false' if x[1] == 'boolean'
                                                else x[0]) , 
                            zip(std_hdrs, std_types))
    idx_cols = '\n,'.join(idx_cols)

    cols = '\n,'.join(std_hdrs)

    START_QUERY =(
                    'select * \n'
                    'from dblink( \n'
                    '\'dbname=raw_consolidate user={0} password={1}\',\n'
                    '\''
                 ).format(FRANKSALARY_DATABASE_USER,FRANKSALARY_DATABASE_PWD)

    sql = """
        SELECT 
            now() as updated_time
            ,{0}
            ,count(*) as count
        FROM {1}
        WHERE
            table_name like '{2}%'
        GROUP BY 
            {3}
    """
    sql = sql.format(cols, table_con, 'yr{0}'.format(2000+YEAR), cols).replace('\'', '\'\'')


    COLS_QUERY = ',\n'.join(map(lambda x: x[0] + ' ' + x[1],zip(std_hdrs, std_types))) + '\n'

    END_QUERY = (
                    'as T( \n' +
                       'updated_time timestamp with time zone, \n' + 
                        COLS_QUERY +
                        '\n ,count int' + 
                    ') \n'
                )

    query2 =    'CREATE EXTENSION IF NOT EXISTS dblink; \n'
    query3 =    'insert into {0} '.format(table_app) + \
                '(\n' + ',\n'.join(['updated_time'] + std_hdrs + ['count']) + \
                ')\n (' + START_QUERY + sql + '\')'  + END_QUERY + ') \n ON CONFLICT (' + \
                idx_cols + ') \n DO UPDATE SET count = EXCLUDED.count, updated_time = now() \n' + \
                'where EXCLUDED.count > {0}.count;'.format(table_app)


    with open('query_update_app_data.log','w') as text_file:
        text_file.write(query2)
        text_file.write(query3)
    
    update_time = datetime.datetime.now(pytz.timezone('GMT'))

    # Now execute the queries
    conn = engine_app.connect()
    
    conn.execute(sqlalchemy.text(query2))
    conn.execute(sqlalchemy.text(query3))
    conn.close()

    return update_time


def update_index(start_time):
    """
    Index the new records in Elastic Search

    """


    cwd = os.getcwd()
    for i in range(2):
        os.chdir('..')

    #shell_cmd = 'python manage.py update_index'
    shell_cmd = 'python manage.py update_index --batch-size=10000 --remove --start=\'{0}\''.format(str(start_time))
    print shell_cmd
    os.system(shell_cmd)

    os.chdir(cwd)

#Lastly 
def update_fsalary_data(FILING, YEAR, ID=1):
    print "update_raw_indv({0}, {1}, {2})".format(FILING, YEAR, ID)
    do_update = update_raw_indv(FILING, YEAR, ID)

    if do_update == 1:
        print "update_raw_consolidate({0}, {1}, {2})".format(FILING, YEAR, ID)
        update_raw_consolidate(FILING, YEAR, ID)

        print "update_app_data({0}, {1})".format(FILING, YEAR)
        timestamp = update_app_data(FILING, YEAR)

        print "update_index({0})".format(timestamp)
        update_index(timestamp)


class MyTest(unittest.TestCase):
    #def test_update_raw_indv(self):
    #    update_raw_indv(FILING='H1B', YEAR=9, ID=1)

    #def test_update_raw_consolidate(self):
    #    update_raw_consolidate(FILING='H2A', YEAR=8, ID=1)

    #def test_standardize_address(self):
    #    standardize_address()

    #def test_update_app_data(self):
    #    update_app_data(FILING='H1B', YEAR=9)

    #def test_update_index(self):
    #    update_index()
    pass




    #def test_update_fsalary_data(self):
    #    update_fsalary_data(FILING='H1B', YEAR=16)

if __name__ == "__main__":
    #unittest.main()
    year_list = range(8, 9)
    for i in year_list:
        update_fsalary_data(FILING='H2A', YEAR=i)

