from django import template
import time

register = template.Library()


@register.filter('title_facet')
def title_facet(orig_str):
    """
        remove underscores and capitalize first character of each word
    """
    return ' '.join([x.title() for x in orig_str.split('_')])


@register.filter('secToDate')
def secToDate(sec):
    """
        convert epoch time to string format
    """

    return time.strftime('%m/%d/%Y', time.localtime(sec/1000))
