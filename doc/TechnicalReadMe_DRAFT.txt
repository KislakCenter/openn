## Licenses and use

All images and metadata descriptions provided here are released
under Creative Commons licenses. All images and metadata are released
under licenses that Creative Commons has approved for Free Cultural
Works, bearing:

- the CC Public Domain mark
    - <https://creativecommons.org/about/pdm>
- CC0 (“CC-zero”), the Public Domain dedication for copyrighted works
    - <https://creativecommons.org/about/cc0>
- CC-BY, the Creative Commons Attribution license
    - <http://creativecommons.org/licenses/by/4.0/>
- CC-BY-SA, the Creative Commons Attribution-Share Alike license
    - <http://creativecommons.org/licenses/by-sa/4.0/>



You are free to download and use the images and metadata on this
website under the license assigned to each document. You do not need
to apply to the holding institutions prior to using the images. We do
ask that whenever possible you cite this website and the holding
institution when you use any of these resources.

On this website, you will find material from several institutional
collections.  In order to determine the license under images have been
released, please refer to each collection's web page on OPenn.



## Accessing the data

Data on this site can be accessed in a number of ways, via the HTTP
web site, anonymous FTP, and the RSYNC remote synchronization
utility. Each of these is discussed below.

Users who want to do more than do casual browsing using the site’s
HTML pages should understand its directory structure. The basic
organization is:

    0_IntroductionReadMe.html              # general site information
    1_TechnicalHelpReadMe.html             # this file
    2_OPennCollection.html                 # list of collections on OPenn
    TablesOfContents/                      # individual collection listings
      |---- TOC_LJSchoenbergManuscripts.html # list of L. J. Schoenberg manuscripts
      |---- TOC_PennManuscripts.html         # list of Penn manuscripts
    Data/                                  # core site data
      |--- LJSchoenbergManuscripts/        # L. J. Schoenberg manuscript images
      |      |--- ljs16/                   # Manuscript LJS 16
      |      |      |--- ...
      |      |--- ...
      |--- PennManuscripts/                 # U. Penn manuscript images
      |      |--- mscodex1048/          # Manuscript MS Codex 1048
      |      |      |--- ...
      |      |--- ...
      |--- ...

Within each manuscript directory, manuscript images and metadata are
presented in a self-contained package, which is described below.

## HTTP Access

Individual manuscript images can viewed and downloaded from this
site using a Web browser. Site navigation guides are in the How to use
this data set section of the ReadMe file.

## Anonymous FTP

This site is accessible via anonymous FTP, at openn.library.upenn.edu:

    $ ftp anonymous@openn.library.upenn.edu

TODO: COMPLETE this

Use your email address as your password.

Free graphical FTP clients are available for all major commercial and
free operating systems. For configuration of FTP client software, use
the standard FTP network port, 21.

## Anonymous RSYNC

RSYNC is an application for synchronizing files between computer
systems and is probably the best tool to use for bulk retrieval of
data from OPenn.

All data is accessible via anonymous rsync. From the command line on
Unix systems the following command can be used to see available
targets.

TODO: COMPLETE ANONYMOUS RSYNC

    > rsync rsync://thedigitalwalters.org

    WaltersManuscripts	Digitized versions of Walters Manuscripts
    OtherCollections	Digitized versions of books and manuscripts not in the Walters collection
    DigitalGalen   	A Syriac palimpsest of Galen
Adding a target to the above command will show give a list of items available under that target:

    > rsync rsync://thedigitalwalters.org/WaltersManuscripts/

    drwxr-xr-x         197 2010/08/06 14:31:34 .
    drwxr-xr-x         117 2011/06/09 18:07:31 ManuscriptDescriptions
    drwxr-xr-x           7 2011/04/05 16:17:24 W102
    drwxr-xr-x           7 2010/08/23 11:49:02 W106
    drwxr-xr-x           7 2011/04/04 15:12:46 W12
    drwxr-xr-x           7 2011/04/05 14:28:24 W13
    drwxr-xr-x           7 2011/04/06 10:30:44 W165
    drwxr-xr-x           7 2010/07/23 10:42:56 W171
    drwxr-xr-x           7 2011/04/06 15:37:20 W174
    drwxr-xr-x           7 2011/03/28 10:24:02 W4
    ...

You can pull down an entire Walters manuscript by using its modified
shelf mark. This command will download all of Walters W.579 to the
user tom’s Manuscripts directory:

      > rsync -ax rsync://thedigitalwalters.org/WaltersManuscripts/W579 \
                /Users/tom/Manuscripts/

That command will silently retrieve all of W.579. To get more detailed
information about what is happening, you could use a command like the
following:

      > rsync -avx --progress  \
                rsync://thedigitalwalters.org/WaltersManuscripts/W579 \
                /Users/tom/Manuscripts/

Be aware that the data set is quite large, and the images for a single
manuscripts can be over 200 GB.

You can pull down a specific set of images for a manuscript (master or
300 PPI TIFFs, or web (‘SAP’) or thumbnail JPEGs) by specifying the
image folder. This command will retrieve all SAP web JPEGs for
manuscript W.579:

      > rsync -avx --progress  \
                rsync://thedigitalwalters.org/WaltersManuscripts/W579/data/W.579/sap/ \
                /Users/tom/Manuscripts/

Always verify the path via the website before setting up such a
command. Notice that there is some inconsistency in the naming of
directories.

## File naming conventions

Image files have names like:


    0284_0000.tif
    0284_0000_thumb.tif
    0284_0000_web.tif

    0284_0001.tif
    0284_0001_thumb.tif
    0284_0001_web.tif

    0284_0002.tif
    0284_0002_thumb.tif
    0284_0002_web.tif

    0284_0003.tif
    0284_0003_thumb.tif
    0284_0003_web.tif

Each image has a base name consisting of document identifier (e.g.,
`0284`), underscore, and a serial number (e.g., `0003`). Each of the
three files that shares a base name is a different version of the same
image. Serial numbers are in a natural order, such as book page
order. For example, if an entire book has been imaged including cover,
then the first serial number (`0000`) would be assigned to the outside
front cover, the second serial number to the insdie front cover, and
so on.

Note that what parts of an object are imaged and what order they are
given in will depend on the providing institution's practice and
policies.  The order and description of each image will be given in
each object's TEI description's `<facsimile>`.  See below for more
information on manuscript descriptions.

    0284_0000
    0284_0001
    0284_0002
    0284_0003


The rest of the file name indicates the derivative and file type of
the image. Images are either TIFF `.tif` or JPEG `.jpg`. There are
three derivative types. They are:


- a full-sized master image, typically a TIFF;
- a web JPEG image is 1800 pixels on its longest side; and
- a thumbnail JPEG that is 190 pixels on its longest side.

The file names indicate the derivative type through a tag, which is
the last segment of the file name before the extension .tif or
.jpg. The tag is `web` for the WEB JPEG, and `thumb` for the thumbnail
JPEG. The master image has no tag.

The following file names are for the master, web and thumbnail images
for LJS 16, image serial number `0284`:

    0284_0000.tif
    0284_0000_thumb.tif
    0284_0000_web.tif

### XMP sidecar files

Each image is accompanied by an XMP "sidecar" file that contains the
image's metadata. Each sidecar file has the name of the image with an
additional `.xmp` extension:

    0284_0000.tif
    0284_0000.tif.xmp
    0284_0000_thumb.tif
    0284_0000_thumb.tif.xmp
    0284_0000_web.tif
    0284_0000_web.tif.xmp

See below for more information on the XMP metadata.

## Finding the file you want

Image subject names are made available in two ways: through a
human-readable browse page and through a TEI manuscript description.

First, each object's web page lists the pieces in order with the piece
name (“folio 1a”, “front flyleaf 1a”, etc.) and associated file names,
as can be seen here:


- <http://openn.library.upenn.edu/Data/LJSchoenbergManuscripts/html/ljs168.html>


Second, each object is provided with a TEI manuscript description that
lists all images in order in the TEI file's `<facsimile>` section.
Note this excerpt from [ljs168_TEI.xml][ljs168_TEI]:

[ljs168_TEI]: http://openn.library.upenn.edu/Data/LJSchoenbergManuscripts/ljs168/data/ljs168_TEI.xml "LJS 268 TEI file"

    <facsimile>
      <surface n="Front cover">
        <graphic height="3478px" url="master/0103_0000.tif" width="3287px"/>
        <graphic height="190px" url="thumb/0103_0000_thumb.jpg" width="179px"/>
        <graphic height="1800px" url="web/0103_0000_web.jpg" width="1701px"/>
      </surface>
      <surface n="Inside front cover">
        <graphic height="3478px" url="master/0103_0001.tif" width="3287px"/>
        <graphic height="190px" url="thumb/0103_0001_thumb.jpg" width="179px"/>
        <graphic height="1800px" url="web/0103_0001_web.jpg" width="1701px"/>
      </surface>
      <surface n="Flyleaf 1 recto">
        <graphic height="3478px" url="master/0103_0002.tif" width="3287px"/>
        <graphic height="190px" url="thumb/0103_0002_thumb.jpg" width="179px"/>
        <graphic height="1800px" url="web/0103_0002_web.jpg" width="1701px"/>
      </surface>
      <surface n="Flyleaf 1 verso">
        <graphic height="3478px" url="master/0103_0003.tif" width="3287px"/>
        <graphic height="190px" url="thumb/0103_0003_thumb.jpg" width="179px"/>
        <graphic height="1800px" url="web/0103_0003_web.jpg" width="1701px"/>
      </surface>
      <surface n="1r">
        <graphic height="3478px" url="master/0103_0004.tif" width="3287px"/>
        <graphic height="190px" url="thumb/0103_0004_thumb.jpg" width="179px"/>
        <graphic height="1800px" url="web/0103_0004_web.jpg" width="1701px"/>
      </surface>

### Manuscript packaging & preservation metadata

Each object's images and metadata are provided in a packaged structure
that permit verification allow for automated navigation of the package
and its contents.

The diagram below shows a typical package structure:

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


The directories have this structure:

    ljs319
    `-- data
        |-- extra
        |   |-- master
        |   |-- thumb
        |   `-- web
        |-- master
        |-- thumb
        `-- web

The package is divided into the top-level directory (in this case
`ljs319`), which contains package metadata, and the data itself, found
here in the directory `ljs319/data`.  The `data` directory contains
the manuscript description and the image files and their
metadata. Each of these is described below.

##### Package metadata

The top-level directory contains the `data` directory and the package
metadata.

    ljs319
    |-- data
    |-- manifest-sha1.txt
    `-- version.txt

There are two package metadata files: `manifest-sha1.txt` and
`version.txt`.  The first lists each file in the data directory with
its SHA-1 checksum.  The second provides information for the *package*
version.

See below under ''Technical and preservation metadata'' for more on
the manifest and version files.


# Preservation and technical metadata


## Package contents and integrity

The top-level directory of each package contains a `manifest-sha1.txt`
file that lists each file in the package's data directory with its
SHA-1 checksum.

    ljs319
    |-- data
    |-- manifest-sha1.txt  # <= package contents and integrity file
    `-- version.txt

The format of the `manifest-sha1.txt` follows the format of the output
of the GNU `sha1sum` program:

    0d0886412592226f8a0044e7a1b0d50088830f04  data/ljs319_TEI.xml
    1f097bb51003f966e8cc709f19555581ed22ac1a  data/master/0311_0005.tif
    c9d46c1235d41074ea4e3b6e29b0e89e95d2c7c7  data/master/0311_0002.tif
    7fa693138d586ac93e229b566ac56c4d3edddf9a  data/master/0311_0003.tif.xmp
    a9c40cede3a0c5cab9214e05b4b574404c357959  data/master/0311_0007.tif.xmp
    2c239526effe30e8900410cb5c9111d279e5b447  data/master/0311_0003.tif
    ...

Checksums can be used to confirm a file's integrity; that is, that it
has not been change since it was last modified.

On Mac OS, Linux, and other Unix-like operating systems verification
can be done using `sha1sum` or a similar command-line utility.

Running `sha1sum` on a file will print its checksum and name:

    $ sha1sum data/ljs319_TEI.xml
    0d0886412592226f8a0044e7a1b0d50088830f04  data/ljs319_TEI.xml

This checksum value can be used to confirm the file has remain
unchanged.  Notice that the checksum printed by `sha1sum` is identical
to the one listed above in the `manifest-sha1.txt` file.

`Sha1sum` can also be used with the `-c` flag to check an entire
manifest:

    $ sha1sum -c manifest-sha1.txt
    data/ljs319_TEI.xml: OK
    data/master/0311_0005.tif: OK
    data/master/0311_0002.tif: OK
    data/master/0311_0003.tif.xmp: OK
    ...

There are checksum verification programs for all modern operating
systems.  Each behaves differently.  Familiarize yourself with the one
you choose.  Here are some examples:

- [Microsoft File Checksum Integrity Verifier][miv] (Windows)
- [Mac OS X: How to verify a SHA-1 digest][macsha1] (Mac)
- [sha1sum(1) - Linux man page][sha1sum] (Linux)
- [Comparison of file verification software][verifysw] (Wikipedia)

[miv]: http://www.microsoft.com/en-us/download/details.aspx?id=11533 "Microsoft File Checksum Integrity Verifier"
[macsha1]: https://support.apple.com/en-us/HT201259 "Mac OS X: How to verify a SHA-1 digest"
[sha1sum]: http://linux.die.net/man/1/sha1sum "sha1sum(1) - Linux man page"
[verifysw]: http://en.wikipedia.org/wiki/Comparison_of_file_verification_software "Comparison of file verification software (Wikipedia)"

For more on SHA-1 see the [SHA-1 Wikipedia page][sha1wiki].

[sha1wiki]: http://en.wikipedia.org/wiki/SHA-1 "SHA-1 (Wikipedia)"

## Package version

It should be a rare occurrence, but from time-to-time packages will
need to be updated.  OPenn does not yet have a full system for
managing package versions; however, in anticipation of that system
each package is provided with a `version.txt` file its top-level
directory:

    ljs319
    |-- data
    |-- manifest-sha1.txt
    `-- version.txt        # <= package version history

The following is the `version.txt` file for LJS 319.

    version: 1.0.0
    date: 2015-03-24T09:55:23
    id: 311
    document: 311

    Initial version
    ---

The file contains one or more dash-separated stanzas for each version
of a package.  The top stanza is for the most recent version of the
package.  The structure of each stanza is:

    version: <SEMANTIC_VERSION_OF_PACKAGE>
    date: <TIMESTAMP_OF_VERSION_RECORD>
    id: <DATABASE_ID_OF_VERSION_RECORD>
    document: <DATABASE_ID_OF_DOCUMENT>

    <DESCRIPTION/REASON>
    ---


- `version`: The version number is a three-part semantic version
  number; e.g., `1.0.0`, `1.0.1`, or `1.1.0`.
- `date`: timestamp of this version's creation
- `id`: database identifier of this version
- `document`: database identifier of the package document
- `description`: the reason for this version

**Semantic versioning**

OPenn uses semantic versions with a three-component version number:

    0.0.0: <MAJOR>.<MINOR>.<PATCH>

New versions of a package contain alterations of data and metadata
content.  Version number changes indicate the type of change and
whether a new version will likely be compatible with applications
built on previous versions of the package.

All OPenn packages are machine readable and follow a regular pattern.
Any application that loads OPenn data dynamically should have no
problem with changing package contents; however, applications that
cache part of the data may fail to work with a new version of a
package that, for example, has fewer images than images than the
previous version or removed metadata.

A change to the last digit (e.g., `1.0.0` to `1.0.1`) indicates a
''patch'' or correction that does not add or remove data or metadata.
The package remains compatible with applications built on the previous
version of the package.  An example of a patch change would be the
substitution of the a correct image for a duplicate one; or a spelling
correction in metadata.

A minor version change, a change to the second digit in the version
number (e.g., `1.0.0` to `1.1.0`), indicates the addition of new data
or metadata.  The package remains compatible with applications built
on the previous version of the package.  An example of a patch change
would be the addition of new metadata to the document's manuscript
description or the addition of new images to the data set. While the
new version of the package will work as before, it may desirable to
update software to take advantage of new data.

A major version change, a change to the first digit in the version
number, indicates the removal of data or metadata or other substantive
change that will likely cause this version to not work with software
built on a previous version of the package.

## Document descriptions and structural metadata

The description of document content and structural metadata are
provided in a TEI file like `ljs319_TEI.xml`.  The file is stored and
named as follows:

     <PACKAGEDIR>/data/<PACKAGEDIR>_TEIL.xml

     ljs319/data/ljs319_TEI.xml

The TEI file name always contains the name of the top-level package
directory.

See the section TEI manuscript description below for a detailed
description of the TEI contents.

## XMP

Each image file has key Dublin Core metadata stored in its header.
This information is also included in a `.xmp` sidecar file for each
image:

    0311_0000.tif
    0311_0000.tif.xmp
    0311_0000_thumb.jpg
    0311_0000_thumb.jpg.xmp
    0311_0000_web.jpg
    0311_0000_web.jpg.xmp

In addition to Dublin Core metadata the XMP file includes technical
metadata about the image and XMP rights information.  What follows is
the content of a sample XMP file.

    <?xpacket begin='﻿' id='W5M0MpCehiHzreSzNTczkc9d'?>
    <x:xmpmeta xmlns:x='adobe:ns:meta/' x:xmptk='Image::ExifTool 9.67'>
    <rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>

     <rdf:Description rdf:about=''
      xmlns:aux='http://ns.adobe.com/exif/1.0/aux/'>
      <aux:Firmware>P45+-H, Firmware: Main=5.1.2, Boot=1.3, FPGA=1.6.8, CPLD=3.2.6, PAVR=1.0.9, UIFC=1.0.1, TGEN=1.0.1</aux:Firmware>
     </rdf:Description>

     <rdf:Description rdf:about=''
      xmlns:dc='http://purl.org/dc/elements/1.1/'>
      <dc:creator>
       <rdf:Seq>
        <rdf:li>The University of Pennsylvania Libraries</rdf:li>
       </rdf:Seq>
      </dc:creator>
      <dc:date>
       <rdf:Seq>
        <rdf:li>2015-03-24</rdf:li>
       </rdf:Seq>
      </dc:date>
      <dc:description>
       <rdf:Alt>
        <rdf:li xml:lang='x-default'>This is an image of fol. 1r from University of Pennsylvania LJS 319: Derrota, from Manila, Philippines, dated to approximately 1750.</rdf:li>
       </rdf:Alt>
      </dc:description>
      <dc:format>image/tiff</dc:format>
      <dc:identifier>311.64390</dc:identifier>
      <dc:publisher>
       <rdf:Bag>
        <rdf:li>The University of Pennsylvania Libraries</rdf:li>
       </rdf:Bag>
      </dc:publisher>
      <dc:relation>
       <rdf:Bag>
        <rdf:li>University of Pennsylvania LJS 319</rdf:li>
        <rdf:li>bibid: 6074170</rdf:li>
        <rdf:li>http://hdl.library.upenn.edu/1017/d/medren/6074170</rdf:li>
       </rdf:Bag>
      </dc:relation>
      <dc:rights>
       <rdf:Alt>
        <rdf:li xml:lang='x-default'>This image and its content are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/.</rdf:li>
       </rdf:Alt>
      </dc:rights>
      <dc:subject>
       <rdf:Bag>
        <rdf:li>Navigation--Early works to 1800</rdf:li>
        <rdf:li>Pilot guides--Philippines</rdf:li>
        <rdf:li>Codices</rdf:li>
        <rdf:li>Tables (documents)</rdf:li>
        <rdf:li>Manuscripts, Spanish--18th century</rdf:li>
        <rdf:li>Manuscripts, European</rdf:li>
       </rdf:Bag>
      </dc:subject>
      <dc:title>
       <rdf:Alt>
        <rdf:li xml:lang='x-default'>University of Pennsylvania LJS 319: Derrota, fol. 1r</rdf:li>
       </rdf:Alt>
      </dc:title>
      <dc:type>
       <rdf:Bag>
        <rdf:li>image</rdf:li>
       </rdf:Bag>
      </dc:type>
     </rdf:Description>

     <rdf:Description rdf:about=''
      xmlns:exif='http://ns.adobe.com/exif/1.0/'>
      <exif:DateTimeOriginal>2014-07-08T15:11:35</exif:DateTimeOriginal>
      <exif:ExifVersion>0220</exif:ExifVersion>
      <exif:ExposureTime>1/60</exif:ExposureTime>
      <exif:FileSource>3</exif:FileSource>
      <exif:ISOSpeedRatings>
       <rdf:Seq>
        <rdf:li>50</rdf:li>
       </rdf:Seq>
      </exif:ISOSpeedRatings>
      <exif:LightSource>255</exif:LightSource>
      <exif:PixelXDimension>3882</exif:PixelXDimension>
      <exif:PixelYDimension>5614</exif:PixelYDimension>
      <exif:SceneType>1</exif:SceneType>
      <exif:ShutterSpeedValue>23917/4049</exif:ShutterSpeedValue>
     </rdf:Description>

     <rdf:Description rdf:about=''
      xmlns:exifEX='http://cipa.jp/exif/1.0/'>
      <exifEX:BodySerialNumber>DR000149</exifEX:BodySerialNumber>
     </rdf:Description>

     <rdf:Description rdf:about=''
      xmlns:photoshop='http://ns.adobe.com/photoshop/1.0/'>
      <photoshop:DateCreated>2014-07-08</photoshop:DateCreated>
      <photoshop:LegacyIPTCDigest>A44D267D0C570E3E8B6B52DEBEE3DCA9</photoshop:LegacyIPTCDigest>
      <photoshop:Source>University of Pennsylvania LJS 319, fol. 1r</photoshop:Source>
     </rdf:Description>

     <rdf:Description rdf:about=''
      xmlns:tiff='http://ns.adobe.com/tiff/1.0/'>
      <tiff:BitsPerSample>
       <rdf:Seq>
        <rdf:li>8</rdf:li>
        <rdf:li>8</rdf:li>
        <rdf:li>8</rdf:li>
       </rdf:Seq>
      </tiff:BitsPerSample>
      <tiff:Compression>1</tiff:Compression>
      <tiff:ImageLength>5614</tiff:ImageLength>
      <tiff:ImageWidth>3882</tiff:ImageWidth>
      <tiff:Make>Phase One</tiff:Make>
      <tiff:Model>P45+</tiff:Model>
      <tiff:Orientation>1</tiff:Orientation>
      <tiff:PhotometricInterpretation>2</tiff:PhotometricInterpretation>
      <tiff:PlanarConfiguration>1</tiff:PlanarConfiguration>
      <tiff:ResolutionUnit>2</tiff:ResolutionUnit>
      <tiff:SamplesPerPixel>3</tiff:SamplesPerPixel>
      <tiff:Software>Capture One 7 Windows</tiff:Software>
      <tiff:XResolution>600/1</tiff:XResolution>
      <tiff:YResolution>600/1</tiff:YResolution>
     </rdf:Description>

     <rdf:Description rdf:about=''
      xmlns:xmp='http://ns.adobe.com/xap/1.0/'>
      <xmp:CreateDate>2014-07-08T15:11:35</xmp:CreateDate>
      <xmp:ModifyDate>2014-07-08T15:11:35</xmp:ModifyDate>
     </rdf:Description>

     <rdf:Description rdf:about=''
      xmlns:xmpRights='http://ns.adobe.com/xap/1.0/rights/'>
      <xmpRights:Marked>False</xmpRights:Marked>
      <xmpRights:UsageTerms>
       <rdf:Alt>
        <rdf:li xml:lang='x-default'>This image and its content are free of known copyright restrictions and in the public domain. See the Creative Commons Public Domain Mark page for usage details, http://creativecommons.org/publicdomain/mark/1.0/.</rdf:li>
       </rdf:Alt>
      </xmpRights:UsageTerms>
     </rdf:Description>
    </rdf:RDF>
    </x:xmpmeta>
    <?xpacket end='w'?>


#### Notable XMP elements

Dublin Core elements:

- `creator` -- person or organization responsible for creation of the
  image
    - example: "The University of Pennsylvania Libraries"

- `date` -- date of the creation of this version of the image,
  including metadata
    - example: "2015-03-24"

- `description` -- brief description of the image content
    - example: "This is an image of fol. 1r from University of
      Pennsylvania LJS 319: Derrota, from Manila, Philippines, dated
      to approximately 1750."


- `format` -- MIME type of the image, either `image/tiff` or
  `image/jpeg`

- `identifier` -- unique identifier of the master image and its
  derivatives
    - example: "311.64390"

- `publisher` -- person or organization responsible for publication of
  the image
    - example: "The University of Pennsylvania Libraries"

- `relation` -- a related resource
    - example: "University of Pennsylvania LJS 319"

- `rights` -- access rights
    - example: "This image and its content are free of known copyright
      restrictions and in the public domain. See the Creative Commons
      Public Domain Mark page for usage details,
      http://creativecommons.org/publicdomain/mark/1.0/."

- `subject` -- a list of subjects
    - examples: "Navigation--Early works to 1800", "Pilot
      guides--Philippines"

- `title` -- the title of the image
    - example: "University of Pennsylvania LJS 319: Derrota, fol. 1r"

- `type` -- the resource type, always "image"

Photoshop element:

- `Source` -- the source of the image content
    - example: "University of Pennsylvania LJS 319, fol. 1r"

#### xmpRight elements

- `Marked` -- whether this is a right-managed resource; "False" if
  Public Domain, "True" otherwise

- `UsageTerms` -- a description of the terms of usage for this
  resource
    - example: "This image and its content are free of known copyright
      restrictions and in the public domain. See the Creative Commons
      Public Domain Mark page for usage details,
      http://creativecommons.org/publicdomain/mark/1.0/."

# TEI document description

Each document package includes a TEI file that provides a manuscript
description and

# Standards

OPenn data and metadata adhere to international standards. The
following is a list of the most important of those.

- Dublin Core: each image includes descriptive Dublin Core metadata
  (see Dublin Core in the Read Me file for details)

- TEI P5: manuscript description information is encoded according to
  Text Encoding Initiative (TEI) P5 guidelines (see the Manuscript
  Description file) BagIt: images are packaged and delivered using the
  BagIt protocol (see above)

- TIFF: when available TIFF images are used for master images

- Unicode: text information in XML files and other text documents is
  in Unicode, typically with UTF-8 encoding

- XMP: Extensible Metadata Platform
