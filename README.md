OPenn scripts
=============

## Workflow

#### High level

- Create package (metadata, derivs, manifest, TEI, browse HTML, desc'n HTML)

- Update TOC file

- Push packages and update indices

#### Proposed package creation process

The package generation script will be called like this:

       $ create_pkg COLLECTION SOURCE_DIR

Where `COLLECTION` is a name of collection and indicates that the `SOURCE_DIR`
will have a particular known format and can be processed according to a known
set of rules. Each collection will have its data arrive in a certain directory
structure and have particular source or format for its metadata (e.g., Penn in
Hand XML metadata).

This script will create a comple package having this format:

    CALL_NUMBER/
      manifest.txt
      metadata.xml
      data/
        master/
        thumb/
        web/
        CALL_NUMBER_TEI.xml
        description.html
        browse.html


The package generation will occur in two steps:

1. COLLECTION specific preparation; this will take input data and return a 
   directory structure as follows:

        CALL_NUMBER/
          PARTIAL_TEI.xml # lacks facsimile section
          file_list.json  # list of all files with labels
          data/
            image1.tif
            image2.tif
            ...

2. The common process will take the prepared directory, and
      - rename the files using the project format: (0001_0000.tif,
        0001_0001.tif, 0001_0002.tif, ...)
      - move the files into data/master
      - create thumbnail and web JPEG derivatives in thumb and web, resp.
      - add to the file list the new file names
      - append the facsimile section to the TEI file, outputting
        `data/<CALL_NUMBER>_TEI.xml`
      - generate description.html
      - generate browse.html





- ID MS

- Copy images to scratch disk

- Fetch XML (need BibID and call number)

- Get new file names
    - Extract file names from XML
    - Compare files names to images on disk
    - Create map of original filenames and new file names
        - New file name pattern will be `"%d_%06d.tif" % (bibid, serial_num)`

- Rename files and generate derivatives
    - TIFF, unchanged
    - SAP JPEG, 1800 px on longest side
    - thumb JPEG, 190 px on longest side
    - Capture image dimensions

- Generate TEI from XML
    - Have to figure out how to add correct file names to TEI

- Generate HTML manuscript description from XML TEI

- Generate HTML browse
    - Links to images with sizes
    - Ordered by page
    - With page numbers
    - Thumbnails?
    - Multiple pages?

- Technical metadata?

- Construct archive
    - Images
    - TEI XML
    - HTML description?
    - Browse page

- Add manifest

- Update Table of contents page

- Push data


## High level overview
