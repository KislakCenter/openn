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
COLLECTIONS_TEMPLATE = 'Collections.html'

STAGING_DIR = os.environ['OPENN_STAGING_DIR']
PACKAGE_DIR = os.environ['OPENN_PACKAGE_DIR']
ARCHIVE_DIR = os.environ['OPENN_ARCHIVE_DIR']

TOC_DIR = 'html'

LICENCES = {
    'CC-BY': {
        'metadata': u'Metadata is ©{year} {holder} and licensed under a Creative Commons Attribution License version 4.0 (CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/legalcode. For a description of the terms of use see the Creative Commons Deed https://creativecommons.org/licenses/by/4.0/. {more_information}',
        'image': u'Images are  ©{year} {holder} and licensed under a Creative Commons Attribution License version 4.0 (CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/legalcode. For a description of the terms of use see the Creative Commons Deed https://creativecommons.org/licenses/by/4.0/. {more_information}',
        'single_image': u'This image of {title} is ©{year} {holder} and licensed under a Creative Commons Attribution License version 4.0 (CC-BY-4.0 https://creativecommons.org/licenses/by/4.0/legalcode. For a description of the terms of use see the Creative Commons Deed https://creativecommons.org/licenses/by/4.0/. {more_information}',

        'legalcode_url': 'https://creativecommons.org/licenses/by/4.0/legalcode',
        'deed_url': 'https://creativecommons.org/licenses/by/4.0/'
        },
    'CC0': {
        'metadata': u'To the extent possible under law, {holder} has waived all copyright and related or neighboring rights to this metadata about {title}. This work is published from: United States. For a summary of CC0, see https://creativecommons.org/publicdomain/zero/1.0/. Legal code: https://creativecommons.org/publicdomain/zero/1.0/legalcode.  {more_information}',
        'image': u'To the extent possible under law, {holder} has waived all copyright and related or neighboring rights to these images and the content of {title}. This work is published from: United States. For a summary of CC0, see https://creativecommons.org/publicdomain/zero/1.0/. Legal code: https://creativecommons.org/publicdomain/zero/1.0/legalcode. {more_information}',
        'single_image': u'To the extent possible under law, {holder} has waived all copyright and related or neighboring rights to this image and the content of {title}. This work is published from: United States. For a summary of CC0, see https://creativecommons.org/publicdomain/zero/1.0/. Legal code: https://creativecommons.org/publicdomain/zero/1.0/legalcode. {more_information}',
        'legalcode_url': 'https://creativecommons.org/publicdomain/zero/1.0/legalcode',
        'deed_url': 'https://creativecommons.org/publicdomain/zero/1.0/'
    },
    'PD': {
        'metadata': u'This metadata about {title} is free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/. {more_information}',
        'image':  u'These images and the content of {title} are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/. {more_information}',
        'single_image':  u'This image and the content of {title} are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/. {more_information}',
        'legalcode_url': 'http://creativecommons.org/publicdomain/mark/1.0/',
        'deed_url': 'http://creativecommons.org/publicdomain/mark/1.0/'
    },
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
    }
]

COLLECTIONS = {
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
            'blurb': """These documents are from the collections of the Rare Books and
Manuscripts Library at the University of Pennsylvania or are hosted by
Penn with the permission of their owners.  Penn holds over 2,000
Western manuscripts produced before the 19th century; medieval and
Renaissance manuscripts comprise approximately 900 items, the earliest
dating from 1000 A.D. The medieval manuscripts, now a collection of
approximately 250 items, have been considered and used as a research
collection since the private library of church historian Henry Charles
Lea came to the University in the early 20th century. Most of the
manuscripts are in Latin, but the medieval vernacular languages of
Middle English, Middle French, Italian, Spanish, German, Dutch, and
Judaeo-Arabic are each represented by one or more manuscripts. The
collection is particularly strong in the fields of church history and
history of science, with secondary strengths in liturgy and liturgical
chant, theology and philosophy, and legal documents.""",
            'include_file': 'PennManuscripts.html',
        },
        {
            'tag': 'ljs',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Lawrence J. Schoenberg Manuscripts',
            'blurb': 'These manuscripts are from the Lawrence J. Schoenberg collection in the Rare Books and Manuscripts Library at the University of Pennsylvania.',
            'include_file': 'LJSchoenbergManuscripts.html',
        },
        {
            'tag': 'brynmawr',
            'metadata_type': 'TEI',
            'live': True,
            'name': 'Bryn Mawr College Library Special Collections',
            'blurb': """The Bryn Mawr College Special Collections includes rare books,
manuscripts, the college archives, works of art on paper, and
ethnographic and archaeological objects.  The rare book collection
contains approximately 50,000 volumes, and includes extensive
collections of late medieval and early modern works, among them more
than 100 medieval manuscript volumes and more than 1000 15th century
printed books.  In addition, there are strong collections on the
history of women, European interaction with Asia, Africa and the
Americas, and British and American literature.<br /><br />

The manuscript collections are particularly strong in women's history,
including the papers of Bryn Mawr president and early women's rights
activist M. Carey Thomas; papers of many prominent women associated
with Bryn Mawr, including poet Marianne Moore, New Yorker editor
Katharine Sergeant White, artist Anne Truitt, and archaeologists Lucy
Shoe Meritt and Dorothy Burr Thompson; and extensive collections of
letters and diaries written by Bryn Mawr students from the time of its
founding in the 1880s.  These collections are supported by a graphics
collection ranging from the 15th century to the present, including
7,300 prints, 3,500 drawings, and 13,000 vintage photographs.Documents
from Special Collections, Bryn Mawr College.""",
            'include_file': 'BrynMawrCollege.html',
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
family; and the hsitory of education.""",
            'include_file': 'DrexelUniversity.html',
        },
        {
            'tag': 'drexmed',
            'name': "Legacy Center, Drexel University College of Medicine",
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """
The Drexel University College of Medicine Legacy Center supports
research and investigation of the history of women in medicine,
history of homeopathic medicine in the United States, and the history
of women's health. Our collections are accessible online and in our
reading room in Philadelphia. We work regularly with K-12 students and
teachers, graduate and undergraduate students, scholars, and
genealogists.<br /><br />

The Center is the repository for records documenting the history of
the College and its predecessor institutions, including Woman's
Medical College of Pennsylvania and Hahnemann University. Special
collections emerging from these institutions' unique and original
missions to educate women physicians and to teach homeopathy reflect
the activity of individuals, institutions, and organizations. Over
4,000 linear feet of materials date from 1502 to the present, with the
            bulk of the materials ranging from 1848-1990.  """,
            'include_file': 'DrexelMedicine.html',
        },
        {
            'tag': 'haverford',
            'name': 'Quaker and Special Collections, Haverford College',
            'metadata_type': 'TEI',
            'live': True,
            'blurb':  """ Quaker & Special Collections contains Haverford College's include
the world-renowned Quaker Collection, College archives, rare books and
manuscripts, and fine art. We seek to collect, preserve, and make
available materials which serve the research and teaching needs of the
Haverford community as well as the wider scholarly community. Our
world-renowned Quaker collections, which illuminate Quaker life,
faith, and practice from the earliest days of the Society of Friends
to the present day in many parts of the world. Materials include early
books and pamphlets, meeting records, organization and family papers,
journals and diaries, English and American Quaker serials, and
audio-visual materials. Archival holdings document the history and
operations of Haverford College from its founding in 1833 to
present. Other strengths include literature (particularly Shakespeare
and the work that influenced him), natural history, science, American
History, and a small but interesting collection of 13th- through
19th-century illuminated manuscripts in Hebrew, Latin, Arabic. Our
photographic holdings document the history of photography and
photographic technology, and include prints by many of the greatest
19th and 20th century photographers, while prints, paintings, and
artifacts complete the art collections. The collections are open to
all.  """,
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
University's history. In addition, Special Collections is the
repository for Lehigh theses and dissertations. Holdings in the
history of technology concentrate on large scale construction,
including a number of classic and seminal works on bridge building and
design, and construction with iron and steel. Special Collections also
holds manuscripts and personal papers, in addition to papers relating
to the University's history.""",
            'include_file': 'LehighUniversity.html',
        },
        {
            'tag': 'friendshl',
            'name': 'Friends Historical Library, Swarthmore College',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """Friends Historical Library was established at Swarthmore College
in 1871, two years after the College opened. Its collections document
the history of the Society of Friends (Quakers) and the testimonies of
Friends from the 17th century to the present. It is the largest Quaker
library in the world and it includes materials on women's suffrage,
the rights of Native Americans, the anti-slavery movement, social
activism, and the peace movement.""",
            'include_file': 'FriendsHistoricalLibrary.html',
        },
        {
            'tag': 'hsp',
            'name': 'Historical Society of Pennsylvania',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': 'Documents from the Historical Society of Pennsylvania.',
            'include_file': 'HistoricalSocietyOfPennsylvania.html',
        },
        {
            'tag': 'lts',
            'name': 'Lutheran Theological Seminary',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': 'Documents from Lutheran Theological Seminary.',
            'include_file': 'LutheranTheologicalSeminary.html',
        },
        {
            'tag': 'ulp',
            'name': 'Union League of Philadelphia',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """The Abraham Lincoln Foundation of The Union League of Philadelphia
(ALF) is the steward of an important collection of art, archives,
manuscripts, books, pamphlets, objects and other historic documents
related to both the Union League and the Civil War.  The collections
include not only the ALF's collection, but also those owned by The
Union League of Philadelphia, The Civil War Museum of Philadelphia,
The Military Order of The Loyal Legion of the United States and The
Dames of the Loyal Legion of the United States.  The collections are
available for research through The Heritage Center of the Union
League.  Additional collections of books related to American and
European history, World Wars I and II, regional history, biographies
and early 20th century travel are also available. """,
            'include_file': 'UnionLeagueOfPhiladelphia.html',
        },
# TLC does not conform to OPenn licensing terms
#         {
#             'tag': 'tlc',
#             'name': 'The Library Company of Philadelphia',
#             'metadata_type': 'TEI',
#             'live': False,
#             'blurb': 'Documents from the Library Company of Philadelphia.',
#             'include_file': 'LibraryCompany.html',
#         },
#         {

# State Library of Pennsylvania does not conform to OPenn licensing terms
#             'tag': 'libpa',
#             'name': 'Rare Collections Library of the State Library of Pennsylvania',
#             'metadata_type': 'TEI',
#             'live': False,
#             'blurb': """The State Library of Pennsylvania collects and preserves the
# written heritage of the Commonwealth through materials published for,
# by, and about Pennsylvania. The strengths of the Rare Collections
# Library include Pennsylvania imprints, government documents, original
# newspapers, pamphlets, maps and atlases, and rare works of
# Pennsylvania religion, natural history, and genealogy.<br /><br />

# The core of the Rare Collections Library is the Assembly Collection,
# numbering over 400 volumes.  These books were purchased by
# Pennsylvania's legislators beginning in 1745 to serve their needs in
# crafting legislation and governing the Commonwealth. Comprised largely
# of law books, the Assembly Collection also contains dictionaries,
# books on architecture, philosophy, history and religion. At the center
# of the Assembly Collection is the 1739 Assembly Bible, upon which
# generations of Pennsylvania's elected leaders have taken their oaths
# of office.""",
#             'include_file': 'StateLibraryOfPennsylvania.html',
#         },
    ],
}

PREP_CONFIGS = {
    'penn-pih': {
        'collection': {
            'tag': 'pennmss',
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
            'tag': 'pih',
        },
        'common_prep': {
            'image_rights': {
                'Marked': 'False',
                'WebStatement': 'http://creativecommons.org/publicdomain/mark/1.0/',
                'UsageTerms': 'This image and its content are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/.',
                'rights': 'This image and its content are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/.',
            },
            'rights_statements': {
                'images': {
                    'url': 'http://creativecommons.org/publicdomain/mark/1.0/',
                    'text': 'Unless otherwise stated, all images and their content are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for more information on terms of use, <a href="http://creativecommons.org/publicdomain/mark/1.0/">http://creativecommons.org/publicdomain/mark/1.0/</a>',
                },
                'metadata': {
                    'url': 'http://creativecommons.org/licenses/by/4.0/',
                    'text': ('Unless otherwise stated, all manuscript descriptions and other cataloging metadata are ©%d The University of Pennsylvania Libraries. They are licensed for use under a Creative Commons Attribution License version 4.0 (CC-BY-4.0 <a href="https://creativecommons.org/licenses/by/4.0/legalcode">https://creativecommons.org/licenses/by/4.0/legalcode</a>. For a description of the terms of use see the Creative Commons Deed <a href="https://creativecommons.org/licenses/by/4.0/">https://creativecommons.org/licenses/by/4.0/</a>' % (today.year, )),
                },
            },
        }
    },
    'ljs-pih': {
        'collection': {
            'tag': 'ljs'
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
            'tag': 'pih',
        },
        'common_prep': {
            'image_rights': {
                'Marked': 'False',
                'WebStatement': 'http://creativecommons.org/publicdomain/mark/1.0/',
                'UsageTerms': 'This image and its content are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/.',
                'rights': 'This image and its content are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/.',
            },
            'rights_statements': {
                'images': {
                    'url': 'http://creativecommons.org/publicdomain/mark/1.0/',
                    'text': 'Unless otherwise stated, all images and their content are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for more information on terms of use, <a href="http://creativecommons.org/publicdomain/mark/1.0/">http://creativecommons.org/publicdomain/mark/1.0/</a>',
                },
                'metadata': {
                    'url': 'http://creativecommons.org/licenses/by/4.0/',
                    'text': ('Unless otherwise stated, all manuscript descriptions and other cataloging metadata are ©%d The University of Pennsylvania Libraries. They are licensed for use under a Creative Commons Attribution License version 4.0 (CC-BY-4.0 <a href="https://creativecommons.org/licenses/by/4.0/legalcode">https://creativecommons.org/licenses/by/4.0/legalcode</a>. For a description of the terms of use see the Creative Commons Deed <a href="https://creativecommons.org/licenses/by/4.0/">https://creativecommons.org/licenses/by/4.0/</a>' % (today.year, )),
                },
            },
        },
    },
    'brynmawr-diaries': {
        'collection': {
            'tag': 'brynmawr'
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
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
    'drexarc-diaries': {
        'collection': {
            'tag': 'drexarc'
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
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
    'drexmed-diaries': {
        'collection': {
            'tag': 'drexmed'
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
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
    'haverford-diaries': {
        'collection': {
            'tag': 'haverford'
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
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
    'lehigh-diaries': {
        'collection': {
            'tag': 'lehigh'
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
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
    'friendshl-diaries': {
        'collection': {
            'tag': 'friendshl'
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
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
    'hsp-diaries': {
        'collection': {
            'tag': 'hsp'
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
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
        'collection': {
            'tag': 'lts'
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
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
    'ulp-diaries': {
        'collection': {
            'tag': 'ulp'
        },
        "image_types": [ '*.tif' ],
        'collection_prep': {
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
    }

}

PREP_CONTEXT = {
    'archive_dir': ARCHIVE_DIR,
    'package_dir': PACKAGE_DIR,
    'staging_dir': STAGING_DIR,
    'licences': LICENCES,
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
