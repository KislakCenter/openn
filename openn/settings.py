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
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci',
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
PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))

TIME_ZONE = 'US/Eastern'
USE_TZ = True

OPENN_HOST = 'openn.library.upenn.edu'

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


PREPARATION_METHODS = [
    {
        'tag': 'pih',
        'description': "Uses metadata scraped from Penn in Hand to build metadata for the object. Requires bibid.txt file containing the object's BibID",
        'name': 'Penn in Hand Prep',
        'package_validation': {
            'valid_names': ['*.tif', 'bibid.txt'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', 'bibid.txt'],
        },
        'prep_class': {
            'class_name': 'openn.prep.medren_prep.MedrenPrep',
            'params': {
                'pih_host': 'dla.library.upenn.edu',
                'pih_path': '/dla/medren/pageturn.xml?id=MEDREN_{0}',
                'xsl': os.path.join(SITE_ROOT, 'xsl/pih2tei.xsl'),
            },
        },
    },
    {
        'tag': 'diaries',
        'description': "Extracts metadata from PACSCL Diaries spreadsheet to build metadata for the object. Requires valid openn_metadata.xslx file.",
        'name': 'PACSCL Diaries Prep',
        'package_validation': {
            'valid_names': ['*.tif', '*.jpg', '*.xlsx'],
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
            'valid_names': ['*.tif', '*.jpg', '*.xlsx'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.xlsx'],
        },
        'before_scripts': [
            [os.path.join(SITE_ROOT, '..', 'scripts', 'get-bibliophilly-keywords.sh')]
        ],
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
        'tag': 'dirlesstei',
        'description': """Directory-less TEI prep: Does not process a directory; add the
folder name to the database; requires a TEI file.""",
        'name': 'Directory-less TEI prep',
        'process_directory': False,
        'package_validation': {
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
            'name': 'University of Pennsylvania Books & Manuscripts',
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
            'name': 'Lawrence J. Schoenberg Manuscripts',
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
            'tag': 'brynmawr',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Bryn Mawr College Library Special Collections',
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
            'tag': 'manchester',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'The University of Manchester Library Special Collections',
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
            'tag': 'drexarc',
            'name': 'Drexel University Archives and Special Collections',
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
            'name': "Legacy Center, Drexel University College of Medicine",
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
            'name': 'Quaker and Special Collections, Haverford College',
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
            'name': 'Special Collections, Lehigh University Library',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """Lehigh University Special Collections serves as the repository for the
University's collections of rare books and manuscripts, and for
holdings relating to its own history. It encompasses a rare book
collection of over 25,000 volumes, with first editions of English and
American literature from the 17th to the 19th centuries, strengths in
travel and exploration, natural history and ornithology, and works of
historical significance in science and technology. Materials relating
to the University include documents and publications of the
University, papers of faculty members, and memorabilia from the
University's history. Special Collections also holds manuscripts and
personal papers, in addition to papers relating to the University's
history.""",
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
            'name': 'Rare Collections Library of the State Library of Pennsylvania',
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
            'tag': 'friendshl',
            'name': 'Friends Historical Library, Swarthmore College',
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
and literature totals more than nine million items. The Library
collections date from the Middle Ages to the 21st century. The greatest
concentration is in the English Renaissance, about 1500 to 1641; other
strengths include medieval manuscripts, incunabula (books printed before
1501), maps, travel literature, British and American history and
literature, the American Southwest, and the history of science, medicine
and technology.""",
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
            'name': 'J. Welles Henderson Archives and Library of the Independence Seaport Museum',
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
            'name': 'Penn Museum Archives',
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
            'name': 'University Archives and Records Center, University of Pennsylvania',
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
        'common_prep': {
            'image_rights': {
                'dynamic': True,
            },
            'rights_statements': {
                'images': {
                    'dynamic': True,
                },
                'metadata': {
                    'dynamic': True,
                },
            },
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
    'pennmuseum-diaries': {
        'repository': {
            'tag': 'pennmuseum'
        },
        "image_types": [ '*.tif', '*.jpg' ],
        'repository_prep': {
            'tag': 'diaries',
        },
        'common_prep': {
            'image_rights': {
                'dynamic': True,
            },
            'rights_statements': {
                'images': {
                    'dynamic': True,
                },
                'metadata': {
                    'dynamic': True,
                },
            },
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
            'blurb': """Documents from the Biblitheca Philadelphiensis Project,
                        funded by the Council on Library and Information Resources.""",
            'csv_only': False,
            'include_file': 'BiblioPhilly.html',
            'live': True,
        },
        {
            'tag': 'pacscl-diaries',
            'name': 'PACSCL Diaries',
            'blurb': """The PACSCL Diaries Project will allow researchers an intimate view into a
                        wide variety of personalities, largely from Philadelphia, as they went about their
                        daily lives and commented on the world around them. The project will
                        ultimately provide an online archive of diaries drawn from PACSCL member
                        collections. OPenn currently hosts a pilot group of 53 diary volumes.""",
            'csv_only': False,
            'include_file': 'PACSCLDiaries.html',
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
