OPenn scripts
=============

## Workflow

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