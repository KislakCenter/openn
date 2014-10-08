#!/usr/bin/env python

import os
from django.template import Context, Template
from django.conf import settings
from django.template.loader import get_template

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openn.settings')

settings.configure(DEBUG=True, TEMPLATE_DEBUG=True)

settings.TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '../openn/templates'), )

# t = Template("My name is {{ name }}")
t = get_template('3_Collections.html')
c = Context({ 'collections': [ { 'name': 'Doug' } ] })

print t.render(c)
