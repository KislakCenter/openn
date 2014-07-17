#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys

from exiftool import ExifTool

from django.utils import unittest
from django.test import TestCase
from django.conf import settings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.prep.exif_manager import ExifManager

class TestExifManager(TestCase):

    staging_dir      = os.path.join(os.path.dirname(__file__), 'staging')
    source_dir       = os.path.join(os.path.dirname(__file__), 'data/mscodex1223')
    test_image_names = [ 'mscodex1223_wk1_body0001.tif', 'mscodex1223_wk1_body0002.tif', 'mscodex1223_wk1_body0003.tif' ]
    test_images      = [ os.path.join(source_dir, img) for img in test_image_names ]
    staged_images    = [ os.path.join(staging_dir, img) for img in test_image_names ]
    img_desc         = { 'ImageDescription': 'This is the image description' }
    img_desc_nl      = { 'ImageDescription': """This is the two-line
description""" }
    xmp_marked       = { 'xmpRights:Marked': 'true' }
    # the following has a unicode (c) symbol
    dc_rights        = { 'dc:Rights': 'The dc rights ©2014' }
    tag_dict         = { 'Marked': True, 'rights': 'The dc rights ©2014' }

    def setUp(self):
        if not os.path.exists(TestExifManager.staging_dir):
            os.mkdir(TestExifManager.staging_dir)
        self._exiftool = ExifTool()

    def tearDown(self):
        if os.path.exists(TestExifManager.staging_dir):
           shutil.rmtree(TestExifManager.staging_dir)
        self._exiftool.terminate()

    def get_metadata(self,img):
        with ExifTool() as et:
            md = et.get_metadata(img)
        return md

    def stage_images(self):
        for f in TestExifManager.test_images:
            shutil.copy(f, TestExifManager.staging_dir)

    def stage_image(self, index=0):
        shutil.copy(TestExifManager.test_images[index],
                TestExifManager.staged_images[index])
        return TestExifManager.staged_images[index]
    
    def test_init(self):
        self.assertIsInstance(ExifManager(), ExifManager)

    def test_add_tag(self):
        img = self.stage_image(0)
        xman = ExifManager()
        xman.add_metadata([img], TestExifManager.img_desc)
        md = self.get_metadata(img)
        self.assertIn('EXIF:ImageDescription', md)
        self.assertIn('the image description', md['EXIF:ImageDescription'])

    def test_add_nl_tag(self):
        img = self.stage_image(0)
        xman = ExifManager()
        xman.add_metadata([img], TestExifManager.img_desc_nl)
        md = self.get_metadata(img)
        self.assertIn('EXIF:ImageDescription', md)
        self.assertIn(TestExifManager.img_desc_nl.values()[0], md['EXIF:ImageDescription'])

    def test_add_xmp_metadata(self):
        self.stage_images()
        xman = ExifManager()
        xman.add_metadata(TestExifManager.staged_images, TestExifManager.xmp_marked)
        for img in TestExifManager.staged_images:
            md = self.get_metadata(img)
            self.assertIn('XMP:Marked', md)
            self.assertTrue(os.path.exists(img + "_original"))
    
    def test_add_json_metadata(self):
        self.stage_images()
        xman = ExifManager()
        xman.add_json_metadata(TestExifManager.staged_images, TestExifManager.tag_dict)
        for img in TestExifManager.staged_images:
            md = self.get_metadata(img)
            self.assertIn('XMP:Marked', md)
            self.assertIn('XMP:Rights', md)
            self.assertTrue(os.path.exists(img + "_original"))


if __name__ == '__main__':
    unittest.main()
