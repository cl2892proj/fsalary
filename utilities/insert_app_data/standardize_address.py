from private_settings import *
import sqlalchemy
import pandas as pd
import numpy as np
import unittest
import pdb
import logging
import geocoder


#LOGGING SETUP
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('standardize_address.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def create_append2_std_address():
    engine_con = sqlalchemy.create_engine(FRANKSALARY_INSERT_CONNSTR_CONSOLIDATE)
    sql = """
        select 
            work_location_city1, work_location_state1 
        from perm 
        limit 10
    """
    df = pd.read_sql(sql, engine_con)

    # free geocoding service with no limit yet
    g_arc = geocoder.arcgis('New York, NY')
    js = g_arc.json
    if js['ok']:
        js['address']
        js['lat']
        js['lng']





class MyTest(unittest.TestCase):
    def test_create_append2_std_address(self):
        create_append2_std_address()


if __name__ == "__main__":
    unittest.main()
