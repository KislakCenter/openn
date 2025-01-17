# -*- coding: utf-8 -*-

import os
import datetime

SECRET_KEY = None
skey_file = os.path.join(os.path.dirname(__file__), 'secret_key.txt')
today = datetime.date.today()
if os.environ.get('OPENN_SECRET_KEY') is not None:
    SECRET_KEY = os.environ['OPENN_SECRET_KEY']
elif os.path.exists(skey_file):
    SECRET_KEY = open(skey_file).read().strip()

# From the docs:
#
#    The lifetime of a database connection, in seconds. Use 0 to close
#    database connections at the end of each request — Django's historical
#    behavior — and None for unlimited persistent connections.
#
# Prevent MySQL error 2006:
#
#    (2006, 'MySQL server has gone away')
#
# See this SO question:
#
#     http://stackoverflow.com/questions/26958592/django-after-upgrade-mysql-server-has-gone-away
#
CONN_MAX_AGE = 0

REQUIRED_ENV_VARS = [
    'OPENN_DB_NAME',
    'OPENN_DB_USER',
    'OPENN_DB_PASSWORD',
    'OPENN_DB_HOST',
    'OPENN_DB_PORT',
    'OPENN_SAXON_JAR',
    'OPENN_STAGING_DIR',
    'OPENN_PACKAGE_DIR' ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['OPENN_DB_NAME'],
        'USER': os.environ['OPENN_DB_USER'],
        'PASSWORD': os.environ['OPENN_DB_PASSWORD'],
        'HOST': os.environ['OPENN_DB_HOST'],
        'PORT': os.environ['OPENN_DB_PORT'],
        'OPTIONS': {
            'init_command': 'SET character_set_connection=utf8,collation_connection=utf8_unicode_ci',
        },
    }
}

# Files matching the following pattern will be cleaned from source
# directories.  The pattern must be a valid, UNCOMPILED python regular
# expression string.
CLOBBER_PATTERN = 'Thumbs.db|.*\.lnk'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.environ['SDBM_DB_NAME'],
#         'USER': os.environ['SDBM_DB_USER'],
#         'PASSWORD': os.environ['SDBM_DB_PASSWORD'],
#         'HOST': os.environ['SDBM_DB_HOST'],
#         'OPTIONS': {
#             'init_command': 'SET storage_engine=INNODB',
#         },
#     }
# }

INSTALLED_APPS = (
        'openn', 'south', 'markdown_deux', 'ordered_model','django_extensions',
        )

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

PROJECT_PATH = os.path.abspath(os.path.join(__file__, '../..'))

TIME_ZONE = 'US/Eastern'
USE_TZ = True

OPENN_HOST = os.getenv('OPENN_HOST', 'openn.library.upenn.edu')

# put the openn/bin dir in the path
os.environ['PATH'] = os.path.join(PROJECT_PATH, 'bin') + os.pathsep + os.environ['PATH']

DERIV_CONFIGS = {
        'web': {
            'ext': 'jpg',
            'max_side': 1800,

            },
        'thumb': {
            'ext': 'jpg',
            'max_side': 190,
            },
        }

# URL to bibliophilly keywords TEI encodingDesc. File should have content like this.
#
#   <?xml version="1.0" encoding="UTF-8"?>
#   <encodingDesc xmlns="http://www.tei-c.org/ns/1.0">
#       <classDecl>
#           <taxonomy xml:id="keywords">
#               <category xml:id="keyword_1">
#                   <catDesc>Book Type</catDesc>
#               <category xml:id="keyword_1.2">
#                   <catDesc>Accounts</catDesc>
#               </category>
#               <!-- ... etc. -->
#           </taxonomy>
#       </classDecl>
#   </encodingDesc>
#
BIBLIO_PHILLY_KEYWORDS_DIR = os.path.join(PROJECT_PATH, 'vendor', 'bibliophilly-keywords')

TEMPLATE_DIRS = (os.path.join(SITE_ROOT, 'templates'), )

README_TEMPLATES = [ { 'file': 'ReadMe.html', 'title': 'Read Me' },
                     { 'file': 'TechnicalReadMe.html', 'title': 'Technical Read Me' } ]
REPOSITORIES_TEMPLATE = 'Repositories.html'
CURATED_COLLECTIONS_TEMPLATE = 'CuratedCollections.html'

STAGING_DIR = os.environ['OPENN_STAGING_DIR']
PACKAGE_DIR = os.environ['OPENN_PACKAGE_DIR']
ARCHIVE_DIR = os.environ['OPENN_ARCHIVE_DIR']
SITE_DIR = os.environ['OPENN_SITE_DIR']

TOC_DIR = 'html'

LICENSE_CC_BY_SA_40 = {
    'code': 'CC-BY-SA',
    'version': '4.0',
    'metadata': u'Metadata is ©{year} {holder} and licensed under a Creative Commons'
                ' Attribution ShareAlike License version 4.0'
                ' (CC-BY-SA-4.0 https://creativecommons.org/licenses/by-sa/4.0/legalcode.'
                ' For a description of the terms of use see the Creative Commons Deed'
                ' https://creativecommons.org/licenses/by/4.0/. {more_information}',
    'images': u'Images are  ©{year} {holder} and licensed under a Creative Commons Attribution'
             ' ShareAlike License version 4.0'
             ' (CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/legalcode.'
             ' For a description of the terms of use see the Creative Commons Deed'
             ' https://creativecommons.org/licenses/by/4.0/. {more_information}',
    'single_image': u'This image of {title} is ©{year} {holder} and licensed under a Creative'
                   ' Commons Attribution ShareAlike License version 4.0 (CC-BY-4.0'
                   ' https://creativecommons.org/licenses/by-sa/4.0/legalcode.'
                   ' For a description of the terms of use see the Creative Commons Deed'
                   ' https://creativecommons.org/licenses/by-sa/4.0/. {more_information}',
    'legalcode_url': 'https://creativecommons.org/licenses/by-sa/4.0/legalcode',
    'deed_url': 'https://creativecommons.org/licenses/by-sa/4.0/',
    'marked': True
}

LICENSE_CC_BY_40 = {
    'code': 'CC-BY',
    'version': '4.0',
    'metadata': u'Metadata is ©{year} {holder} and licensed under a Creative Commons Attribution'
                ' License version 4.0 (CC-BY-4.0'
                ' https://creativecommons.org/licenses/by/4.0/legalcode.'
                ' For a description of the terms of use see the Creative Commons Deed'
                ' https://creativecommons.org/licenses/by/4.0/. {more_information}',
    'images': u'Images are  ©{year} {holder} and licensed under a Creative Commons Attribution'
            ' License version 4.0 (CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/legalcode.'
            ' For a description of the terms of use see the Creative Commons Deed'
            ' https://creativecommons.org/licenses/by/4.0/. {more_information}',
    'single_image': u'This image of {title} is ©{year} {holder} and licensed under a Creative'
                    ' Commons Attribution License version 4.0 (CC-BY-4.0'
                    ' https://creativecommons.org/licenses/by/4.0/legalcode.'
                    ' For a description of the terms of use see the Creative Commons Deed'
                    ' https://creativecommons.org/licenses/by/4.0/. {more_information}',
    'legalcode_url': 'https://creativecommons.org/licenses/by/4.0/legalcode',
    'deed_url': 'https://creativecommons.org/licenses/by/4.0/',
    'marked': True
}

LICENSE_CC0_10 = {
    'code': 'CC0',
    'version': '1.0',
    'metadata': u'To the extent possible under law, {holder} has waived all copyright and related'
                ' or neighboring rights to this metadata about {title}. This work is published'
                ' from: United States. For a summary of CC0, see'
                ' https://creativecommons.org/publicdomain/zero/1.0/. Legal code:'
                ' https://creativecommons.org/publicdomain/zero/1.0/legalcode.  {more_information}',
    'images': u'To the extent possible under law, {holder} has waived all copyright and related or'
            ' neighboring rights to these images and the content of {title}. This work is published'
            ' from: United States. For a summary of CC0, see'
            ' https://creativecommons.org/publicdomain/zero/1.0/. Legal code:'
            ' https://creativecommons.org/publicdomain/zero/1.0/legalcode. {more_information}',
    'single_image': u'To the extent possible under law, {holder} has waived all copyright and'
                    ' related or neighboring rights to this image and the content of {title}. This'
                    ' work is published from: United States. For a summary of CC0, see'
                    ' https://creativecommons.org/publicdomain/zero/1.0/. Legal code:'
                    ' https://creativecommons.org/publicdomain/zero/1.0/legalcode. {more_information}',
    'legalcode_url': 'https://creativecommons.org/publicdomain/zero/1.0/legalcode',
    'deed_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
    'marked': True
}

LICENSE_PD_10 = {
    'code': 'PD',
    'version': '1.0',
    'metadata': u'This metadata about {title} is free of known copyright restrictions and in the'
                ' public domain. See the Creative Commons Public Domain Mark page for usage'
                ' details, http://creativecommons.org/publicdomain/mark/1.0/. {more_information}',
    'images': u'These images and the content of {title} are free of known copyright restrictions'
             ' and in the public domain. See the Creative Commons Public Domain Mark page for usage'
             ' details, http://creativecommons.org/publicdomain/mark/1.0/. {more_information}',
    'single_image': u'This image and the content of {title} are free of known copyright'
                    ' restrictions and in the public domain. See the Creative Commons Public Domain'
                    ' Mark page for usage details,'
                    ' http://creativecommons.org/publicdomain/mark/1.0/. {more_information}',
    'legalcode_url': 'http://creativecommons.org/publicdomain/mark/1.0/',
    'deed_url': 'http://creativecommons.org/publicdomain/mark/1.0/',
    'marked': False
}
LICENSE_CC_BY_SA_20 = {
    'code': 'CC-BY-SA-20',
    'version': '2.0',
    'metadata': u'Metadata is ©{year} {holder} and licensed under a Creative Commons'
                ' Attribution ShareAlike License version 2.0'
                ' (CC-BY-SA-2.0 https://creativecommons.org/licenses/by-sa/2.0/legalcode.'
                ' For a description of the terms of use see the Creative Commons Deed'
                ' https://creativecommons.org/licenses/by/2.0/. {more_information}',
    'images': u'Images are  ©{year} {holder} and licensed under a Creative Commons Attribution'
             ' ShareAlike License version 4.0'
             ' (CC-BY-2.0 https://creativecommons.org/licenses/by/2.0/legalcode.'
             ' For a description of the terms of use see the Creative Commons Deed'
             ' https://creativecommons.org/licenses/by/2.0/. {more_information}',
    'single_image': u'This image of {title} is ©{year} {holder} and licensed under a Creative'
                   ' Commons Attribution ShareAlike License version 2.0 (CC-BY-2.0'
                   ' https://creativecommons.org/licenses/by-sa/2.0/legalcode.'
                   ' For a description of the terms of use see the Creative Commons Deed'
                   ' https://creativecommons.org/licenses/by-sa/2.0/. {more_information}',
    'legalcode_url': 'https://creativecommons.org/licenses/by-sa/2.0/legalcode',
    'deed_url': 'https://creativecommons.org/licenses/by-sa/2.0/',
    'marked': True

}

LICENSES = {
    'CC-BY-SA' : LICENSE_CC_BY_SA_40,
    'CC-BY': LICENSE_CC_BY_40,
    'CC0': LICENSE_CC0_10,
    'PD': LICENSE_PD_10,
    'CC-BY-SA-40' : LICENSE_CC_BY_SA_40,
    'CC-BY-40': LICENSE_CC_BY_40,
    'CC0-10': LICENSE_CC0_10,
    'PD-10': LICENSE_PD_10,
    'CC-BY-SA-20' : LICENSE_CC_BY_SA_20,
}

IMAGE_TYPES = ( '*.tif', '*.jpg' )

# http://mdproc.library.upenn.edu:9292/records/9915808403503681/show?format=openn


PREPARATION_METHODS = [
    {
        'tag': 'pih',
        'description': "Uses metadata scraped from Penn in Hand to build metadata for the object. Requires bibid.txt file containing the object's BibID",
        'name': 'Penn in Hand Prep',
        'package_validation': {
            'valid_names': ['*.tif', 'bibid.txt', 'holdingid.txt', 'keywords.txt'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', 'bibid.txt'],
        },
        'prep_class': {
            'class_name': 'openn.prep.medren_prep.MedrenPrep',
            'params': {
                'pih_host': 'mdproc.library.upenn.edu:9292',
                'pih_path': '/records/{0}/create?format=openn',
                'xsl': os.path.join(SITE_ROOT, 'xsl/pih2tei.xsl'),
                'encoding_desc': os.path.join(BIBLIO_PHILLY_KEYWORDS_DIR, 'bibliophilly-keywords.xml'),
            },
        },
    },
    {
        'tag': 'pagesxlsx',
        'description': "Uses metadata scraped from MARC XML and extracts metadata from a spreadsheet to build metadata for the object. Requires bibid.txt or description.xml file and page.xlsx file.",
        'name': 'Manuscripts of the Muslim World Prep',
        'package_validation': {
            'valid_names': ['*.tif', 'bibid.txt', 'holdingid.txt', 'marc.xml', 'pages.xlsx', 'keywords.txt'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', 'pages.xlsx'],
        },
        'prep_class': {
            'class_name': 'openn.prep.mmw_prep.MMWPrep',
            'params': {
                'pih_host': 'mdproc.library.upenn.edu:9292',
                'pih_path': '/records/{0}/create?format=marc21',
                'xsl': os.path.join(SITE_ROOT, 'xsl/pih2tei.xsl'),
                'merge_pages_xsl': os.path.join(SITE_ROOT, 'xsl/merge_marc_pages.xsl'),
                'config_json': os.path.join(SITE_ROOT, 'muslimworld.json'),
            },
        },
    },
    {
        'tag': 'diaries',
        'description': "Extracts metadata from PACSCL Diaries spreadsheet to build metadata for the object. Requires valid openn_metadata.xslx file.",
        'name': 'PACSCL Diaries Prep',
        'package_validation': {
            'valid_names': ['*.tif', '*.jpg', 'openn_metadata.xlsx'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.xlsx'],
        },
        'prep_class': {
            'class_name': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
            'params' : {
                'image_rights': {
                    'dynamic': True,
                },
                'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json'),
                'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
            },
        },
    },
    {
        'tag': 'bphil',
        'description': """Extracts metadata from Biblio-Philly spreadsheet to build metadata for the
            object. Requires valid openn_metadata.xslx file.""",
        'name': 'Biblio Philly Prep',
        'package_validation': {
            'valid_names': ['*.tif', '*.jpg', 'openn_metadata.xlsx'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.xlsx'],
        },
        'before_scripts': [
            [os.path.join(SITE_ROOT, '..', 'scripts', 'get-bibliophilly-keywords.sh'), BIBLIO_PHILLY_KEYWORDS_DIR]
        ],
        'prep_class': {
            'class_name': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
            'params' : {
                'image_rights': {
                    'dynamic': False,
                },
                'config_json': os.path.join(SITE_ROOT, 'bibliophilly.json'),
                'xsl': os.path.join(SITE_ROOT, 'xsl/bp_spreadsheet_xml2tei.xsl'),
                'encoding_desc': os.path.join(BIBLIO_PHILLY_KEYWORDS_DIR, 'bibliophilly-keywords.xml'),
            },
        },
    },
    {
        'tag': 'congs',
        'description': """Extracts metadata from Biblio-Philly spreadsheet to build metadata for the
            object for CLIR congregations grant. Requires valid openn_metadata.xslx file.""",
        'name': 'CLIR Congregations Prep',
        'package_validation': {
            'valid_names': ['*.tif', '*.jpg', 'openn_metadata.xlsx'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.xlsx'],
        },
        'prep_class': {
            'class_name': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
            'params' : {
                'image_rights': {
                    'dynamic': False,
                },
                'config_json': os.path.join(SITE_ROOT, 'bibliophilly.json'),
                'xsl': os.path.join(SITE_ROOT, 'xsl/bp_spreadsheet_xml2tei.xsl'),
            },
        },
    },
    {
        'tag': 'gzh',
        'description': """Extracts metadata from Genizah spreadsheet to build metadata for the
            object. Requires valid openn_metadata.xslx file. Uses the same XSL as 'bphil' This
            genizah.json configuration is the same as bibliophilly.json, with these exceptions:
                - Metadata Creator/Email:   not required in genizah.json
                - Subject: keywords:        not required in genizah.json
                - Scribe information:       added in genizah.json
                - Provenance Details:       repeatable in genizah.json
                - Date requirements:        looser in genizah.json

                """,
        'name': 'Genizah Prep',
        'package_validation': {
            'valid_names': ['*.tif', '*.jpg', 'openn_metadata.xlsx'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*', '.DS_Store'],
            'required_names': ['*.xlsx'],
        },
        'prep_class': {
            'class_name': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
            'params' : {
                'image_rights': {
                    'dynamic': False,
                },
                'config_json': os.path.join(SITE_ROOT, 'genizah.json'),
                'xsl': os.path.join(SITE_ROOT, 'xsl/bp_spreadsheet_xml2tei.xsl'),
            },
        },
    },
    {
        'tag': 'dirlesstei',
        'description': """Directory-less TEI prep: Does not process a directory; add the
folder name to the database; requires a TEI file.""",
        'name': 'Directory-less TEI prep',
        'process_directory': False,
        'package_validation': {
            'valid_names': ['TEI.xml'],
            'required_names': ['TEI.xml'],
        },
        'prep_class': {
            'class_name': 'openn.prep.dirless_tei_prep.DirlessTEIPrep',
            'params' : {
            },
        },
    },

]

# On 'no-document' repositories: These are repositories for which OPenn lists
# no documents. The Walters Art Museum is one such repository. Listing of
# documents is handled by the site itself.
REPOSITORIES = {
    'validations': {
        'unique_fields': [
            'tag',
            'name',
            'include_file',
        ],
        'required_fields': [
            'tag',
            'live',
            'name',
            'blurb',
            'include_file',
            'metadata_type',
        ],
    },
    'configs': [
        {
            'tag': 'pennmss',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'University of Pennsylvania Libraries',
            'blurb': """With approximately 250,000 printed books and nearly ten million
pieces of manuscript material, the Rare Book and Manuscript Library is
a small part of the University's 5 million-volume library system.
Special strengths include American literature, drama, and history;
English, Spanish, Italian, and German literature; the Edgar Fahs Smith
Memorial Collection in the history of chemistry; the Horace Howard
Furness Memorial Library devoted to Shakespeare and his
contemporaries; and the Henry Charles Lea Library with strengths in
Church history, the Inquisition, magic, and witchcraft.""",
            'include_file': 'PennManuscripts.html',
        },
        {
            'tag': 'ljs',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'University of Pennsylvania Libraries, Lawrence J. Schoenberg Manuscripts',
            'blurb': """These manuscripts are from the Lawrence J. Schoenberg collection in
the Rare Books and Manuscripts Library at the University of
Pennsylvania. With its emphasis on the history of science and the
transmission of knowledge across time and geography, the Schoenberg
Collection of about 300 manuscripts brings together many of the great
scientific and philosophical traditions of the ancient and medieval
worlds. Documenting the extraordinary achievements of scholars,
philosophers, and scientists active in pre-modern Europe, Africa, and
Asia, the collection illuminates the foundations of our shared
intellectual heritage.""",
            'include_file': 'LJSchoenbergManuscripts.html',
        },
        {
            'tag': 'bates',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'University of Pennsylvania School of Nursing, Barbara Bates Center',
            'blurb': """The Barbara Bates Center for the Study of the History of Nursing is the
largest repository for primary source materials and rare books about the
history of nursing. The Center holds an extensive collection of
materials from 19th to the 20th century hospital based nursing schools,
visiting nurse societies and the personal papers of nursing leaders.
Contained in the collections are over 3000 books, rare books, glass
slides, photographs, audio tapes, and films, as well as a smaller amount
of artifact holdings. The Center's collections are approximately 2300
linear feet.""",
            'include_file': 'BatesCenter.html',
        },
        {
            'tag': 'brynmawr',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Bryn Mawr College, Special Collections',
            'blurb': """The Bryn Mawr College Special Collections includes rare books,
manuscripts, the college archives, works of art on paper, and
ethnographic and archaeological objects. The rare book collection
contains approximately 50,000 volumes, and includes extensive
collections of late medieval and early modern works, among them more
than 100 medieval manuscript volumes and more than 1000 15th century
printed books. These collections are supported by a graphics
collection ranging from the 15th century to the present, including
7,300 prints, 3,500 drawings, and 13,000 vintage photographs.""",
            'include_file': 'BrynMawrCollege.html',
        },
        {
            'tag': 'lasalle',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'La Salle University, Department of Special Collections',
            'blurb': """The Department of Special Collections in the Connelly Library houses a
diverse range of materials, from 15th century illuminated devotionals to
subject collections treating contemporary social issues. Bodies of work
include literature, music, films, art, archival material and ephemera.
The collections explore a variety of themes in aural, narrative and
illustrative form. Special Collections maintains a focus on acquiring,
cataloging and housing unique material that is tied to undergraduate
pedagogy and is freely available to researchers. The Department of
Special Collections is a proud member of the Philadelphia Area
Consortium of Special Collections Libraries.""",
            'include_file': 'LaSalleUniversity.html',
        },
        {
            'tag': 'chf',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Science History Institute, Othmer Library',
            'blurb': """The Science History Institute's Donald F. and Mildred Topp Othmer
Library of Chemical History collects, preserves, and makes accessible
materials relating to the history of science, technology, and medicine
with an emphasis on chemical and material sciences and technologies from
ancient to modern times. The Othmer Library was founded in 1988 when Dr.
and Mrs. Othmer announced their challenge grant to be given for the
creation of a library which would work to preserve the history of the
chemical sciences. The Othmer Library now houses approximately 160,000
print and microform volumes, rare books & manuscripts, significant
archival materials, and historical photographs of great value to
researchers and our cultural heritage. Together these collections form
an unrivaled resource for the history of chemistry and related sciences,
technologies, and industries.""",
            'include_file': 'SciHistoryInstitute.html',
        },
        {
            'tag': 'cpp',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'College of Physicians of Philadelphia, The Historical Medical Library',
            'blurb': """Established in 1788, the Historical Medical Library was Philadelphia's
central medical library for over 150 years, serving its medical schools,
hospitals, physicians and other health professionals. Today, it is an
independent research library devoted to the history of medicine and the
medical humanities, serving hundreds of scholars, health professionals,
students and popular writers each year.""",
            'include_file': 'CollegeOfPhysicians.html',
        },
        {
            'tag': 'columbia',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Columbia University, Rare Book & Manuscript Library',
            'blurb': u"""The Libraries at Columbia are at the heart of the University. The
collections serve the research needs of the Columbia faculty,
undergraduate and graduate students, and the community, while providing
a wealth of items for the use of scholars from around the world. The
Rare Book and Manuscript Library, largest of Columbia's repositories for
the special collections of the University, holds collections spanning
more than 4,000 years, from cuneiform tablets to born-digital objects.
Some 600,000 printed books and 17 miles of manuscripts, personal papers,
and records form the core of the RBML holdings, along with well over one
million photographs, prints and drawings, maps, coins, scientific
instruments, playing cards, theater set models and other realia, and
audio and moving image materials. The collections cover a broad range of
subjects, and provide researchers with a great depth of material to
study. RBML holds important early manuscripts and printed books in
Arabic, Latin, Greek, Hebrew, and a wide variety of other languages.
Particular collecting strengths include the history of English and
American literature, journalism, finance and economics, mathematics and
astronomy, printing and publishing, theater and the performing arts,
photography, American history, Russian and East European Emigré history
and culture, Hebraica and Judaica, and Latino arts and activism. RBML is
home to one of the oldest oral history collections in the country, and
is also the repository for archives that support the mission of the
Center for Human Rights Documentation and Research.
""",
            'include_file': 'ColumbiaUniversity.html',
        },
        {
            'tag': 'amphilsoc',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'American Philosophical Society',
            'blurb': """The American Philosophical Society (APS), the oldest learned society in
the United States, was founded in 1743 by Benjamin Franklin for the
purposes of "promoting useful knowledge." In the 21st century, it serves
to advance knowledge and promote scholarship in the humanities and
social, mathematical, life, and physical sciences. The APS Library and
Museum's collections make it among the premier institutions for
documenting and exhibiting the history of the American Revolution and
founding, the history of science from Newton to NASA, Native American
languages and culture, and the development of American anthropology. The
Library houses over 13 million manuscripts, 275,000 volumes and bound
periodicals, and 250,000 images, fine art and other objects.""",
            'include_file': 'AmericanPhilosophicalSociety.html',
        },
        {
            'tag': 'burke',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Columbia University, The Burke Library at Union Theological Seminary',
            'blurb': """The mission of Columbia University's Burke Library at Union Theological
Seminary is to identify, acquire, organize, provide access to,
interpret, and preserve for the future information in the field of
theology and related areas of the humanities and social sciences. One of
the largest theological libraries in North America, its holdings of over
700,000 items include numerous western medieval and Renaissance
manuscripts, as well as Greek, Hebrew, Arabic, Turkish, Armenian,
Ethiopic, and Syriac materials. The collection of Syriac manuscripts in
one of the largest in this hemisphere.""",
            'include_file': 'BurkeLibrary.html',
        },
        {
            'tag': 'manchester',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'University of Manchester Library, Special Collections',
            'blurb': """The University of Manchester Library's manuscripts and archives are
internationally important. Their subject range is extraordinarily
diverse and the collections span many centuries, from the 3rd millennium
BCE to the 21st century. European manuscripts include hundreds of
medieval codices, and there are major collections of Arabic, Persian,
Turkish and Hebrew manuscripts. The Library holds the archives of
hundreds of companies, trade unions, charities, social organizations and
religious institutions, as well as individuals. Our rare book
collections are amongst the finest in the world. They encompass almost
all the landmarks of printing through five centuries, including
magnificent illustrated books. Highlights include: over 4,000
incunables; a remarkable collection of 16th-century Italian books; one
of the greatest collections in the world covering the entire history of
the printed Bible; internationally important collections of French
Revolutionary material, Nonconformist literature, and scientific and
medical texts. The Library's significant Visual Collection comprises:
paintings, drawings, photographs, sculptures, textiles, ceramics, glass,
archives, manuscripts, prints, papers, illustrated and painted books,
and associated objects. Dating from the ancient world to the present,
its representation of visual culture is excellent, of international
scope, importance and interest.""",
            'include_file': 'UniversityOfManchester.html',
        },
        {
            'tag': 'christchurch',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Christ Church Philadelphia',
            'blurb': """Founded in 1695, Christ Church was the first Anglican church to be
established in Pennsylvania. This fulfilled the provision outlined by
King Charles II in the charter he granted to William Penn in 1681
stipulating that if twenty individuals requested an Anglican clergyman
the Bishop of London would appoint one. Accordingly, thirty-nine
Philadelphians came together in 1695 to form Christ Church. Located on
Second Street, just north of Market Street the Church transitioned from
a small frame structure in its early years to the imposing Georgian
structure built from 1727-1754 that still stands on the site today.
Members of the Continental Congress and early government officials
worshipped here and seven signers of the Declaration of Independence are
buried on Church property. When the congregation grew too large to be
accommodated here the vestry built St. Peter's at the southern edge of
the city in 1760 and later St. James. Those United Churches remained a
unit until the 1820s and 1830s. Christ Church is an active Episcopal
parish today as well as a major historic site. The records consist of
vestry minutes, parish records, accounting and financial records, deeds,
architectural drawings, photographs, and audiovisual materials. In
addition, there are materials from parish organizations and affiliated
institutions such as Christ Church Hospital, Episcopal School, Christ
Church Burial Ground, and Christ Church Preservation Trust. A detailed
finding aid is available on-site.""",
            'include_file': 'ChristChurch.html',
        },
        {
            'tag': 'stthomas',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'African Episcopal Church of St. Thomas',
            'blurb': """The African Episcopal Church of St. Thomas was an outgrowth of the
African Church of Philadelphia founded in 1792 by the Free African
Society, a mutual aid organization, established in 1787 by Absalom Jones
and Richard Allen for the purpose of encouraging religion and literacy,
and providing destitute members--especially widows and orphans-- with
financial assistance. Absalom Jones led the congregation and became the
first African American admitted to Holy Orders in the Episcopal Church
when Bishop William White ordained him a deacon in 1796 and a priest in
1802. Richard Allen formed Mother Bethel African Methodist Episcopal
Church which became a separate Methodist denomination. Records consist
of vestry minutes, pew rents, birth and baptismal records, as well as
some records of the Free African Society.""",
            'include_file': 'StThomas.html',
        },
        {
            'tag': 'stgeorges',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Saint George\'s United Methodist Church of Philadelphia',
            'blurb': """Historic St. George's United Methodist Church of Philadelphia is the
oldest Methodist Church in America. Located in Philadelphia, the church
was founded by Captain Thomas Webb and the Methodist Society of
Philadelphia in 1769 for the purpose of practicing the Methodist
religion. In December of 1769, Joseph Pilmore, a missionary of John
Wesley, held the first prayer meeting at the church followed later by
Thomas Coke and Bishop Francis Asbury. Bishop Asbury was the first
pastor of St. George's United Methodist Church and ordained as many as
35 ministers in the Methodist faith within America during his travels.
Two African Americans, Richard Allen and Absalom Jones, licensed as lay
preachers of Methodism, eventually left the church because of racial
tensions and formed two new congregations. Richard Allen formed Mother
Bethel African Methodist Episcopal Church. Absalom Jones turned to the
Episcopal faith and established St. Thomas' African Episcopal Church.
St. George's is known as "the church that moved the bridge," as the
Benjamin Franklin Bridge was rerouted in the 1920s so the church would
not be demolished by its construction. St. George's records consist of
conference letters; account books; baptism, death, and marriage records;
as well as journals, diaries, etc.""",
            'include_file': 'StGeorge.html',
        },
        {
            'tag': 'mikvehisrael',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Congregation Mikveh Israel',
            'blurb': """Congregation Mikveh Israel (officially Kahal Kadosh Mikveh Israel) is
also known as the "Synagogue of the American Revolution." The oldest
Congregation in Philadelphia, Mikveh Israel was informally established
by religious-minded Jews in British America during the 1740s, and has
become the second-oldest surviving Congregation in the United States. In
Pennsylvania, and Philadelphia in particular, Jews found an environment
of tolerance for their religious beliefs and traditions made possible by
William Penn's "great experiment." By 1775 a community of 300 strong
existed in a city of 35,000. Among items in the archives of Congregation
Mikveh Israel are letters written by George Washington and Abraham
Lincoln, and a public subscription list for the 1782 building signed by
Benjamin Franklin, David Rittenhouse, and other civic leaders.""",
            'include_file': 'MikvehIsrael.html',
        },
        {
            'tag': 'americanbaptist',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'American Baptist Historical Society',
            'blurb': """As the oldest Baptist historical organization (founded in 1835), the
American Baptist Historical Society serves as guardian of the largest
and most diverse collection of Baptist historical material worldwide,
including the archives of the American Baptist Churches, USA, the
American Baptist Home Mission Societies, the American Baptist Foreign
Mission Society/International Ministries, as well as other affiliated
agencies and some pan-Baptist organizations. The Society holds
unparalleled resources on African American Baptists, the modern
missionary movement, women's work, and the social gospel movement. Its
manuscript collections include more than 1,200 collections of personal
papers of missionaries, pastors, and other notable Baptists. The
Society's Samuel Colgate Baptist Historical Library comprises over
40,000 volumes.""",
            'include_file': 'AmericanBaptistHistoricalSociety.html',
        },
        {
            'tag': 'gloriadei',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Gloria Dei Church',
            'blurb': '''In the 17th century Swedish settlers landed on the banks of the Delaware
River establishing churches in Wilmington, Tinicum and by the mid-17th
century in Wicaco outside of what would become Philadelphia. That latter
church, Gloria Dei, is Pennsylvania's oldest congregation. The existing
church was built between 1698 and 1700 and originally served a Swedish
Lutheran congregation. The church today is part of the Episcopal Diocese
and a national historic site. Archival records scanned as part of this
project include vestry minutes, registers, financial correspondence
between the original Swedish parishes and the churches in Philadelphia,
Delaware and New Jersey as well as their "miscellaneous records."''',
            'include_file': 'GloriaDeiChurch.html',
        },
        {
            'tag': 'episcopaldiocese',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Episcopal Diocese of Pennsylvania Archives',
            'blurb': """Following the American Revolution, American Anglicans led by the
Reverend William White came together to form the Episcopal Diocese of
Pennsylvania which once covered the entire Commonwealth. In 1865 and
1871 new dioceses were formed out of the Diocese of Pennsylvania. Today
the Diocese of Pennsylvania covers Philadelphia, Bucks, Montgomery,
Chester and Delaware counties. The Archives are the official repository
for records of the administration of the Diocese, parishes that have
closed and histories of the Diocese, spanning the period from 1784 to
the present. Records included in this project are the founding minutes
of the Diocese and selected records of St. Paul's Episcopal Church.""",
            'include_file': 'EpiscopalDiocese.html',
        },
        {
            'tag': 'stpeters',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'St. Peter\'s Church of Philadelphia',
            'blurb': """In 1758 the vestry of Christ Church authorized the construction of a new
chapel at Third and Pine Streets to accomodate its members living in the
southern section of the city. St. Peter's Church and Christ Church
shared the same vestry, ministers, and records and until they formally
separated in 1832 were known as the United Churches of Christ Church and
St. Peter's. The formal separation agreement stipulated that records
created prior to 1832 were to be maintained by Christ Church so
researchers looking for pre-1832 information should check Christ
Church's collections. Records created after 1832 are maintained by St.
Peter's, an active parish. Scanned for this project are minutes, pew
rents and registers.""",
            'include_file': 'StPeters.html',
        },
        {
            'tag': 'presbyterian',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Presbyterian Historical Society',
            'blurb': """Organized in 1852, the Presbyterian Historical Society in Philadelphia
is the oldest denominational archives in the United States. PHS serves
as the national archives of the Presbyterian Church (U.S.A.) and exists
to collect, preserve, and share the story of the American Presbyterian
and Reformed experience with Presbyterians, the scholarly community, and
the general public. The society's holdings include over 30,000 cubic
feet of records from congregations, presbyteries, and synods from across
the country, and from national agencies charged with overseeing
Presbyterian mission work both in the United States and abroad. The PHS
collection also includes personal papers and a library of over 250,000
titles germane to Reformed history from the sixteenth century to the
present.""",
            'include_file': 'PresbyterianHistoricalSociety.html',
        },
        {
            'tag': 'drexarc',
            'name': 'Drexel University, Archives and Special Collections',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """
The Drexel University Archives and Special Collections acquires,
preserves and makes available records, manuscripts, visual materials
and publications related to the history of Drexel University. The
Archives has material related to Drexel's founders as well as Drexel
students, faculty, academic departments, administrative offices, and
campus organizations. The Special Collections house rare books and
manuscript collections, with a focus on incunabula; the history of
printing and fine press; the history of Philadelphia; the Drexel
family; and the history of education.""",
            'include_file': 'DrexelUniversity.html',
        },
        {
            'tag': 'drexmed',
            'name': "Drexel University College of Medicine, Legacy Center",
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The Drexel University College of Medicine Legacy Center supports
research and investigation of the history of women in medicine,
history of homeopathic medicine in the United States, and the history
of women's health. The Center is the repository for records
documenting the history of the College and its predecessor
institutions, including the Woman's Medical College of Pennsylvania
and Hahnemann University. Over 4,000 linear feet of materials date
from 1502 to the present, with the bulk of the materials ranging from
1848-1990.""",
            'include_file': 'DrexelMedicine.html',
        },
        {
            'tag': 'haverford',
            'name': 'Haverford College, Quaker and Special Collections',
            'metadata_type': 'TEI',
            'live': True,
            'blurb':  """Quaker & Special Collections contains Haverford College's
world-renowned Quaker Collection, College archives, rare books and
manuscripts, and fine art. The world-renowned Quaker collections
illuminate Quaker life, faith, and practice from the earliest days of
the Society of Friends to the present day and in many parts of the
world. Archival holdings document the history and operations of
Haverford College from its founding in 1833 to present. Other
strengths include literature, natural history, science, American
History, and a small but interesting collection of 13th through
19th-century illuminated manuscripts in Hebrew, Latin, and Arabic. The
collections are open to all.""",
            'include_file': 'HaverfordCollege.html',
        },
        {
            'tag': 'lehigh',
            'name': 'Lehigh University Libraries, Special Collections',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """Lehigh University Libraries' Special Collections serves as the
repository for the University's collections of rare books and
manuscripts as well as for holdings relating to Lehigh's institutional
and cultural history. The catalog encompasses over 40,000 volumes,
including first editions of English and American literature from the
seventeenth to the nineteenth centuries and represents diverse topics
such as travel and exploration, natural history, and ornithology. A
special focus on the history of science and technology includes an
expansive assortment of material related to large-scale construction and
the use of iron and steel in industrial life, as well as a collection of
classic and seminal works relating to bridge building and design.
University materials include official documents and publications of the
school administration, papers and publications of faculty members,
theses and dissertations composed by graduate students, and memorabilia
from the broad spectrum of campus life.""",
            'include_file': 'LehighUniversity.html',
        },
        {
            'tag': 'tlc',
            'name': 'The Library Company of Philadelphia',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The Library Company of Philadelphia is an independent research library
specializing in American history and culture from the 17th through the
19th centuries. Open to the public free of charge, the Library Company
houses an extensive non-circulating collection of rare books,
manuscripts, broadsides, ephemera, prints, photographs, and works of
art.""",
            'include_file': 'LibraryCompany.html',
        },
        {
            'tag': 'libpa',
            'name': 'State Library of Pennsylvania, Rare Collections Library',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The State Library of Pennsylvania collects and preserves the
written heritage of the Commonwealth through materials published for,
by, and about Pennsylvania. The strengths of the Rare Collections
Library include Pennsylvania imprints, government documents, original
newspapers, pamphlets, maps and atlases, and rare works of
Pennsylvania religion, natural history, and genealogy.""",
            'include_file': 'StateLibraryOfPennsylvania.html',
        },
        {
            'tag': 'loc',
            'name': 'Library of Congress',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """Today's Library of Congress is an unparalleled world resource. The
enormous size and variety of its collections make it the largest library
in the world. The collection of more than 168 million items includes
more than 39 million catalogued books and other print materials in 470
languages; more than 72 million manuscripts; the largest rare book
collection in North America; and the world's largest collection of legal
materials, films, maps, sheet music and sound recordings.""",
            'include_file': 'LibraryOfCongress.html',
        },
        {
            'tag': 'friendshl',
            'name': 'Swarthmore College, Friends Historical Library',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """Established in 1871 at Swarthmore College, two years after the College
opened, the Friends Historical Library documents the history of the
Religious Society of Friends (Quakers) from their mid-seventeenth
century origins to the present. As the largest Quaker library in the
world, it includes materials on women's suffrage, the rights of Native
Americans, the anti-slavery movement, social activism, and the peace
movement.""",
            'include_file': 'FriendsHistoricalLibrary.html',
        },
        {
            'tag': 'huntington',
            'name': 'The Huntington Library',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The Huntington Library is one of the largest and most complete research
libraries in the United States in its fields of specialization. The
Library's collection of rare books, manuscripts, prints, photographs,
maps, and other materials in the fields of British and American history
and literature totals more than nine million items. OPenn hosts one item
from The Huntington Library, the *Autobiography of Benjamin
Franklin,(Autograph manuscript signed), 1771-1789.*""",
            'include_file': 'HuntingtonLibrary.html',
        },
        {
            'tag': 'hsp',
            'name': 'Historical Society of Pennsylvania',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The collections of Historical Society of Pennsylvania range from
genealogical and family papers to business and organizational records
to collections of items such as photographs, postcards, sheet music,
menus, and trade cards.  HSP's library contains a wealth of published
material, including books, pamphlets, serials, and newspapers.  Our
collections span from the seventeenth through the twenty-first
centuries, and they touch upon numerous topics, from social and
economic issues during the nation's founding to the effects of the
Industrial Revolution to the immigrant experience of recent decades.
While our collections generally focus on Philadelphia, Eastern
Pennsylvania, and the greater Delaware Valley, we also have books from
other states East of the Mississippi River, maps from different parts
of the world, and manuscripts from national and international
leaders.""",
            'include_file': 'HistoricalSocietyOfPennsylvania.html',
        },
        {
            'tag': 'lts',
            'name': 'Lutheran Archives Center at Philadelphia',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The Lutheran Archives Center at Philadelphia is the Northeast Regional
Archives (Region 7) for the Evangelical Lutheran Church in America
(ELCA). It carries on the work of its predecessors in the first
Lutheran Church organization in America, the Evangelical Lutheran
Ministerium of Pennsylvania and Adjacent States, founded on August 15,
1748 by Henry Melchior Muhlenberg. The archives was recognized as a
part of the church organization in 1792. Collections include personal
papers of Lutheran clergy, theologians, and church workers; archives
of church organizations; and records of congregations.""",
            'include_file': 'LutheranTheologicalSeminary.html',
        },
        {
            'tag': 'ulp',
            'name': 'Abraham Lincoln Foundation of The Union League of Philadelphia',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The Abraham Lincoln Foundation of The Union League of Philadelphia
(ALF) is the steward of an important collection of art, archives,
manuscripts, books, pamphlets, objects and other historic documents
related to both the Union League and the Civil War.  The collections
include materials from the ALF, The
Union League of Philadelphia, The Civil War Museum of Philadelphia,
The Military Order of The Loyal Legion of the United States and The
Dames of the Loyal Legion of the United States. The collections are
available for research through The Heritage Center of the Union
League. """,
            'include_file': 'UnionLeagueOfPhiladelphia.html',
        },
        {
            'tag': 'private1',
            'name': 'Private Collection A',
            'metadata_type': 'custom',
            'live': True,
            'blurb': """Documents from a private collection: the Archimedes Palimpsest and the
Galen Syriac Palimpsest. Data and metadata from both are available
under a Creative Commons Attribution License.""",
            'include_file': 'PrivateCollectionA.html',
        },
        {
            'tag': 'ism',
            'name': 'Independence Seaport Museum, J. Welles Henderson Archives and Library',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """Independence  Seaport Museum's J. Welles Henderson Archives and
Library is one of the nation's premier regional maritime research
facilities. With a rich repository of regional documents, 12,000 ship
plans, a significant collection of rare books and manuscripts; maps
and charts; photographs, and a 15,000 volume research library, the J.
Welles Henderson Archives and Library boasts an impressive range of
materials. The collections are dedicated to a deeper understanding,
appreciation, and experience of Philadelphia's regional waterways and
the Delaware watershed area for everyone. They carry national and
international significance.""",
            'include_file': 'IndependenceSeaportMuseum.html',
        },
        {
            'tag': 'gsp',
            'name': 'German Society of Pennsylvania',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """Founded in 1764, The German Society of Pennsylvania is America's
oldest German organization. Its Joseph P. Horner Memorial Library,
housed in a beautiful 19th century reading room, holds one of the
largest private collections of German-language books in the U.S. The
German American Collection contains a wealth of material documenting
all aspects of German American life, beginning with the first settlers
in Germantown in 1683. In addition to books, the library houses
sizable collections of 19th century Philadelphia German newspapers,
periodicals, pamphlets, and manuscripts.""",
            'include_file': 'GermanSociety.html',
        },
        {
            'tag': 'pennmuseumarchives',
            'name': 'University of Pennsylvania Museum of Archaeology and Anthropology, Archives',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The Penn Museum Archives is the institutional repository of the Penn
Museum and the work for its archaeologists and anthropologists. The
collections include 2,500 feet of records; these records document the
Museum's archaeological expeditions to every inhabited continent, the
history of the Penn Museum, and the history of the practices of
archaeology and anthropology. Further, we hold three-quarters of a
million images and nearly one thousand reels of film.""",
            'include_file': 'PennMuseumArchives.html',
        },
        {
            'tag': 'uarc',
            'name': 'University of Pennsylvania Archives and Records Center',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The University Archives and Records Center (UARC) serves the
University community as a center for research, teaching and learning
as well as center for the storage and management of inactive
University records. The Trustees of the University of Pennsylvania
established the University Archives and Records Center in 1945 and
approved records management programs in 1954 and 1990. UARC's
collections include a broad range of historically significant
materials from the first paper records created by the Trustees in 1749
to the millions of electronic records of the present. These materials
document the University's corporate or organizational origin and
development as well as the many activities and achievements of its
officers, staff, faculty, students, alumni, and benefactors. UARC's
collections policies also extend beyond the institution itself and
embrace the history of prominent persons associated with the
University; the history of institutions of higher learning in the
United States; the history of American intellectual life generally;
and the history of the Philadelphia community in which the University
lives. The collections consist of more than 14,000 cubic feet of
records in many different formats, including visual archives and
three-dimensional memorabilia.""",
            'include_file': 'UniversityArchives.html',
        },
        {
            'tag': 'pennmuseum',
            'name': 'University of Pennsylvania Museum of Archaeology and Anthropology',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """Founded in 1887, the Penn Museum has always been one of the world's
great archaeology and anthropology research museums, and the largest
university museum in the United States. With roughly one million
objects in its care, the Penn Museum encapsulates and illustrates the
human story.""",
            'include_file': 'PennMuseum.html',
        },
        {
            'tag': 'tdw',
            'name': 'The Walters Art Museum',
            'metadata_type': 'walters-tei',
            'live': True,
            'blurb': """The Walters Art Museum in Baltimore, Maryland is internationally
renowned for its collection of art. This collection presents an
overview of world art from pre-dynastic Egypt to 20th-century Europe,
and counts among its many treasures Greek sculpture and Roman
sarcophagi; medieval ivories and Old Master paintings; Art Nouveau
jewelry and 19th-century European and American masterpieces. With more
than 900 illuminated manuscripts, this extraordinary collection
chronicles the art of the book over more than 1,000 years. Items in
the collection are from all over the world, and from ancient to modern
times. It features deluxe Gospel books from Armenia, Ethiopia,
Byzantium, and Ottonian Germany; French and Flemish books of hours; as
well as masterpieces of Safavid, Mughal and Ottoman manuscript
illumination.""",
            'include_file': 'TheDigitalWalters.html',
            'no_document': True,
        },
        {
            'tag': 'kislak',
            'name': 'University of Miami, Jay I. Kislak Collection',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """Since its arrival in 2018, the Jay I. Kislak Collection of the Early
Americas, Exploration and Navigation has transformed the University of
Miami and its Libraries. The Kislak Collection at the University of
Miami includes an assembly of rare books, manuscripts, maps,
photographs, and artifacts that convey a multifaceted history of the
Americas, hemispheric cultural encounters, and global exploration
beginning with Native American cultures and extending to modern times.""",
            'include_file': 'KislakFoundation.html',
        },
        {
            'tag': 'flp',
            'name': 'Free Library of Philadelphia, Special Collections',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """With more than 6 million visits to its 54 locations and 9 million online
visits annually, the Free Library is one of Philadelphia's most widely
used educational and cultural institutions. The Free Library's Special
Collections feature music, maps, drawings, photographs, fine art prints,
and one of the largest rare book collections in an American public
library. The Rare Book Department houses thousands of illuminated
pre-modern manuscripts and cuttings; first editions and manuscripts of
important American and British writers, including some of the largest
collections of Charles Dickens and Edgar Allan Poe; early American
children's books and original artworks by children's illustrators;
hundreds of incunables; and books, manuscripts, and maps relating to the
discovery, exploration, and settlement of the Americas. """,
            'include_file': 'FreeLibraryOfPhiladelphia.html',
        },
        {
            'tag': 'pma',
            'name': 'Philadelphia Museum of Art',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The Philadelphia Museum of Art houses a world-renowned collection in a
landmark building. Highlights of the collection include: the largest and
most importnat collection of works by Marcel Duchamp; the greatest
collection of sculpture by Constantin Brancusi outside Europe. The
finest public collection of Auguste Rodin's sculpture in the United
States; superb Impressionist and Post-Impressionist paintings by Edouard
Manet, Claude Monet, Pierre-Auguste Renoir, Camille Pissarro and Edgar
Degas; exceptional American painting, sculpture, furniture, silver, and
ceramics that reflect Philadelphia's central role in American history;
and extraordinary "period rooms" and architectural ensembles from around
the world.  The museum's landmark building, opened in 1928 at the
western end of Benjamin Franklin Parkway. The other buildings that make
up its campus include the Perelman Building, the Rodin Museum, and the
two great eighteenth-century houses in Fairmount Park, Mount Pleasant
and Cedar Grove.""",
            'include_file': 'PhiladelphiaMuseumOfArt.html',
        },
        {
            'tag': 'udel',
            'name': 'University of Delaware Library',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """Special Collections at the University of Delaware Library collects,
preserves, and makes accessible rare and unique materials such as rare
books, artists' books, fine press books, manuscripts and archives.  The
Special Collections have four main collecting areas in literature, art,
history and Delawareana, and science and technology.""",
            'include_file': 'UniversityOfDelaware.html',
        },
        {
            'tag': 'britlib',
            'name': 'British Library',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The British Library is the national library of the United Kingdom and
gives access to the world's most comprehensive research collection. The
collection of over 170 million items includes artifacts from every age
of written civilization.""",
            'include_file': 'BritishLibrary.html',
        },
        {
            'tag': 'temple',
            'name': 'Temple University Libraries, Special Collections Research Center',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The Special Collections Research Center (SCRC) is the principal
repository for and steward of the Libraries' rare books, manuscripts,
archives and University records.  The SCRC collects, preserves, and
makes accessible primary resources and rare or unique materials, to
stimulate, enrich, and support research, teaching, learning, and
administration at Temple University.  SCRC makes these resources
available to a broad constituency as part of the University's engagement
with the larger community of scholars and independent researchers.""",
            'include_file': 'TempleUniversity.html',
        },
        {
            'tag': 'villanova',
            'name': 'Villanova University Libraries, Special Collections',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """Villanova University Special Collections houses approximately 15,000
items. Some of these items are rare or unique and most require special
handling and preservation. Collections include Augustiniana, the DiOrio
Theater collection, European imprints to 1800, the Hubbard collection,
incunabula, limited editions, the McGarrity Collection, manuscripts, the
Mendel Collection, North American imprints to 1864, the Reap World War
II collection, the Sherman Thackara collection and Villanovana.""",
            'include_file': 'VillanovaUniversity.html',
        },
        {
            'tag': 'fandm',
            'name': 'Franklin & Marshall College Library, Archives & Special Collections',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The Archives & Special Collections at Franklin & Marshall College
Library organizes, preserves, and promotes the visual and written record
of the college, faculty and student scholarship, and the digital and
special collections of the library. Collections include German-American
imprints, manuscripts and rare books, posters, maps, prints, newspapers
and photographs, as well as the permanent historical record of Franklin
& Marshall College and its related institutions: Franklin College,
Marshall College, and Franklin and Marshall Academy.""",
            'include_file': 'FranklinMarshallCollege.html',
        },
        {
            'tag': 'rosenbach',
            'name': 'Free Library of Philadelphia, The Rosenbach',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The Rosenbach seeks to foster inquiry, learning and creative thought by
engaging audiences in programs, exhibitions, and research inspired by
our collections of nearly 400,000 rare books, manuscripts, and fine and
decorative art objects, including some of the best-known literary and
historical objects in the world. In December 2013, the Rosenbach became
affiliated with the Free Library of Philadelphia, bringing together two
of the world's preeminent collections of rare books, manuscripts,
Americana and art. The combined holdings of the Rosenbach and the Free
Library of Philadelphia inspire unique exhibitions and programs
throughout the year.""",
            'include_file': 'Rosenbach.html',
        },
        {
            'tag': 'hmml',
            'name': 'The Hill Museum & Manuscript Library (HMML)',
            'metadata_type': 'custom',
            'live': True,
            'blurb': """The Hill Museum & Manuscript Library (HMML), located at Saint John's
University in Collegeville, Minnesota, holds the world's largest archive
of manuscript photographs in both microfilm and digital format. HMML
identifies manuscript collections around the world that need
photographic preservation. HMML's archives now contain more than 300,000
complete manuscripts, ranging in size from large codices of hundreds of
folios to brief documents consisting of just a few leaves. Hosted on
OPenn is a palimpsest leaf from HMML, SJU MS Frag 32.""",
        'include_file': 'HMML.html',
        },
    ],
}

PREP_CONFIGS = {
    'penn-pih': {
        'repository': {
            'tag': 'pennmss',
        },
        "image_types": ['*.tif'],
        'repository_prep': {
            'tag': 'pih',
        },
        'rights': {
            'image_rights': 'PD',
            'metadata_rights': 'CC-BY-40'
        },
    },
    'penn-pagesxlsx': {
        'repository': {
            'tag': 'pennmss'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'pagesxlsx',
            'params': {
                'required_xpaths': [
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="b"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="a"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="e"]',
                ]
            },
        },
        'rights': {
            'image_rights': 'PD',
            'metadata_rights': 'CC-BY-40'
        },
    },
    'ljs-pih': {
        'repository': {
            'tag': 'ljs'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'pih',
        },
        'rights': {
            'holder': 'The University of Pennsylvania Libraries',
            'image_rights': 'PD',
            'metadata_rights': 'CC-BY-40'
        },
    },
    'pennmuseum-pih': {
        'repository': {
            'tag': 'pennmuseum'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'pih',
        },
        'rights': {
            'image_rights': 'CC-BY-SA-20',
            'metadata_rights': 'CC-BY-40'
        },
    },
    'penn-diaries': {
        'repository': {
            'tag': 'pennmss'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'bates-diaries': {
        'repository': {
            'tag': 'bates'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'brynmawr-diaries': {
        'repository': {
            'tag': 'brynmawr'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'drexarc-diaries': {
        'repository': {
            'tag': 'drexarc'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'drexmed-diaries': {
        'repository': {
            'tag': 'drexmed'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'haverford-diaries': {
        'repository': {
            'tag': 'haverford'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'lehigh-diaries': {
        'repository': {
            'tag': 'lehigh'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'friendshl-diaries': {
        'repository': {
            'tag': 'friendshl'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'hsp-diaries': {
        'repository': {
            'tag': 'hsp'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
     'huntington-diaries': {
        'repository': {
            'tag': 'huntington'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'lts-diaries': {
        'repository': {
            'tag': 'lts'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'ulp-diaries': {
        'repository': {
            'tag': 'ulp'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'tlc-diaries': {
        'repository': {
            'tag': 'tlc'
        },
        "image_types": [ '*.tif' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'libpa-diaries': {
        'repository': {
            'tag': 'libpa'
        },
        "image_types": [ '*.tif', '*.jpg' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'ism-diaries': {
        'repository': {
            'tag': 'ism'
        },
        "image_types": [ '*.tif', '*.jpg' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'uarc-diaries': {
        'repository': {
            'tag': 'uarc'
        },
        "image_types": [ '*.tif', '*.jpg' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'gsp-diaries': {
        'repository': {
            'tag': 'gsp'
        },
        "image_types": [ '*.tif', '*.jpg' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'private1-dirlesstei': {
        'repository': {
            'tag': 'private1',
        },
        'repository_prep': {
            'tag': 'dirlesstei',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'pennmuseumarchives-diaries': {
        'repository': {
            'tag': 'pennmuseumarchives'
        },
        "image_types": [ '*.tif', '*.jpg' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'flp-bphil': {
        'repository': {
            'tag': 'flp'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'lasalle-bphil': {
        'repository': {
            'tag': 'lasalle'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'britlib-gzh': {
        'repository': {
            'tag': 'britlib'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["The Polonsky Foundation"],
        'repository_prep': {
            'tag': 'gzh',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'loc-bphil': {
        'repository': {
            'tag': 'loc'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'pennmuseum-bphil': {
        'repository': {
            'tag': 'pennmuseum'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'CC-BY-SA-20',
            'metadata_rights': 'CC-BY-40',
        }
    },
    'brynmawr-bphil': {
        'repository': {
            'tag': 'brynmawr'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'haverford-bphil': {
        'repository': {
            'tag': 'haverford'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'udel-bphil': {
        'repository': {
            'tag': 'udel'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'temple-bphil': {
        'repository': {
            'tag': 'temple'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'villanova-bphil': {
        'repository': {
            'tag': 'villanova'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'fandm-bphil': {
        'repository': {
            'tag': 'fandm'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'pma-bphil': {
        'repository': {
            'tag': 'pma'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'pma-bphil-nofunder': {
        'repository': {
        'tag': 'pma'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'rosenbach-bphil': {
        'repository': {
            'tag': 'rosenbach'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'chf-bphil': {
        'repository': {
            'tag': 'chf'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'lehigh-bphil': {
        'repository': {
            'tag': 'lehigh'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'tlc-bphil': {
        'repository': {
            'tag': 'tlc'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'cpp-bphil': {
        'repository': {
            'tag': 'cpp'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'cchurch-congs': {
        'repository': {
            'tag': 'christchurch'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'congs',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'stpeters-congs': {
        'repository': {
            'tag': 'stpeters'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'congs',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'stgeorges-congs': {
        'repository': {
            'tag': 'stgeorges'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'congs',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'stthomas-congs': {
        'repository': {
            'tag': 'stthomas'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'congs',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'mikvehisrael-congs': {
        'repository': {
            'tag': 'mikvehisrael'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'congs',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'gloriadei-congs': {
        'repository': {
            'tag': 'gloriadei'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'congs',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'americanbaptist-congs': {
        'repository': {
            'tag': 'americanbaptist'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'congs',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'presb-congs': {
        'repository': {
            'tag': 'presbyterian'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'congs',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'episc-congs': {
        'repository': {
            'tag': 'episcopaldiocese'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'congs',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'flp-mmw': {
        'repository': {
            'tag': 'flp'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'pagesxlsx',
            'params': {
                'required_xpaths': [
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="b"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="a"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="e"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="u"]',
                    '//marc:datafield[@tag="035"]/marc:subfield[@code="a" and starts-with(., "(PLF)")]',
                ]
            },
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'tlc-rush': {
        'repository': {
            'tag': 'tlc'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'pagesxlsx',
            'params': {
                'required_xpaths': [
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="b"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="a"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="e"]',
                ]
            },
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'columbia-mmw': {
        'repository': {
            'tag': 'columbia'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'pagesxlsx',
            'params': {
                'required_xpaths': [
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="b"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="a"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="e"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="u"]',
                    '//marc:datafield[@tag="035"]/marc:subfield[@code="a" and starts-with(., "(NNC)")]',
                ]
            },
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'haverford-mmw': {
        'repository': {
            'tag': 'haverford'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'pagesxlsx',
            'params': {
                'required_xpaths': [
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="b"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="a"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="e"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="u"]',
                    '//marc:datafield[@tag="035"]/marc:subfield[@code="a" and starts-with(., "(PHC)")]',
                ]
            },
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'brynmawr-mmw': {
        'repository': {
            'tag': 'brynmawr'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'pagesxlsx',
            'params': {
                'required_xpaths': [
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="b"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="a"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="e"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="u"]',
                ]
            },
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'ljs-mmw': {
        'repository': {
            'tag': 'ljs'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'pagesxlsx',
            'params': {
                'required_xpaths': [
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="b"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="a"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="e"]',
                ]
            },
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'penn-mmw': {
        'repository': {
            'tag': 'pennmss'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'pagesxlsx',
            'params': {
                'required_xpaths': [
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="b"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="a"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="e"]',
                ]
            },
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'pennmuseum-mmw': {
        'repository': {
            'tag': 'pennmuseum'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'pagesxlsx',
            'params': {
                'required_xpaths': [
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="b"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="a"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="e"]',
                ]
            },
        },
        'rights': {
            'image_rights': 'CC-BY-SA-20',
            'metadata_rights': 'CC-BY-40',
        }
    },
    'burke-mmw': {
        'repository': {
            'tag': 'burke'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'pagesxlsx',
            'params': {
                'required_xpaths': [
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="b"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="a"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="e"]',
                    '//marc:datafield[@tag="852"]/marc:subfield[@code="u"]',
                    '//marc:datafield[@tag="035"]/marc:subfield[@code="a" and starts-with(., "(NNC)")]',
                ]
            },
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'friendshl-bphil': {
        'repository': {
            'tag': 'friendshl'
        },
        "image_types": ['*.tif', '*.jpg'],
        "funders": ["Council on Library and Information Resources"],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'amphilsoc-bphil': {
        'repository': {
            'tag': 'amphilsoc'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC0-10',
        }
    },
    'manchester-bphil': {
        'repository': {
            'tag': 'manchester'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'CC-BY',
            'metadata_rights': 'CC-BY',
        }
    },
    'kislak-bphil': {
        'repository': {
            'tag': 'kislak'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'bphil',
        },
        'rights': {
            'image_rights': 'PD-10',
            'metadata_rights': 'CC-BY',
        }
    },
    'penn-gzh': {
        'repository': {
            'tag': 'pennmss'
        },
        "image_types": ['*.tif', '*.jpg'],
        'repository_prep': {
            'tag': 'gzh',
        },
        'rights': {
            'image_rights': 'CC-BY',
            'metadata_rights': 'CC-BY',
        }
    },
    'pennmuseum-diaries': {
        'repository': {
            'tag': 'pennmuseum'
        },
        "image_types": [ '*.tif', '*.jpg' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
    'hmml-dirlesstei': {
        'repository': {
            'tag': 'hmml',
        },
        'repository_prep': {
            'tag': 'dirlesstei',
        },
        'rights': {
            'image_rights': 'dynamic',
            'metadata_rights': 'dynamic',
        }
    },
}

CURATED_COLLECTIONS = {
    'validations': {
        'unique_fields': [
            'tag',
            'name',
        ],
        'required_fields': [
            'tag',
            'live',
            'name',
            'blurb',
            'csv_only',
        ],
    },
    'configs': [
        {
            'tag': 'bibliophilly',
            'name': 'Bibliotheca Philadelphiensis',
            'blurb': """This collection, when completed, will include digital editions of more
than 400 western European medieval and early modern codices, plus
selected leaves and cuttings, from the collections of Philadelphia Area
Consortium of Special Collections Libraries (PACSCL) member libraries.
This collections is funded by the Council on Library and Information
Resources.""",
            'csv_only': False,
            'include_file': 'BiblioPhilly.html',
            'live': True,
        },
        {
            'tag': 'pacscl-diaries',
            'name': 'PACSCL Diaries',
            'blurb': """The PACSCL Diaries Project will allow researchers an intimate view into
a wide variety of personalities, largely from Philadelphia, as they went
about their daily lives and commented on the world around them. The
project will ultimately provide an online archive of diaries drawn from
PACSCL member collections. OPenn currently hosts a pilot group of 53
diary volumes.""",
            'csv_only': False,
            'include_file': 'PACSCLDiaries.html',
            'live': True,
        },
        {
            'tag': 'muslimworld',
            'name': 'Manuscripts of the Muslim World',
            'blurb': """This collection will include digital editions of more than 500
manuscripts and 827 paintings from the Islamicate world broadly
construed. Together these holdings represent in great breadth the
flourishing intellectual and cultural heritage of Muslim lands from 1000
to 1900, covering mathematics, astrology, history, law, literature, as
well as the Qur'an and Hadith. The bulk of the collection consists of
manuscripts in Arabic and Persian, along with examples of Coptic,
Samaritan, Syriac, Turkish, and Berber. The primary partners are
Columbia University, the Free Library of Philadelphia, and the
University of Pennsylvania with signifiant contributions from Bryn Mawr
College and Haverford College. This collection is funded by the Council
on Library and Information Resources.""",
            'csv_only': False,
            'include_file': 'MuslimWorld.html',
            'live': True,
        },
        {
            'tag': 'kislakcurated',
            'name': 'Jay I. Kislak Digital Library of the Americas',
            'blurb': """Over the course of many decades, Jay I. Kislak (1922-2018) built a
collection of primary source material - rare books, manuscripts, maps,
photographs, and artifacts that convey the multifaceted history of the
Americas, hemispheric cultural encounters, and global exploration
beginning with Native American cultures and extending to modern times.
In 2004, the Jay I. Kislak Foundation donated more than 3,000 items from
this collection to the Library of Congress where they are available for
scholarly research. Beginning in 2016 the Kislak Foundation, in
partnership with the University of Miami and Miami Dade College,
established a Kislak Center on each campus along with a gift of 2,500
books, manuscripts, and historic objects. The Kislak-MDC-UM partnership
includes exhibitions, research, education, and public outreach programs
that will serve MDC and UM students and faculty, the local communicty,
and a global network of engaged scholars. The Jay I. Kislak Digital
Library of the Americas aims to unite the materials from all of these
institutions to tell a compelling story about early American history and
culture.""",
            'csv_only': False,
            'include_file': 'KislakLibraryOfAmericas.html',
            'live': True,
        },
        {
            'tag': 'medicalhub',
            'name': 'For the Health of the New Nation: Philadelphia as the Center of American Medical Education, 1746-1868',
            'blurb': """This initiative will digitize, describe, an provide access to 140,000
pages of lecture tickets, course schedules, theses, dissertations,
student notes, faculty lecture notes, commencement addresses, opening
addresses, and matriculation records from Philadelphia, 1746-1868. The
project will emphasize not only the voices of the medical greats, but
also the often unheard voices of students and others. Project parters
for this initiative are The College of Physicians of Philadelphia; The
Legacy Center, Drexel University College of Medicine; University of
Pennsylvania Libraries; Pennsylvania Hospital Historic Collections; The
Library Company of Philadelphia; American Philosophical Society; Thomas
Jefferson University Archives and Special Collections; and Philadelphia
Area Consortium of Special Collections Libraries (PACSCL).""",
            'csv_only': False,
            'include_file': 'HealthOfTheNewNation.html',
            'live': True,
        },
        {
            'tag': 'indic',
            'name': 'Collection of Indic Manuscripts',
            'blurb': """Penn Libraries holds more than 3,000 manuscripts from South Asia, making
it one of the largest collections of its kind in the Americas.
Predominantly Indic in provenance, the manuscripts are chiefly Sanskrit
works written in Devanāgarī script. Though generally informed by
traditional Hindu learning, the collection nevertheless remains
thematically comprehensive and contains significant Buddhist and Jain
texts.""",
            'csv_only': False,
            'include_file': 'IndicCurated.html',
            'live': True,
        },
        {
            'tag': 'congregations',
            'name': 'Digitizing Philadelphia\'s Historic Congregations',
            'blurb': """The churches and synagogues of Philadelphia were gathering places in the
18th and 19th centuries and their records reflect the changing
political, social and cultural mores. More than 40,000 scanned images
from vestry and trustee minutes, baptismal, birth, marriage and death
records, pew rents, accounting records, sermons and correspondence gives
researchers opportunities to explore these connections. Collaborating
institutions include Christ Church, St. George's Methodist Church,
Gloria Dei, Mikveh Israel, African Episcopal Church of St. Thomas,
Episcopal Diocese of Pennsylvania Archives, Presbyterian Historical
Society, St. Peter's Episcopal Church and American Baptist Historical
Society. This project is funded by the Council on Library and
Information Resources.""",
            'csv_only': False,
            'include_file': 'Congregations.html',
            'live': True,
        },
        {
            'tag': 'genizah',
            'name': 'Cairo Genizah',
            'blurb': """In the late 1990s, thanks to a significant gift from a Penn alum named
Jeffrey Keil, W' 65 and PAR '91, Penn initiated a project, in
collaboration with Cambridge University Libraries, to apply digital
technologies to discover new intellectual matches among physically
dispersed Cario genizah fragments. Through this initiative it was
demonstrated how digital technologies may serve as discovery tools to
identify matches among a global diaspora of thousands of fragments of
medieval manuscripts (see:
http://sceti.library.upenn.edu/genizah/index.cfm). This collection of
Cairo genizah fragments consists of Penn manuscripts that were part of
this project.""",
            'csv_only': False,
            'include_file': 'CairoGenizah.html',
            'live': True,
        },
        {
            'tag': 'thai',
            'name': 'Thai Manuscripts',
            'blurb': 'Lorem ipsum',
            'csv_only': True,
            'live': True,
        },
    ],
}

PREP_CONTEXT = {
    'archive_dir': ARCHIVE_DIR,
    'package_dir': PACKAGE_DIR,
    'staging_dir': STAGING_DIR,
    'licences': LICENSES,
    'deriv_configs': DERIV_CONFIGS,
}

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
            'fenced-code-blocks': None,
            'toc': None,
        },
        "safe_mode": "escape",
    },
    "trusted": {
        "extras": {
            "code-friendly": None,
        },
        "safe_mode": False,
    }
}
