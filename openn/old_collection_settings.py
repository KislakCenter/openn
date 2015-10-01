COLLECTIONS_OLD = {
    'medren': {
        'tag': 'medren',
        'name': 'Penn Manuscripts',
        'blurb': 'These manuscripts are from the collections of the Rare Books and Manuscripts Library at the University of Pennsylvania or are hosted by Penn with the permission of their owners.  Penn holds over 2,000 Western manuscripts produced before the 19th century; medieval and Renaissance manuscripts comprise approximately 900 items, the earliest dating from 1000 A.D. The medieval manuscripts, now a collection of approximately 250 items, have been considered and used as a research collection since the private library of church historian Henry Charles Lea came to the University in the early 20th century. Most of the manuscripts are in Latin, but the medieval vernacular languages of Middle English, Middle French, Italian, Spanish, German, Dutch, and Judaeo-Arabic are each represented by one or more manuscripts. The collection is particularly strong in the fields of church history and history of science, with secondary strengths in liturgy and liturgical chant, theology and philosophy, and legal documents.',
        'toc_file': 'PennManuscripts.html',
        'include_file': 'PennManuscripts.html',
        'web_dir': 'Data/PennManuscripts',
        'html_dir': 'Data/PennManuscripts/html',
        'prep_class': 'openn.prep.medren_prep.MedrenPrep',
        'live': True,
        'package_validation': {
            'valid_names': ['*.tif', 'bibid.txt'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', 'bibid.txt'],
        },
        'config' : {
            'host': 'dla.library.upenn.edu',
            'path': '/dla/medren/pageturn.xml?id=MEDREN_{0}',
            'xsl': os.path.join(SITE_ROOT, 'xsl/pih2tei.xsl'),
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
    'ljs': {
        'tag': 'ljs',
        'name': 'Lawrence J. Schoenberg Manuscripts',
        'live': True,
        'blurb': 'These manuscripts are from the Lawrence J. Schoenberg collection in the Rare Books and Manuscripts Library at the University of Pennsylvania.',
        'toc_file': 'LJSchoenbergManuscripts.html',
        'web_dir': 'Data/LJSchoenbergManuscripts',
        'html_dir': 'Data/LJSchoenbergManuscripts/html',
        'prep_class': 'openn.prep.medren_prep.MedrenPrep',
        'package_validation': {
            'valid_names': ['*.tif', 'bibid.txt'],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', 'bibid.txt'],
        },
        'config' : {
            'host': 'dla.library.upenn.edu',
            'path': '/dla/medren/pageturn.xml?id=MEDREN_{0}',
            'xsl': os.path.join(SITE_ROOT, 'xsl/pih2tei.xsl'),
            'image_rights': {
                'Marked': 'False',
                'WebStatment': 'http://creativecommons.org/publicdomain/mark/1.0/',
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
    'brynmawr' : {
        'tag': 'brynmawr',
        'name': 'Special Collections, Bryn Mawr College',
        'live': False,
        'blurb': 'Documents from Special Collections, Bryn Mawr College.',
        'toc_file': 'BrynMawrCollege.html',
        'web_dir': 'Data/BrynMawrCollege',
        'html_dir': 'Data/BrynMawrCollege/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
            'rights_statements': {
                'images': {
                    'dynamic': True,
                },
                'metadata': {
                    'dynamic': True,
                },
            },
        },
    },
    'drexarc' : {
        'tag': 'drexarc',
        'name': 'Drexel University Archives',
       'live': False,
        'blurb': 'Documents from Drexel University Archives.',
        'toc_file': 'DrexelUniversity.html',
        'web_dir': 'Data/DrexelUniversity',
        'html_dir': 'Data/DrexelUniversity/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'drexmed' : {
        'tag': 'drexmed',
        'name': 'Legacy Center Archives & Special Collection, Drexel University College of Medicine.',
        'live': False,
        'blurb': 'Documents from the Legacy Center Archives & Special Collection, Drexel University College of Medicine.',
        'toc_file': 'DrexelMedicine.html',
        'web_dir': 'Data/DrexelMedicine',
        'html_dir': 'Data/DrexelMedicine/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'haverford' : {
        'tag': 'haverford',
        'name': 'Quaker and Special Collections, Haverford College',
        'live': False,
        'blurb': 'Documents from Quaker and Special Collections, Haverford College.',
        'toc_file': 'HaverfordCollege.html',
        'web_dir': 'Data/HaverfordCollege',
        'html_dir': 'Data/HaverfordCollege/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'lehigh' : {
        'tag': 'lehigh',
        'name': 'Special Collections, Lehigh University',
        'live': False,
        'blurb': 'Documents from Special Collections, Lehigh University.',
        'toc_file': 'SpecialCollectionsLehighUniversity.html',
        'web_dir': 'Data/SpecialCollectionsLehighUniversity',
        'html_dir': 'Data/HaverfordCollege/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'tlc' : {
        'tag': 'tlc',
        'name': 'The Library Company of Philadelphia',
        'live': False,
        'blurb': 'Documents from the Library Company of Philadelphia.',
        'toc_file': 'LibraryCompany.html',
        'web_dir': 'Data/LibraryCompany',
        'html_dir': 'Data/LibraryCompany/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'libpa' : {
        'tag': 'libpa',
        'name': 'Rare Collections Library, State Library of Pennsylvania',
        'live': False,
        'blurb': 'Documents from the Rare Collections Library, State Library of Pennsylvania.',
        'toc_file': 'StateLibraryOfPennsylvania.html',
        'web_dir': 'Data/StateLibraryOfPennsylvania',
        'html_dir': 'Data/StateLibraryOfPennsylvania/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'friendshl' : {
        'tag': 'friendshl',
        'name': 'Friends Historical Library, Swarthmare College',
        'live': False,
        'blurb': 'Documents from the Friends Historical Library, Swarthmare College.',
        'toc_file': 'FriendsHistoricalLibrary.html',
        'web_dir': 'Data/FriendsHistoricalLibrary',
        'html_dir': 'Data/FriendsHistoricalLibrary/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'hsp' : {
        'tag': 'hsp',
        'name': 'Historical Society of Pennsylvania',
        'live': False,
        'blurb': 'Documents from the Historical Society of Pennsylvania.',
        'toc_file': 'HistoricalSocietyOfPennsylvania.html',
        'web_dir': 'Data/HistoricalSocietyOfPennsylvania',
        'html_dir': 'Data/HistoricalSocietyOfPennsylvania/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'lts' : {
        'tag': 'lts',
        'name': 'Lutheran Theological Seminary',
        'live': False,
        'blurb': 'Documents from Lutheran Theological Seminary.',
        'toc_file': 'LutheranTheologicalSeminary.html',
        'web_dir': 'Data/LutheranTheologicalSeminary',
        'html_dir': 'Data/LutheranTheologicalSeminary/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
    'ulp' : {
        'tag': 'ulp',
        'name': 'Union League of Philadelphia',
        'live': False,
        'blurb': 'Documents from the Union League of Philadelphia.',
        'toc_file': 'UnionLeagueOfPhiladelphia.html',
        'web_dir': 'Data/UnionLeagueOfPhiladelphia',
        'html_dir': 'Data/UnionLeagueOfPhiladelphia/html',
        'prep_class': 'openn.prep.spreadsheet_prep.SpreadsheetPrep',
        'prep_class_kwargs': {
            'config_json': os.path.join(SITE_ROOT, 'pacscl_diaries.json')
        },
        'package_validation': {
            'valid_names': ['*.tif', '*.xlsx' ],
            'invalid_names': ['CaptureOne', 'Output', '*[()]*'],
            'required_names': ['*.tif', '*.xlsx'],
        },
        'config' : {
            'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
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
        },
    },
}
