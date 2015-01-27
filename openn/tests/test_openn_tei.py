#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import sys
from django.utils import unittest
from django.test import TestCase
from django.conf import settings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.xml.openn_tei import OPennTEI

class TestOPennTEI(TestCase):


    test_partial_tei = os.path.join(os.path.dirname(__file__), 'data/xml/ms1223_PARTIAL_TEI.xml')
    ljs270_tei       = os.path.join(os.path.dirname(__file__), 'data/xml/ljs270_TEI.xml')
    ljs454_tei       = os.path.join(os.path.dirname(__file__), 'data/xml/ljs454_TEI.xml')
    ljs471_tei       = os.path.join(os.path.dirname(__file__), 'data/xml/ljs471_TEI.xml')
    ljs498_tei       = os.path.join(os.path.dirname(__file__), 'data/xml/ljs498_TEI.xml')
    mscodex1589_tei  = os.path.join(os.path.dirname(__file__), 'data/xml/mscodex1589_TEI.xml')
    mscodex218_tei   = os.path.join(os.path.dirname(__file__), 'data/xml/mscodex218_TEI.xml')
    mscodex52_tei    = os.path.join(os.path.dirname(__file__), 'data/xml/mscodex52_TEI.xml')
    mscodex75_tei    = os.path.join(os.path.dirname(__file__), 'data/xml/mscodex75_TEI.xml')
    mscodex906_tei   = os.path.join(os.path.dirname(__file__), 'data/xml/mscodex906_TEI.xml')
    mscodex83_tei    = os.path.join(os.path.dirname(__file__), 'data/xml/mscodex83_TEI.xml')


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_call_number(self):
        openn_tei = OPennTEI(open(TestOPennTEI.test_partial_tei))
        self.assertEqual('Ms. Codex 1223', openn_tei.call_number)

    def test_get_title(self):
        openn_tei = OPennTEI(open(TestOPennTEI.test_partial_tei))
        self.assertEqual('Fragments of the Digests of Justinian, Book 37, Titles 7-9', openn_tei.title)

    def test_foliation(self):
        openn_tei = OPennTEI(open(self.mscodex52_tei))
        self.assertEqual('Paper, i (contemporary paper) + 119; 1-94, [95-119]; contemporary foliation in ink, modern foliation in pencil, upper right recto.', openn_tei.foliation)

    def test_layout(self):
        openn_tei = OPennTEI(open(self.ljs270_tei))
        self.assertEqual('Inscribed in 23 lines on 2 sides of the tablet.', openn_tei.layout)

    def test_colophon(self):
        openn_tei = OPennTEI(open(self.mscodex83_tei))
        self.assertEqual('Colophon (f. 32v): Explicit hic liber; de pena sum modo liber/ Explicit hoc totum; pro pena da michi potum/ Explicit expliceat; ludere scriptor eat/ Finito libro sit laus et gloria Christo.', openn_tei.colophon)

    def test_collation(self):
        openn_tei = OPennTEI(codecs.open(self.mscodex906_tei))
        self.assertEqual(u'Paper, 342; 1-18¹⁶ 19¹⁸ 20-22¹⁶; [ii], 1-317, 319-340, [i]; misnumbered at 318, no loss of text. Foliation and line numbering in a later hand. Signatures at bottom right; catchwords at bottom center, often cropped.', openn_tei.collation)

    def test_script(self):
        openn_tei = OPennTEI(codecs.open(self.mscodex906_tei))
        self.assertEqual(u'Written in Gothic cursive, with the first words or first line at the beginning of sections in bâtarde script; f. 306-322v (a single gathering) in a second hand.', openn_tei.script)

    def test_decoration(self):
        openn_tei = OPennTEI(codecs.open(self.mscodex906_tei))
        self.assertEqual(u'Many 2- and 3-line initials in red; capital at beginning of each line stroked with yellow; rubrication in red, often with cropped notes for rubrication or illustration barely visible at edge of page; spaces for illumination, approximately 9 lines in height, are frequent at the beginning of the manuscript but disappear in the second half (after f. 171v).', openn_tei.decoration)

    def test_binding(self):
        openn_tei = OPennTEI(open(self.mscodex906_tei))
        self.assertEqual(u'Contemporary blind-stamped calf, rebacked; wormholes in boards, leather, and text near spine.', openn_tei.binding)

    def test_origin(self):
        openn_tei = OPennTEI(open(self.mscodex906_tei))
        self.assertEqual(u'Written in France after 1474, based on primary watermark.', openn_tei.origin)

    def test_watermark(self):
        openn_tei = OPennTEI(open(self.ljs498_tei))
        self.assertEqual(u'Similar to Briquet, Aigle à deux têtes 285 (f. 45, 48; Gratz, 1594-1598; Millstatt (Carinthie), 1597-1600; Vienna, 1599) and Aigle à deux têtes 282 (Gratz, 1580; Osnabruck, 1588); similar to Briquet, Aigle à deux têtes 291 (f. 189; Gratz, 1598; Kempten, 1607-1627).', openn_tei.watermark)

    def test_signatures(self):
        openn_tei = OPennTEI(open(self.mscodex75_tei))
        self.assertEqual(u'Some signatures visible in red in the first half of some quires.', openn_tei.signatures)


if __name__ == '__main__':
    unittest.main()
