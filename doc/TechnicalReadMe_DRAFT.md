
LICENSE AND USE


All Walters manuscript images and descriptions provided here are licensed for use under the the Creative Commons Attribution-Share Alike 3.0 Unported License and the GNU Free Documentation License.

You are free to download and use the images and descriptions on this website under the licenses named above. You do not need to apply to the Walters prior to using the images. We ask only that you cite the source of the images as the Walters Art Museum (see citation style in the ReadMe document).

Additionally, we request that a copy of any work created using these materials be sent to the Curator of Manuscripts and Rare Books at the Walters Art Museum, 600 N. Charles Street, Baltimore, MD 21201, mss-curator@thewalters.org.

Note these terms mark a change from our previous license, which placed a noncommercial restriction on the use of these materials. The noncommercial restriction no longer applies, and this license supercedes the previously advertised license, and replaces that found in many of the archival TIFF image headers.

This change follows the Walters Art Museum’s licensing policy. More information on the Walters’ intellectual property policy can be found on the Walters website: http://art.thewalters.org/license/.

SPONSORSHIP
The images and descriptions of Walters manuscripts on this website were created with funding awarded to the Walters Art Museum by the National Endowment for the Humanities in two projects—Islamic Manuscripts of the Walters Art Museum: A Digital Resource (2008 to 2011) and Parchment to Pixel: Creating a Digital Resource of Medieval Manuscripts (2010 to present). Additional funding has been provided by an anonymous donor.

ACCESSING THE DATA
Data on this site can be accessed in a number of ways, via the HTTP web site, anonymous FTP, and the RSYNC remote synchronization utility. Each of these is discussed below.

Users who want to do more than do casual browsing using the site’s HTML pages should understand its directory structure. The basic organization is:

01_ACCESS_WALTERS_MANUSCRIPTS.html  # list of Walters manuscripts
02_ACCESS_OTHER_BOOKS.html          # list of other books here
03_ReadMe.html                      # general site introduction
04_TechnicalReadMe.html             # this file
Data/                               # data: images and manuscript descriptions
 |--- DigitalGalen/                 # Galen palimpsest
 |     |--- ...
 |
 |--- OtherCollections/             # Non-Walters manuscripts
 |     |--- ...
 |
 |--- WaltersManuscripts/           # Walters manuscripts
       |--- ManuscriptDescriptions/ # TEI P5 manuscript descriptions
       |     |--- ...
       |
       |--- W102/                   # Image files for manuscript W.102
       |     |--- ...
       |
       |--- W106/
       |--- W12/
       |--- W13/
       |--- ...
Within each manuscript directory, manuscripts are collected in a data delivery package called a “bag,” which is described in detail below.

HTTP ACCESS
Individual manuscript images can viewed and downloaded from this site using a Web browser. Site navigation guides are in the How to use this data set section of the ReadMe file.

ANONYMOUS FTP
This site is accessible via anonymous FTP, at thedigitalwalters.org:

    $ ftp anonymous@thedigitalwalters.org
    Connected to thedigitalwalters.org.
    220 (vsFTPd 2.1.0)
    331 Please specify the password.
    Password:
    230 Login successful.
    Remote system type is UNIX.
    Using binary mode to transfer files.
    ftp>
Use your email address as your password.

Free graphical FTP clients are available for all major commercial and free operating systems. For configuration of FTP client software, use the standard FTP network port, 21.

ANONYMOUS RSYNC
RSYNC is an application for synchronizing files between computer systems and is probably the best tool to use for bulk retrieval of data from the Digital Walters.

All data is accessible via anonymous rsync. From the command line on Unix systems the following command can be used to see available targets.

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
You can pull down an entire Walters manuscript by using its modified shelf mark. This command will download all of Walters W.579 to the user tom’s Manuscripts directory:

      > rsync -ax rsync://thedigitalwalters.org/WaltersManuscripts/W579 \
                /Users/tom/Manuscripts/
That command will silently retrieve all of W.579. To get more detailed information about what is happening, you could use a command like the following:

      > rsync -avx --progress  \
                rsync://thedigitalwalters.org/WaltersManuscripts/W579 \
                /Users/tom/Manuscripts/
Be aware that the data set is quite large, and the images for a single manuscripts can be over 200 GB.

You can pull down a specific set of images for a manuscript (master or 300 PPI TIFFs, or web (‘SAP’) or thumbnail JPEGs) by specifying the image folder. This command will retrieve all SAP web JPEGs for manuscript W.579:

      > rsync -avx --progress  \
                rsync://thedigitalwalters.org/WaltersManuscripts/W579/data/W.579/sap/ \
                /Users/tom/Manuscripts/
Always verify the path via the website before setting up such a command. Notice that there is some inconsistency in the naming of directories.

Manuscript descriptions are found in different directory:

/WaltersManuscripts/ManuscriptDescriptions

They are comparatively small, and can be retrieved individually. You can get them all via rsync with the following command:

      > rsync -avzx rsync://thedigitalwalters.org/WaltersManuscripts/ManuscriptDescriptions \
                /Users/tom/Manuscripts/
Note that this command adds the z flag, which compresses the data before transfer.

FILE NAMING CONVENTIONS
Manuscripts image files have names like:

W583_000001_300.tif
W583_000001_1200.tif
W583_000001_sap.jpg
W583_000001_thumb.jpg
Each image has a base name consisting of the shelf mark (less the dot ’.’ character), an underscore, and a serial number. Each of the four files that shares a base name is a different version of the same image. Serial numbers are assigned sequentially to each manuscript component as it is added to the database imaging list. This number does not necessarily reflect the order of the image subject in the manuscript.

W582_000001
W582_000002
W582_000003
W582_000004
etc.
The rest of the file name indicates the derivative and file type of the image. Images are either TIFF .tif or JPEG .jpg. There are four derivative types. They are:

a full-sized, archival TIFF image, which includes a ruler and a Macbeth color-calibration chart in the frame (600 PPI text folios/ 1200 PPI illuminated folios);
a 300 PPI TIFF suitable for print publication;
a standard all-purpose (SAP) JPEG intended for web use that is 1800 pixels on its longest side; and
a thumbnail JPEG that is 190 pixels on its longest side.
The ruler and Macbeth color-calibration chart are cropped out of the frame for the three non-master images.

The file names indicate the derivative type through a “tag,” which is the last segment of the file name before the extension .tif or .jpg. The tag is 300 for the 300 PPI TIFF, sap for the SAP JPEG, thumb for the thumbnail JPEG, or a number between 600 and 1200 for the archival TIFF.

The following file names are for the 300 PPI TIFF and standard all-purpose and thumbnail JPEG images for W.583, image serial no. 1:

W583_000001_300.tif
W583_000001_sap.jpg
W583_000001_thumb.jpg
For archival master images, the tag indicates the image’s resolution. These master TIFF image names for W.579 show this:

W579_000001_1171.tif
W579_000002_1200.tif
W579_000003_1168.tif
W579_000004_600.tif
W579_000005_600.tif
Text pages are captured at 600 pixels per inch. Illuminated and decorated parts of manuscripts are captured at 1200 pixels per inch, or the highest resolution possible, when the size of the object prohibits capture at 1200.

FINDING THE FILE YOU WANT
Image order and image subject names are made available in three ways. First, each manuscript’s web page lists the pieces in order with the piece name (“folio 1a”, “front flyleaf 1a”, etc.) and associated file names, as can be seen here:

http://www.thedigitalwalters.org/Data/WaltersManuscripts/html/W579/
Second, each manuscript is shipped to the site with a detailed metadata file describing all the manuscript’s delivered images, for example:

http://thedigitalwalters.org/Data/WaltersManuscripts/W579/data/metadata.xml
This file’s <image> element contains each item’s order, name, and associated file names:

Order is mapped to: /manuscript/images/image/index
Item name is mapped to: /manuscript/images/image/image_subject
The master file image name is mapped to: /manuscript/images/image/jhoveData/jhove:jhove/repinfo/@uri
For example:

    <?xml version="1.0" encoding="UTF-8"?>
    <manuscript xmlns="http://www.thewalters.org/ns/mss-manifest/1.0/"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:mix="http://www.loc.gov/mix/v20">
     <imaged_object>
       <!-- ... -->
     </imaged_object>
     <images>
      <image>
       <index>0</index>
       <image_subject>Upper board outside</image_subject>
       <!-- ... -->
       <jhoveData>
        <jhove xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xmlns="http://hul.harvard.edu/ois/xml/ns/jhove"
         xsi:schemaLocation="http://hul.harvard.edu/ois/xml/ns/jhove http://hul.harvard.edu/ois/xml/xsd/jhove/1.5/jhove.xsd"
         name="Jhove" release="1.4" date="2009-07-30">
         <date>2009-11-04T11:45:40-05:00</date>
         <repInfo uri="W.579/master/W579_000001_1171.tif">
         <!-- ... -->
This XSL transformation: metadata_to_html.xsl can be used to extract piece and file names from any metadata.xml file.

Finally, for those manuscripts whose TEI manuscript description has been published to the site, all items are listed in order, by name in the TEI file’s <facsimile> section. Note this excerpt from W579_tei.xml:

    <facsimile xml:id="n216.055872">
      <surface n="Upper board outside" xml:id="n216.055421">
        <graphic url="master/W579_000001_1171.tif" xml:id="n216.055422"/>
        <graphic url="300/W579_000001_300.tif" xml:id="n216.055423"/>
        <graphic url="sap/W579_000001_sap.jpg" xml:id="n216.055424"/>
        <graphic url="thumb/W579_000001_thumb.jpg" xml:id="n216.055425"/>
      </surface>
      <surface n="Upper board inside" xml:id="n216.055426">
        <graphic url="master/W579_000002_1200.tif" xml:id="n216.055427"/>
        <graphic url="300/W579_000002_300.tif" xml:id="n216.055428"/>
        <graphic url="sap/W579_000002_sap.jpg" xml:id="n216.055429"/>
        <graphic url="thumb/W579_000002_thumb.jpg" xml:id="n216.055430"/>
      </surface>
      <surface n="Front flyleaf ia flap closed" xml:id="n216.055431">
        <graphic url="master/W579_000003_1168.tif" xml:id="n216.055432"/>
        <graphic url="300/W579_000003_300.tif" xml:id="n216.055433"/>
        <graphic url="sap/W579_000003_sap.jpg" xml:id="n216.055434"/>
        <graphic url="thumb/W579_000003_thumb.jpg" xml:id="n216.055435"/>
      </surface>
      <surface n="Front flyleaf ia" xml:id="n216.055436">
        <graphic url="master/W579_000004_600.tif" xml:id="n216.055437"/>
        <graphic url="300/W579_000004_300.tif" xml:id="n216.055438"/>
        <graphic url="sap/W579_000004_sap.jpg" xml:id="n216.055439"/>
        <graphic url="thumb/W579_000004_thumb.jpg" xml:id="n216.055440"/>
      </surface>
      <!-- ... -->
    </facsimile>
MANUSCRIPT PACKAGING & PRESERVATION METADATA
For delivery to the Digital Walters and other recipients, the Walters uses BagIt. BagIt is a packaging format that distinguishes delivered data, the BagIt “payload,” from supporting metadata, the “tags” used to ensure the integrity of the delivered payload.

Manuscript data on this website is found in bags that have this structure:

    W579/
     |--- bag-info.txt                  # description of the data package
     |--- bagit.txt                     # bagit protocol version, text encoding
     |--- manifest-md5.txt              # list of payload files with check sums
     |--- tagmanifest-md5.txt           # list of BagIt files with check sums
     |--- data/                         # the manuscript data proper
           |--- metadata.xml            # preservation metadata for image files
           |--- W.579/
                 |--- 300/              # 300 PPI TIFF images
                 |     |--- W579_000001_300.tif
                 |     |--- W579_000002_300.tif
                 |     |--- W579_000003_300.tif
                 |     |--- ...
                 |--- master/           # master archival images
                 |     |--- W579_000001_1171.tif
                 |     |--- W579_000002_1200.tif
                 |     |--- W579_000003_1168.tif
                 |     |--- ...
                 |--- sap/              # standard-all-purpose JPEG images
                 |     |--- W579_000001_sap.jpg
                 |     |--- W579_000002_sap.jpg
                 |     |--- W579_000003_sap.jpg
                 |     |--- ...
                 |--- thumb/            # thumbnail JPEG images
                       |--- W579_000001_thumb.jpg
                       |--- W579_000002_thumb.jpg
                       |--- W579_000003_thumb.jpg
                       |--- ...
The tag files are found in the top-level directory of the bag, W579. These include a manifest of the included files with checksums, and information about the bag. The payload is in the data directory. It contains preservation metadata, in the metadata.xml file, and a directory of images, in this case W.579. Within this directory are folders for each of the derivative types: 300 for the 300 PPI TIFFs, master for the archival TIFFs, sap for the standard all-purpose JPEGs, and thumb for the thumbnail JPEGs.

The most important tag file is manifest-md5.txt, which lists all the files in the bag along with a check sum that can be used to check the integrity of the file. Its contents look like this:

    1f11da7f4086e45ae65c8a9f6819f6e1 data/W.579/master/W579_000009_1200.tif
    340dcee00a5f4882938a81efd9154310 data/W.579/master/W579_000001_1171.tif
    b82735d1bcf689aee7695bec411a3910 data/W.579/300/W579_000010_300.tif
    53fd20c4faa32a899b097427143cb3ee data/W.579/300/W579_000020_300.tif
    ...
See the following pages for more information and tools for working with bags:

IETF draft BagIt specification
BagIt, on Wikipedia
Library of Congress BagIt transfer utilities
Checksum, on Wikipedia, with a list of checksum tools
A NOTE ON FOLDER NAMES
Note the difference between the shelf mark folders for W.579 in the above diagram. The top level directory is the shelf mark with the dot . character removed: W579. In the second instance, inside the data directory, the full shelf mark with the dot is used: W.579. This is the pattern for almost all manuscripts; for example,

    /Data/WaltersManuscripts/W4/data/W.4
    /Data/WaltersManuscripts/W595/data/W.595
    /Data/WaltersManuscripts/W624/data/W.624
    ...
There are ten exceptions to this rule. Early in the project, the dot ’.’ character was removed in both locations. Thus, we have for only these manuscripts:

    /Data/WaltersManuscripts/W555/data/W555
    /Data/WaltersManuscripts/W559/data/W559
    /Data/WaltersManuscripts/W582/data/W582
    /Data/WaltersManuscripts/W583/data/W583
    /Data/WaltersManuscripts/W585/data/W585
    /Data/WaltersManuscripts/W589/data/W589
    /Data/WaltersManuscripts/W591/data/W591
    /Data/WaltersManuscripts/W596/data/W596
    /Data/WaltersManuscripts/W615/data/W615
    /Data/WaltersManuscripts/W658/data/W658
PRESERVATION AND TECHNICAL METADATA
The metadata.xml file in each manuscript’s data directory, encodes extensive technical metadata for each manuscript. The structure of the file is specified by the schema, idr-manifest.xsd, which can be found at /Supplemental/XML/schemas/idr-manifest.xsd.

Each metadata.xml has this information:

/manuscript: top-level container of metadata for a manuscript’s images

/manuscript/image_object: description of the manuscript, primarily Dublin Core metadata, with the number of images captured in the imageCount element

/manuscript/images: container for the manuscript’s image data

/manuscript/images/image: information about a single capture and its derivatives, including:

/manuscript/images/image/index: the order of the image in the set, beginning with 0

/manuscript/images/image/image_subject: the folio number or name of the piece imaged

/manuscript/images/image/capture: detailed information about the image’s capture extracted from the imaging software database

/manuscript/images/image/masterDerivation: description of how the archival TIFF image was generated from the camera raw file, including cropping and color correction information

/manuscript/images/image/jhoveData: XML output of the JHOVE utility run on the archival TIFF file

/manuscript/images/image/derivative: three elements containing cropping and scaling information needed to generate the 300 PPI, SAP, and thumbnail files from the archival TIFF

JHOVE
JHOVE stands for “JSTOR/Harvard Object Validation Environment.” According to the project website, JHOVE “provides functions to perform format-specific identification, validation, and characterization of digital objects.”

The Walters uses JHOVE (version 1.4) to validate and extract complete TIFF metadata from master TIFF images in XML format. The -k flag is used to generate checksums for each file. This command is issued:

    > jhove.bat -h xml -m TIFF-hul -k FILE_NAME
The JHOVE XML output is included in its entirety in the <jhoveData> element for each image in the metadata.xml.

STANDARDS
Throughout, the Walters NEH-funded projects adhere to accepted international standards. The following is a list of the most important of those.

TIFF 6.0: all archival images adhere to the TIFF 6.0 specification

Dublin Core: each image includes descriptive Dublin Core metadata (see Dublin Core in the Read Me file for details)

TEI P5: manuscript description information is encoded according to Text Encoding Initiative (TEI) P5 guidelines (see the Manuscript Description file)
BagIt: images are packaged and delivered using the BagIt protocol (see above)

Unicode: text information in XML files and other text documents is in Unicode, typically with UTF-8 encoding
