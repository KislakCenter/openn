#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import sys
import glob
from django.utils import unittest
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError
from pprint import PrettyPrinter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
from openn.openn_exception import OPennException
from openn.prep.mmw_prep import MMWPrep
from openn.prep.file_list import FileList
from openn.xml.openn_tei import OPennTEI
from openn.prep.prep_setup import PrepSetup
from openn.prep.prep_config_factory import PrepConfigFactory
from openn.models import *
from openn.tests.openn_test_case import OPennTestCase
from openn.tests.helpers import *

class TestMMWPrep(OPennTestCase):

    staging_dir      = os.path.join(os.path.dirname(__file__), 'staging')
    staged_source    = os.path.join(staging_dir, 'ms_or_15')
    staged_penn_source = os.path.join(staging_dir, 'mscodex1905')
    staged_pages_xlsx = os.path.join(staged_source, 'pages.xlsx')
    staged_description_xml = os.path.join(staged_source, 'marc.xml')
    staged_flp_source = os.path.join(staging_dir, 'lewis_o_003')

    prep_cfg_factory = PrepConfigFactory(
        prep_configs_dict=settings.PREP_CONFIGS,
        prep_methods=settings.PREPARATION_METHODS,
        repository_configs=settings.REPOSITORIES,
        prep_context=settings.PREP_CONTEXT)
    columbia_mmw_prep_config = prep_cfg_factory.create_prep_config('columbia-mmw')
    penn_mmw_prep_config = prep_cfg_factory.create_prep_config('penn-mmw')
    flp_mmw_prep_config = prep_cfg_factory.create_prep_config('flp-mmw')

    # TODO: Use rich MARC XML for Columbia to test all fields
    # TODO: test all expected values in TEI

    columbia_mmw_files = (
        'ms_or_15_000_0000001.tif',
        'ms_or_15_000_0000002.tif',
        'ms_or_15_000_0000003.tif',
        'ms_or_15_000_0000004.tif',
        'ms_or_15_000_0000005.tif',
        'ms_or_15_000_0000006.tif',
        'ms_or_15_000_0000007.tif',
        'ms_or_15_000_0000008.tif',
        'ms_or_15_000_0000009.tif',
        'ms_or_15_000_0000010.tif',
        'ms_or_15_000_0000011.tif',
        'ms_or_15_000_0000012.tif',
        'ms_or_15_000_0000013.tif',
        'ms_or_15_000_0000014.tif',
        'ms_or_15_000_0000015.tif',
        'ms_or_15_000_0000016.tif',
        )

    penn_mmw_files = (
        'mscodex1905_body0000ref.tif',
        'mscodex1905_body0001.tif',
        'mscodex1905_body0002.tif',
        'mscodex1905_body0003.tif',
        'mscodex1905_body0004.tif',
        'mscodex1905_body0005.tif',
        'mscodex1905_body0006.tif',
        'mscodex1905_body0007.tif',
        'mscodex1905_body0008.tif',
        'mscodex1905_body0009.tif',
        'mscodex1905_body0010.tif',
        'mscodex1905_body0011.tif',
        'mscodex1905_body0012.tif',
        )

    flp_mmw_files = (
        'lewis_o_3_body0001.tif',
        'lewis_o_3_body0002.tif',
        'lewis_o_3_body0003.tif',
        'lewis_o_3_body0004.tif',
        'lewis_o_3_body0005.tif',
        'lewis_o_3_body0006.tif',
        'lewis_o_3_body0007.tif',
        'lewis_o_3_body0008.tif',
        'lewis_o_3_body0009.tif',
        'lewis_o_3_body0010.tif',
        )

    template_image = os.path.join(os.path.dirname(__file__), 'data/mscodex1223/mscodex1223_wk1_back0001.tif')
    template_pages_xlsx = os.path.join(os.path.dirname(__file__), 'data/muslim_world/ms_or_15.xlsx')
    template_description_xml = os.path.join(os.path.dirname(__file__), 'data/muslim_world/cu_ms_or_15.xml')
    template_dir = os.path.join(os.path.dirname(__file__),'data/muslim_world/ms_or_15')
    template_penn_dir = os.path.join(os.path.dirname(__file__), 'data/muslim_world/mscodex1905')
    template_flp_dir = os.path.join(os.path.dirname(__file__), 'data/muslim_world/lewis_o_003')


    pp               = PrettyPrinter(indent=2)
    expected_xpaths  = (
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:titleStmt/ns:title',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:publicationStmt/ns:publisher',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:publicationStmt/ns:availability/ns:licence',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:notesStmt/ns:note',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:msIdentifier/ns:settlement',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:msIdentifier/ns:institution',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:msIdentifier/ns:repository',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:msIdentifier/ns:idno',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:msIdentifier/ns:idno/@type',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:msIdentifier/ns:altIdentifier/ns:idno',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:msIdentifier/ns:altIdentifier/@type',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:msContents/ns:summary',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:msContents/ns:textLang',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:msContents/ns:msItem/@n',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:msContents/ns:msItem/ns:title',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:msContents/ns:msItem/ns:author',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:msContents/ns:msItem/ns:respStmt/ns:resp',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:msContents/ns:msItem/ns:respStmt/ns:persName',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:physDesc/ns:objectDesc/ns:supportDesc/@material',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:physDesc/ns:objectDesc/ns:supportDesc/ns:support/ns:p',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:physDesc/ns:objectDesc/ns:supportDesc/ns:extent',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:physDesc/ns:objectDesc/ns:layoutDesc/ns:layout',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:physDesc/ns:scriptDesc/ns:scriptNote',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:physDesc/ns:decoDesc/ns:decoNote',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:physDesc/ns:bindingDesc/ns:binding/ns:p',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:history/ns:origin/ns:p',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:history/ns:origin/ns:origDate',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:history/ns:origin/ns:origPlace',
        '/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:history/ns:provenance',
        '/ns:TEI/ns:teiHeader/ns:profileDesc/ns:textClass/ns:keywords/@n',
        '/ns:TEI/ns:teiHeader/ns:profileDesc/ns:textClass/ns:keywords/ns:term',
        '/ns:TEI/ns:facsimile/ns:graphic')

    expected_titles = (
        'Fragments of the Digests of Justinian, Book 37, Titles 7-9',
        'De dotis collatione (37.7.1.4), f. 1r',
        'De ventre in possessionem mittendo et curatore eius (37.9.1), f. 1v',
        'De coniungendis cum emancipato liberis eius (37.8.1.10), f. 2r')

    expected_deconotes = (
        'Initials (1-line to 3-line) alternating in red and blue ink, paragraph marks in red and blue ink, six-line Title 8 initial in red and blue ink.',
        'Puzzle initial, Initial S, f. 1v')

    def setUp(self):
        if os.path.exists(self.staging_dir):
            shutil.rmtree(self.staging_dir)

        if not os.path.exists(self.staging_dir):
            os.mkdir(self.staging_dir)

    def stage_default(self):
        if not os.path.exists(self.staged_source):
            os.mkdir(self.staged_source)

        shutil.copyfile(self.template_pages_xlsx, self.staged_pages_xlsx)
        shutil.copyfile(self.template_description_xml, self.staged_description_xml)
        for image in self.columbia_mmw_files:
            self.touch(os.path.join(self.staged_source, image))

    def stage_penn_ms(self):
        shutil.copytree(self.template_penn_dir, self.staging_dir)

    def tearDown(self):
        if os.path.exists(self.staging_dir):
            shutil.rmtree(self.staging_dir)

    def touch(self, filename, times=None):
        with(open(filename,'a')):
            os.utime(filename, times)

    def assertHasFile(self,file_list, group, path):
        for info in file_list[group]:
            if info['filename'] == path:
                return True
        raise AssertionError("Expected file: '%s' in group: '%s'" % (path,group))

    def assertNotHasFile(self,file_list, group, path):
        for info in file_list[group]:
            if info['filename'] == path:
                raise AssertionError("Should not have file: '%s' in group: '%s'" % (path,group))

    def pprint(self,thing):
        self.pp.pprint(thing)

    def stage_template(self, template_dir):
        shutil.copytree(template_dir, self.staged_source)

    def test_run(self):
        self.stage_template(self.template_dir)
        for image in self.columbia_mmw_files:
            self.touch(os.path.join(self.staged_source, image))
        doc_count = Document.objects.count()
        repo_wrapper = self.columbia_mmw_prep_config.repository_wrapper()
        doc = PrepSetup().prep_document(repo_wrapper, 'ms_or_15')
        prep = MMWPrep(source_dir=self.staged_source, document=doc,
                          prep_config = self.columbia_mmw_prep_config)

        prep.prep_dir()
        path = os.path.join(self.staged_source, 'PARTIAL_TEI.xml')
        self.assertTrue(os.path.exists(path), 'Expected path to exist: %s' % path)

        root = self.assertXmlDocument(open(path).read())
        self.assertXpathsExist(root, self.expected_xpaths)

    def test_penn_ms(self):
        # self.stage_template(self.template_penn_dir)
        shutil.copytree(self.template_penn_dir, self.staged_penn_source)
        for image in self.penn_mmw_files:
            self.touch(os.path.join(self.staged_penn_source, image))
        doc_count = Document.objects.count()
        repo_wrapper = self.penn_mmw_prep_config.repository_wrapper()
        doc = PrepSetup().prep_document(repo_wrapper, 'mscodex1905')
        prep = MMWPrep(source_dir=self.staged_penn_source, document=doc,
                        prep_config = self.penn_mmw_prep_config)

        prep.prep_dir()
        path = os.path.join(self.staged_penn_source, 'PARTIAL_TEI.xml')
        self.assertTrue(os.path.exists(path), 'Expected path to exist: %s' % path)

        root = self.assertXmlDocument(open(path).read())
        expected = list(self.expected_xpaths)
        expected.remove('/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:history/ns:origin/ns:origPlace',)
        self.assertXpathsExist(root, expected)

    def test_flp_ms(self):
        # self.stage_template(self.template_flp_dir)
        shutil.copytree(self.template_flp_dir, self.staged_flp_source)
        for image in self.flp_mmw_files:
            self.touch(os.path.join(self.staged_flp_source, image))
        doc_count = Document.objects.count()
        repo_wrapper = self.flp_mmw_prep_config.repository_wrapper()
        doc = PrepSetup().prep_document(repo_wrapper, 'lewis_o_003')
        prep = MMWPrep(source_dir=self.staged_flp_source, document=doc,
                        prep_config = self.flp_mmw_prep_config)

        prep.prep_dir()
        path = os.path.join(self.staged_flp_source, 'PARTIAL_TEI.xml')
        self.assertTrue(os.path.exists(path), 'Expected path to exist: %s' % path)

        root = self.assertXmlDocument(open(path).read())
        expected = list(self.expected_xpaths)
        expected.remove('/ns:TEI/ns:teiHeader/ns:fileDesc/ns:sourceDesc/ns:msDesc/ns:history/ns:origin/ns:origPlace',)
        self.assertXpathsExist(root, expected)
    ##
    # TODO: Re-enable all of these
    #
    # def test_bad_holdingid(self):
    #     # setup
    #     self.stage_template()
    #     shutil.copyfile(self.bad_holdingid_txt, self.staged_holdingid)
    #     doc_count = Document.objects.count()
    #     repo_wrapper = self.pennpih_prep_config.repository_wrapper()
    #     doc = PrepSetup().prep_document(repo_wrapper, 'mscodex1223')
    #     prep = MedrenPrep(source_dir=self.staged_source, document=doc,
    #                       prep_config = self.pennpih_prep_config)
    #     # run
    #     with self.assertRaisesRegexp(OPennException, r'999999999999999999'):
    #         prep.prep_dir()
    # # ljs472_wk1_back0002a.tif    # not used by PIH
    # # ljs472_wk1_back0002b.tif    # not used by PIH
    # # ljs472_wk1_body0065a.tif    # extra file; listed in PIH
    # # ljs472_wk1_body0065b.tif    # extra file; listed in PIH
    # # ljs472_wk1_body0193.tif     # 'blank' file not in PIH
    # # ljs472_wk1_body0194.tif     # 'blank' file not in PIH
    # # ljs472_wk1_body0195.tif     # 'blank' file not in PIH
    # # ljs472_wk1_body0196.tif     # 'blank' file not in PIH
    # def test_complex_names(self):
    #     # setup
    #     shutil.copytree(self.complex_files, self.complex_staged)
    #     repo_wrapper = self.ljs_prep_config.repository_wrapper()
    #     doc = PrepSetup().prep_document(repo_wrapper, 'ljs472')
    #     prep = MedrenPrep(self.complex_staged, doc, self.ljs_prep_config)
    #     files = prep.build_file_list(self.complex_pih_xml)
    #     self.assertHasFile(files, 'document', 'data/ljs472_wk1_body0193.tif')
    #     self.assertHasFile(files, 'document', 'data/ljs472_wk1_body0194.tif')
    #     self.assertHasFile(files, 'document', 'data/ljs472_wk1_body0195.tif')
    #     self.assertHasFile(files, 'document', 'data/ljs472_wk1_body0196.tif')
    #     self.assertHasFile(files, 'document', 'data/ljs472_wk1_body0065a.tif')
    #     self.assertHasFile(files, 'document', 'data/ljs472_wk1_body0065b.tif')
    #     self.assertHasFile(files, 'extra', 'data/ljs472_wk1_back0002a.tif')
    #     self.assertHasFile(files, 'extra', 'data/ljs472_wk1_back0002a.tif')
    #     self.assertNotHasFile(files, 'extra', 'data/ljs472_wk1_body0193.tif')
    #     self.assertNotHasFile(files, 'extra', 'data/ljs472_wk1_body0194.tif')
    #     self.assertNotHasFile(files, 'extra', 'data/ljs472_wk1_body0195.tif')
    #     self.assertNotHasFile(files, 'extra', 'data/ljs472_wk1_body0196.tif')
    #     self.assertNotHasFile(files, 'extra', 'data/ljs472_wk1_body0065a.tif')
    #     self.assertNotHasFile(files, 'extra', 'data/ljs472_wk1_body0065b.tif')
    #     self.assertNotHasFile(files, 'document', 'data/ljs472_wk1_back0002a.tif')
    #     self.assertNotHasFile(files, 'document', 'data/ljs472_wk1_back0002a.tif')

    # def test_tei_generation(self):
    #     self.stage_template()
    #     doc_count = Document.objects.count()
    #     repo_wrapper = self.pennpih_prep_config.repository_wrapper()
    #     doc = PrepSetup().prep_document(repo_wrapper, 'mscodex1223')
    #     prep = MedrenPrep(source_dir=self.staged_source, document=doc,
    #                       prep_config = self.pennpih_prep_config)
    #     shutil.copyfile(self.mscodex1223_marmite, self.staged_pih)
    #     xml = prep.gen_partial_tei()
    #     root = self.assertXmlDocument(xml)
    #     self.assertXpathsExist(root, self.expected_xpaths)
    #     self.assertXpathValues(root, '//ns:titleStmt/ns:title/text()', ('Description of University of Pennsylvania Oversize Ms. Codex 1223: Fragments of the Digests of Justinian, Book 37, Titles 7-9',))
    #     self.assertXpathValues(root, '//ns:msContents/ns:msItem/ns:title/text()', self.expected_titles)
    #     self.assertXpathValues(root, '//ns:msContents/ns:msItem/@n', ('1r', '1v', '2r'))
    #     self.assertXpathValues(root, '//ns:msDesc/ns:physDesc/ns:decoDesc/ns:decoNote/text()', self.expected_deconotes)
    #     self.assertXpathValues(root, '//ns:msDesc/ns:physDesc/ns:decoDesc/ns:decoNote/@n', ('1v',))
    #     self.assertXpathValues(root, '//ns:extent/text()', ('2 leaves : 429 x 289 (237 x 135) mm. bound to 439 x 295 mm',))

    # def test_tei_with_item_number(self):
    #     self.stage_template()
    #     doc_count = Document.objects.count()
    #     repo_wrapper = self.pennpih_prep_config.repository_wrapper()
    #     doc = PrepSetup().prep_document(repo_wrapper, 'mscodex1223')
    #     prep = MedrenPrep(source_dir=self.staged_source, document=doc,
    #                       prep_config = self.pennpih_prep_config)
    #     shutil.copyfile(self.ms_coll_390_item_1044_marmite, self.staged_pih)
    #     os.remove(self.staged_holdingid)
    #     xml = prep.gen_partial_tei()
    #     root = self.assertXmlDocument(xml)
    #     self.assertXpathValues(root, '//ns:msDesc/ns:msIdentifier/ns:idno/text()', ('Ms. Coll. 390 Item 1044',))

    # def test_tei_extent(self):
    #     self.stage_template()
    #     repo_wrapper = self.pennpih_prep_config.repository_wrapper()
    #     doc = PrepSetup().prep_document(repo_wrapper, 'mscodex1223')
    #     prep = MedrenPrep(source_dir=self.staged_source, document=doc,
    #                       prep_config = self.pennpih_prep_config)
    #     shutil.copyfile(self.msoversize8_marmite, self.staged_pih)
    #     os.remove(self.staged_holdingid)
    #     xml = prep.gen_partial_tei()
    #     root = self.assertXmlDocument(xml)
    #     self.assertXpathValues(root, '//ns:extent/text()', ('1 item (1 leaf) : 36 x 44 cm',))

if __name__ == '__main__':
    unittest.main()
