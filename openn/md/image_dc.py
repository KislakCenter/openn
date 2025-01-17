# -*- coding: utf-8 -*-
import re
import mimetypes

from datetime import date
from openn.xml.openn_tei import OPennTEI
from openn.md.dublin_core import DublinCore
from openn.md.common_dc import CommonDC

from django.conf import settings

class ImageDC(CommonDC):

    BLANK_RE = re.compile('blank|unlabeled', re.I)

    def __init__(self, derivative):
        self._derivative = derivative
        kwargs = { 'document': self.image.document }
        super(ImageDC,self).__init__(**kwargs)

    @property
    def derivative(self):
        return self._derivative

    @property
    def image(self):
        return self.derivative.image

    def short_date(self):
        if self.tei.date_when:
            return self.tei.date_when
        elif self.tei.date_from:
            return ' - '.join([self.tei.date_from, self.tei.date_to ])
        elif self.tei.date_notBefore:
            return ' - '.join([self.tei.date_notBefore, self.tei.date_notAfter ])

    def origin(self):
        parts = [ x for x in ( self.tei.orig_place, self.short_date() ) if x ]
        return '(%s)' % (', '.join(parts),)

    def dc_identifier(self):
        return '%d.%d' % (self.document.id, self.image.id)

    def dc_relation(self):
        rels = [ self.tei.full_call_number ]
        rels += super(ImageDC, self).dc_relation()
        return rels

    def dc_date(self):
        return self.image.updated.strftime('%Y-%m-%d')

    def dc_title(self):
        return "%s, %s" % (self.tei.formal_title, self.image.display_label())

    def dc_description(self):
        s = 'This is'
        label = self.image.display_label()
        if not label or ImageDC.BLANK_RE.search(label) or label == 'None':
            s += ' an image'
        else:
            s += ' an image of %s' % (label, )

        s += ' from %s' % (self.tei.formal_title, )

        if self.tei.support:
            s += ', a document on %s' % (self.tei.support, )

        if self.tei.authors:
            s += ', by %s' % (', '.join(self.tei.author_names), )

        origin = self.origin()
        if origin:
            s += ' %s' % (origin,)

        if not s.endswith('.'):
            s += '.'

        return s

    def dc_format(self):
        path = self.derivative.path
        return path and mimetypes.guess_type(path)[0]

    def dc_source(self):
        return "%s, %s" % (self.tei.full_call_number, self.image.display_label())

    def dc_type(self):
        return 'image'
