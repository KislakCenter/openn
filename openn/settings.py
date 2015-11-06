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
SITE_DIR = os.environ['OPENN_SITE_DIR']

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
            'name': 'Lutheran Theological Seminary',
            'metadata_type': 'TEI',
            'live': True,
            'blurb': """While the Krauth Memorial Library has over 193,000 volumes, the Rare
Book Collection includes 8,000 volumes, fifteen incunabula, three
Books of Hours, and twenty-five cuneiform tablets. Collection
strengths are the 16th-century Lutheran Reformation, Continental
Pietism, 18th-century works in theology ad philosophy, liturgical
studies, and 19th-century American Lutheran periodicals.""",
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
include materilas from the ALF, The
Union League of Philadelphia, The Civil War Museum of Philadelphia,
The Military Order of The Loyal Legion of the United States and The
Dames of the Loyal Legion of the United States. The collections are
available for research through The Heritage Center of the Union
League. """,
            'include_file': 'UnionLeagueOfPhiladelphia.html',
        },
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
    'penn-diaries': {
        'collection': {
            'tag': 'pennmss'
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
    },
    'tlc-diaries': {
        'collection': {
            'tag': 'tlc'
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
    'libpa-diaries': {
        'collection': {
            'tag': 'libpa'
        },
        "image_types": [ '*.tif', '*.jpg' ],
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
