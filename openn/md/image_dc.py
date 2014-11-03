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

    def dc_identifier(self):
        return '%d.%d' % (self.document.id, self.image.id)

    def dc_relation(self):
        rels = [ '%s %s' % (self.tei.institution, self.document.call_number) ]
        rels += super(ImageDC, self).dc_relation()
        return rels

    def dc_date(self):
        return self.image.updated.strftime('%Y-%m-%d')

    def dc_title(self):
        return "%s, %s" % (self.tei.formal_title, self.image.display_label())

    def dc_description(self):
        s = 'This is'
        label = self.image.display_label()
        if not label or ImageDC.BLANK_RE.search(label):
            s += ' an image'
        else:
            s += ' an image of %s' % (label, )

        s += ' from %s' % (self.tei.formal_title, )

        if self.tei.support:
            s += ', a document on %s' % (self.tei.support, )

        if self.tei.authors:
            s += ', by %s' % (', '.join(self.tei.authors), )

        if self.tei.orig_place:
            s += ', from %s' % (self.tei.orig_place, )

        if self.tei.orig_date:
            s += ', dated to %s' % (self.tei.orig_date, )

        s += '.'

        return s

    def dc_format(self):
        path = self.derivative.path
        return path and mimetypes.guess_type(path)[0]

    def dc_source(self):
        vals = (self.tei.institution, self.tei.call_number,
                self.image.display_label())
        return "%s %s, %s" % vals

    def dc_type(self):
        return 'image'
