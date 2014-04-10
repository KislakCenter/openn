#!/usr/bin/env python

from django.template import Context, Template
from django.conf import settings

settings.configure(DEBUG=True, TEMPLATE_DEBUG=True)

t = Template("My name is {{ name }}")

c = Context({ 'name': 'Doug' })

print t.render(c)