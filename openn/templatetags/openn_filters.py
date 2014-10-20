from django import template
from django.template.defaultfilters import stringfilter
import os
import re

register = template.Library()

gig = 1024**3
meg = 1024**2
kil = 1024

ANAME_RE = re.compile('[^a-zA-Z0-9]')

def format_size(num, unit):
    return '%.2f %s' % (round(float(num),1), unit)

@register.filter
def doit(value):
    return value

@register.filter
def mb(value):
    num = None
    try:
        num = float(value)
    except:
        return value

    if (num > gig):
        return format_size(num/gig, 'GB')
    elif (num > meg):
        return format_size(num/meg, 'MB')
    elif (num > kil):
        return format_size(num/kil, 'KB')
    else:
        return '%d B' % int(num)

@register.filter(name='basename')
@stringfilter
def basename(value):
    return os.path.basename(value)


@register.filter(name='aname')
@stringfilter
def aname(value):
    return "a%s" % (ANAME_RE.sub('', value).lower(),) if value else None
