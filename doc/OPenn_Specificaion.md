OPenn specifications
====================

OPenn is a website that provides HTTP access to image files and metadata for
digitized objects. The site supports both human and machine navigability of
all content. It does so by providing alternate methods for each type of user.

OPenn consists of image files, metadata files, and HTML pages. Image files and
metadata are accessible via links from HTML pages or by navigating exposed
directory listings.

OPenn also supports anonymous FTP and rsync protocol access.

# Terms

OPenn is structured around *items* which are members of *collections*. Each
item has a single *metadata format*. There are two types of collections:
*primary* and *secondary*. These are described below.

### Item

An OPenn **item** is a package of images and metadata of a digitized document
or other object; for example, of a medieval manuscript or print book. Each
item belongs to a single *primary collection* and may belong to one or more
*secondary collections*. Each item has a *metadata format*.

### Primary collection

An OPenn **primary collection** is a group of *items* belonging to a single
institutional collection, all having the same *metadata format*. Each primary
collection has a numeric ID; for example, `0001`, `0020`.

The scope of an institutional collection is determined by the institution. An
institution may have a single collection for all its items or choose to have
multiple primary collections. For example, the University of Pennsylvania is
represented by several collections, including 'University of Pennsylvania
Books & Manuscripts', 'Lawrence J. Schoenberg Manuscripts', and 'Penn Museum
Archives'.

Because a primary collection can only have one metadata format, in order to
present multiple metadata formats, an institution must have at least one
primary collection for each format. For example, Penn Libraries has TEI
collections for 'Lawrence J. Schoenberg Manuscripts' and 'University of
Pennsylvania Books & Manuscripts'. To have a collection with MODS metadata,
Penn Libraries would need to create a new collection for that purpose.

### Secondary collection

An OPenn **secondary collection** is a group of *items* belonging to one or
more *primary collections*. Items in a secondary collection are not required
to have the same *metadata format*. Secondary collections have unique mnemonic
tags, like 'biblio_philly' or 'pacscl_diaries'. They do not have numeric
identifiers.

Secondary collections make possible the grouping of items by topic, theme, or
project; for example, 'Penn Indic Manuscripts', 'PACSCL Diaries', 'Bibliotheca
Philadelphiensis'.

### Metadata format

An OPenn **metadata format** includes a specific implementation of a metadata
standard **and** package structure. A *metadata format* should provide
descriptive and structural metadata.

Examples: 'OPENN-TEI', 'Custom', 'WALTERS-TEI'. Note that there are two
example TEI formats, one for OPenn and one for the Walters Art Museum. While
both provide TEI P5 XML metadata, they have distinct and important
differences. They are not considered strictly compatible.

The special metadata type 'Custom' indicates that each such marked collection
or item should be investigated separately. No level of compatibility is
implied by two collections or items having the 'Custom' metadata format.

## OPenn configuration and structure

OPenn is a website configured to display directory listings. The contents of
any directory not containing an `index.html` file are displayed to users. This
is the case with the website's main page:

```
        Name                  Last modified         Size

    Collections.html         2016-11-26 18:18        16K
    Data/                    2016-05-19 18:15        -
    Projects.html            2016-11-26 18:18        16K
    ReadMe.html              2016-11-26 18:18        11K
    TechnicalReadMe.html     2016-11-26 18:18        87K
    robots.txt               2015-09-10 14:54        24
```

The `/Data` directory displays its content, and so on:

```
        Name                 Last modified          Size

    0001/                    2016-09-15 18:15        -
    0002/                    2016-12-01 18:15        -
    0003/                    2015-10-06 20:31        -
    0004/                    2015-10-06 20:31        -
    0005/                    2015-10-06 20:31        -
    0006/                    2015-10-06 20:31        -
    0007/                    2015-10-06 20:32        -
    0008/                    2015-10-06 20:31        -
    0009/                    2015-11-05 11:10        -
    0010/                    2015-11-05 19:05        -
    0011/                    2015-10-06 20:33        -
    0012/                    2015-11-05 11:12        -
    0013/                    2015-11-05 11:10        -
    ...
    collections.csv          2016-05-19 11:06       1.4K
```

The site's structure (apart from some hidden directories) can be navigated
starting with the link to the [`/Data/`][data_dir] directory. In this way it
is expected that web crawlers, including search engines, can recursively walk
the site via HTTP from the root directory.

[data_dir]: http://openn.library.upenn.edu/Data/ "/Data directory"

### Primary collections

The data directory contains the collection folders. Each collection folder has
a four-digit name (like `0001`), corresponding the collection identifier.

Each collection directory has subdirectories for items in the collection.

Example:

- [`/Data/0001/`][coll_dir] is the folder for all manuscripts from the Lawrence
  J. Schoenberg collection

[coll_dir]: http://openn.library.upenn.edu/Data/0001/ "Collection dir example"

The following diagram outlines the directory structure with collection items.

```
    Data/                          # core site data
      |--- 0001/                   # L. J. Schoenberg manuscript images
      |      |--- ljs16/           # Manuscript LJS 16
      |      |      |--- ...
      |      |--- ...
      |--- 0002/                   # Penn Books & Manuscripts images
      |      |--- mscodex1048/     # Manuscript MS Codex 1048
      |      |      |--- ...
      |      |--- ...
      |--- ...
```

Each item directory, like `ljs16` above, is organized according to its
metadata type. The contract that OPenn makes is that each OPenn collection
corresponds to a single institutional collection (as defined by the holding
institution) and all data folders have similar structure and metadata. For
example, all documents in collection '0002', Penn Books and Manuscripts, have
the same directory structure and TEI XML metadata in the same format. See the
section on collections.

Each collection has four-digit identifier, like '0001' for the Lawrence J.
Schoenberg collection. The collection identifier is used for the collection's
directory on OPenn; for example, [`/Data/0001`][LJS]. Every document in this
collection has TEI format metadata.

[LJS]: http://openn.library.upenn.edu/Data/0001/ "LJ Schoenberg Collection"

A primary collection always has a *metadata format*.

> At present, *metadata formats* include: 'TEI', 'Walters TEI', and 'Custom'.

#### Secondary collections

Secondary collections bring together items from one or more primary
collections and thus may contain items from multiple directories. A secondary
collection may be a subset of a single primary collection or draw multiple
primary collections. Secondary collections are intended to provide topical or
project-related groupings of items.

Secondary collections are virtual collections and have no representation in
OPenn's directory structure. Secondary collections can be accessed from HTML
files and machine-readable navigation files. See below for details.

#### Items

Primary collections are composed of items. Each item belongs to a primary
collection and is found in the primary collection's folder and has the same
metadata format and directory structure as all other items in that collection.
Items are structure collections of images and metadata corresponding to a
single object, like a book or manuscript.

The extent of an object and its corresponding digital item is determined by an
agreement between OPenn's managers and data providers. That extent should be
such that an institutional collection of such items makes sense.

> It remains to be decided whether a collection of archival papers would
> constitute one OPenn item or several.

> At present all items are sets of images and metadata for a single
> manuscript. In the future, other types of items will be added to OPenn.

Items must:

- be verifiable,
- be machine navigable,
- have descriptive metadata, and
- have structural metadata linked to image files.


### Items with TEI metadata format

TEI is used for data packages for manuscripts. Each item corresponds to a
single  manuscript. The following diagram shows the TEI package structure.

```
    ljs319
    |-- data
    |   |-- extra
    |   |   |-- master
    |   |   |   |-- ljs319_wk1_body0009a.tif
    |   |   |   |-- ljs319_wk1_body0009a.tif.xmp
    |   |   |   |-- ...
    |   |   |
    |   |   |-- thumb
    |   |   |   |-- ...
    |   |   |
    |   |   `-- web
    |   |       |-- ...
    |   |
    |   |-- ljs319_TEI.xml
    |   |-- master
    |   |   |-- 0311_0000.tif
    |   |   |-- 0311_0000.tif.xmp
    |   |   |-- 0311_0001.tif
    |   |   |-- 0311_0001.tif.xmp
    |   |   |-- 0311_0002.tif
    |   |   |-- ...
    |   |
    |   |-- thumb
    |   |   |-- 0311_0000_thumb.jpg
    |   |   |-- 0311_0000_thumb.jpg.xmp
    |   |   |-- ...
    |   |
    |   `-- web
    |       |-- 0311_0000_web.jpg
    |       |-- 0311_0000_web.jpg.xmp
    |       |-- ...
    |
    |-- manifest-sha1.txt
    `-- version.txt
```

The root directory is a normalized shelf mark/call number `ljs319` for LJS
319. Directory names may not contain spaces.

##### Package metadata

The top-level directory contains the data directory and the package metadata.
It is structured thus:

```
    ljs319
    |-- data/
    |-- manifest-sha1.txt
    `-- version.txt
```


The format of `the manifest-sha1.txt` follows the format of the output of the
GNU `sha1sum` program:

```
0d0886412592226f8a0044e7a1b0d50088830f04  data/ljs319_TEI.xml
1f097bb51003f966e8cc709f19555581ed22ac1a  data/master/0311_0005.tif
c9d46c1235d41074ea4e3b6e29b0e89e95d2c7c7  data/master/0311_0002.tif
7fa693138d586ac93e229b566ac56c4d3edddf9a  data/master/0311_0003.tif.xmp
a9c40cede3a0c5cab9214e05b4b574404c357959  data/master/0311_0007.tif.xmp
2c239526effe30e8900410cb5c9111d279e5b447  data/master/0311_0003.tif
...
```

It should be a rare occurrence, but from time-to-time packages will need to be
updated. OPenn does not yet have a full system for managing package versions;
however, in anticipation of that system each package is provided with a
`version.txt` file in its top-level directory:

```
ljs319
|-- data
|-- manifest-sha1.txt
`-- version.txt        # <= package version history
```

The following is the `version.txt` file for LJS 319.

```
version: 1.0.0
date: 2015-03-24T09:55:23
id: 311
document: 311
Initial version
---
```

##### TEI Descriptive and structural metadata

Document descriptive and structural metadata are provided in a TEI file. The
file is stored and named as follows:

     <PACKAGEDIR>/data/<PACKAGEDIR>_TEI.xml

Example:

     ljs319/data/ljs319_TEI.xml

The TEI file name always contains the name of the top-level package directory.

##### Image files

Each object's images and metadata are presented in a regular package structure
that allows for automated navigation of the package and its contents.

The directories have this structure:

```
    ljs319
    `-- data
        |-- extra
        |   |-- master
        |   |-- thumb
        |   `-- web
        |-- master
        |-- thumb
        `-- web
```

Core document images are in the package's `data/master`, `data/thumb`, and
`data/web` directories. All of these images are listed in the `<facsimile>`
section of the TEI manuscript description. Any other files provided with the
document, like color and ruler reference shots, are included in the
`data/extra` directory in `master`, `thumb`, and `web` sub-directories.



# Navigation

OPenn must be navigable by both humans and machines. HTML pages provide human
navigation to primary and secondary collections and items. Machines can
naively traverse the entire site's directory tree starting with the `/Data` or
from a single collection directory, like `/Data/0001`. Machines can also
employ special navigation files and information about conventions of item
structure and file naming.

Both human and machine navigation are described below.


## Human navigation

**Requirements**:

1. OPenn must provide documentation of its structure and content for both
   human and machine access.
2. All images and descriptive and structural metadata must be accessible to
   human users.
3. Human navigation pages should not interfere with machine navigation.

Human access is provided by HTML pages. There are two types of pages:
informational and descriptive/navigational.

#### Informational pages

The informational pages are:

- `/ReadMe.html`
- `/TechnicalReadMe.html`

The informational pages provide site documentation and orientation
information.

#### Descriptive/navigational pages

The bulk of the HTML pages are descriptive/navigational. Human users can
navigate to items on OPenn via lists of collections, which in turn link to
table of contents lists of items in each collection. From each table of
contents page, users can navigate to item browse pages, which give
descriptions and links to metadata and images belonging to the item.

The descriptive/navigational pages are:

- **Collections list** A list of all collections on OPenn with collection
  blurb and link to collection table of contents
  [`/Collections.html`][Colls]

- **Projects list** A list of all secondary collections on OPenn with
  collection blurb and link to each secondary collection table of contents;
  `/Projects.html` **[TO BE IMPLEMENTED]**

- **Primary collection TOC** Primary collection table of contents, with
  description of collection and link to Browse page for each item; e.g.,
  [`/html/0001.html`][TOC], for the Lawrence J. Schoenberg collection

- **Secondary collection TOC** Table of contents file for a secondary
  collection, with a description of the secondary collection and a link to the
  Browse page for each item; items grouped by primary collection; e.g.,
  `/html/bibliophilly.html` **[TO BE IMPLEMENTED]**

- **Browse page** Description of the item and a link to all master and
  derivative images for the item; e.g.,
  [`/Data/0011/html/XI_2_Lincolniana.html`][Browse] for the Tanner Diary of
  Lincoln's assassination

[Colls]:         http://openn.library.upenn.edu/Collections.html                      "Collections Page"

[TOC]:           http://openn.library.upenn.edu/html/0001.html                        "Collection TOC example"
[root_html_dir]: http://openn.library.upenn.edu/html/                                 "Root HTML dir"

[Browse]:        http://openn.library.upenn.edu/Data/0011/html/XI_2_Lincolniana.html  "Object page example"
[coll_html_dir]: http://openn.library.upenn.edu/Data/0001/html/                       "Collection HTML dir"

#### Hidden directories

To prevent interference with machine navigation, most descriptive/navigational
pages are in hidden `html` directories -- that is, the web server is
configured not to display `html` directories when returning directory
listings. The use of such hidden directories is not a requirement, but an
implementation of the requirement that human and machine navigational methods
not overlap.

Apart from the Collections and Projects pages, all descriptive/navigational
pages are in the hidden `html` directories. These directories are:

- The root [`/html`][root_html_dir] directory

- Collection specific `html` directories like
  [`/Data/0001/html`][coll_html_dir]

The root `html` directory contains all primary and secondary collection TOC
files, like [`/html/0001.html`][TOC].

The collection specific `html` directories contain all item browse pages, like
[`/Data/0011/html/XI_2_Lincolniana.html`][Browse].

## Machine navigation

#### Requirements

1. Machines should be able to access the site and its data recursively via
   HTTP.
2. Machines should be able to select subsets of data based on topical
   collections, institutional collection, metadata type, file type, or date of
   item creation or update.
3. Each item in a primary collection must have have the same structural and
   descriptive metadata type and have the same arrangement of data and
   metadata.
    - This requirement supports the creation of uniform methods of processing
      based on metadata type.
4. Item data integrity must be verifiable.

## Navigation files

**NOTE: All items below are TO BE IMPLEMENTED.**

For machine access CSV files are provided for lists of: primary
collections, secondary collections, items in each primary collections, items
in each secondary collection.

##### Collections CSV

The collections CSV file is called `collections.csv` and is located in
the data folder:

    Data/collections.csv

It has these columns:

- `collection_id`:    the numerical ID of the collection; e.g., `0001`; 'N/A'
                      for secondary collections

- `collection_tag`:   a mnemonic tag for the collection; e.g., `ljs`, `pennmss`

- `collection_type`:  `primary` or `secondary`

- `metadata_type`:    `OPENN-TEI`, `WALTERS-TEI`, etc.; secondary collections
                      may also have metadata type of `MIXED`

- `collection_name`:  human name for the collection; e.g., 'Historical Society
                      of Pennsylvania'

A sample file, with padding added for legibility, follows.

```
collection_id,  collection_tag, collection_type,  metadata_type,  collection_name
0001,           ljs,            primary,          OPENN-TEI,      Lawrence J. Schoenberg Manuscripts
0002,           pennmss,        primary,          OPENN-TEI,      University of Pennsylvania Books & Manuscripts
0003,           brynmawr,       primary,          OPENN-TEI,      Bryn Mawr College Library Special Collections
0004,           drexarc,        primary,          OPENN-TEI,      Drexel University Archives and Special Collections
N/A,            bibliophilly,   secondary,        OPENN-TEI,      Bibliotheca Philadelphiensis
```

##### Primary Collections TOC

All primary collections have a table of contents file. This file is named
`contents.csv` and is located in the collection folder; thus:

    /Data/0002_contents.csv

The file has these columns:

- `document_id`:  the numerical ID of the item
- `path`:         the path of the item folder, relative to the CSV file
- `title`:        the text title of the document
- `created`:      the database date-time the document ID was created
- `updated`:      the database date-time the item was last updated

A sample follows, with padding added for legibility.

```
document_id,  path,                   title,                              created,              updated
1435,         0002/mscodex901         "Il finto Policare, tragicomedia",  2015-10-15 13:02:00,  2015-10-15 08:22:00
1710,         0002/mscoll764_item84,  Some title,                         2016-02-21 16:13:11,  2016-02-23 09:55:38
1711,         0002/mscoll764_item85,  Some title,                         2016-02-21 16:13:30,  2016-02-23 09:55:38
1712,         0002/mscoll764_item86,  Some title,                         2016-02-21 16:13:55,  2016-02-23 09:55:38
```

> **Implementation note:**
>
> The fields `created` and `updated` reflect date-times recorded in OPenn's
> database. The item's files may be pushed hours or even days after the item
> was created or updated. For this reason, programs looking for items updated
> since last check should use the most recent `updated` value of the previous
> check as lower bounding date.
>
> In the example above, three items have the same `updated` value. This time
> was  set when the OPenn scripts found these items on-line and set the
> `is_online`  field to `true`. (The `is_online` flag is used to create the
> TOC and Browse  web pages. These pages are generated based on an item's
> presence on line.)  However, if an item is updated and re-pushed to the
> OPenn website, it will  have an updated date later than its original on-line
> date.

##### Secondary Collections TOC

Secondary collections have corresponding table of contents files. These files
are named by the collection tag; for example, `bibliophilly_contents.csv`. A
secondary collection TOC has these columns:

- `primary_collection_id`:
                    the ID of the primary collection; e.g., '0020'

- `document_id`:    the numeric ID of the document; e.g., '2420'

- `path`:           the relative path to the item's folder; e.g.,
                    `0002/mscoll764_item86`

- `metadata_type`:  the items metadata format; e.g., 'TEI'

- `title`:          title of the item; e.g., 'Il finto Policare, tragicomedia'

- `added`:          date the item was added to the collection

The following is a sample secondary collection TOC file,
`bibliophilly_contents.csv`.

```
primary_collection_id,    document_id,  path,             metadata_type,  title,                  added
0002,                     1435,         0002/mscodex117,  TEI,            Alchemical miscellany,  2016-11-29 10:55:00
0001,                     288,          0001/ljs447,      TEI,            Masālik al-abṣār...,    2016-12-02 15:10:00
```
