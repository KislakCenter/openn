# -*- coding: utf-8 -*-
from datetime import date
from openn.xml.openn_tei import OPennTEI
from openn.md.dublin_core import DublinCore

class DocumentDC(CommonDC):
    """The following Dublin Core elements are used:

    - Identifier: the shelf mark for manuscripts and other documents
      (e.g., University of Pennsylvania Ms. Codex 1223), and the image
      serial number for images (e.g., 0001_0123)

    - Date: the date of the image's publication

    - Title: the title of the document or image (e.g, “University of
      Pennsylvania Ms. Codex 1223, Fragments of the Digests of
      Justinian, Book 37, Titles 7-9” or "Image of fol. 1r of
      University of Pennsylvania Ms. Codex 1223, Fragments of the
      Digests of Justinian, Book 37, Titles 7-9")

    - Description: a description of the document

    - Source: source of the object used to create the image or image
      collection (e.g., "University of Pennsylvania Ms. Codex 1223,
      Fragments of the Digests of Justinian, Book 37, Titles 7-9")

    - Type: Image for individual images; Collection for all images of a manuscript

    - Format: image/tiff for images, text/html for a manuscript web page

    - Subject: keywords describing the manuscript or imaged folio

    - Rights: license and usage terms

    """
    def __init__(self, document):
        kwargs = { 'document': document }

        super(DocumentDC,self).__init__(**kwargs)

    def dc_identifier(self):
        return "%s %s" % (self.tei.repository, self.document.call_number)

    def dc_date(self):
        return self.document.updated.strftime('%Y-%m-%d')

    def dc_title(self):
        return self.tei.tei_title

    def dc_description(self):
        return self.tei.summary

    def dc_type(self):
        return 'collection'

    def dc_format(self):
        return 'text/html'

    def dc_source(self):
        parts = (self.tei.institution, self.tei.call_number, self.title)
        return "%s %s: %s" % parts

    def dc_rights(self):
        return [lic.text for lic in self.tei.licences]

    def dc_language(self):
        """Return the language of the TEI document; this is always English.
        """
        return 'eng'
