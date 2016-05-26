from django import template

register = template.Library()


@register.filter('title_facet')
def title_facet(orig_str):
    return ' '.join([x.title() for x in orig_str.split('_')])
