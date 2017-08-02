# Tasks

## Incoming

genizah.json
 x -- Make MD creator not required
 x -- Add scribe name, scribe uri
 x -- Make provenance repeatable

 genizah_spreadsheet_xml2tei.xsl
 x -- Add scribe name
 x -- Add scribe URI
 x -- Handle repeated provenance

 bibliophilly.json
 x -- Make 'Subject: keywords' required


## Repositories, collections

- Projects CSV
  + Single project taks
  + All projects

- Projects html = curated_collections.html

- rename collections.html to repositories.html
- curated_collections.html
-
- HTML for each project/curated collections
- CSV for each project/curated collections
<!-- - CSV for each repository -->

# Deploy

Re-run config
Update op-todo items, coll_config -> repo_config

BibPhilly changes
- Add metadata creator to spreadsheet to XML code as TEI <resp>Project
  Cataloger</resp>, <resp>Inst'l cataloger</resp> --- language to be
  determined
- Add author to pages spreadsheet
- Add author @ref to XSL
- Creator name optional for BibPhilly
- Create BibPhilly JSON for spreadsheet generation

x Update browse HTML to incorporate new TEI values -- done
x Update test DB fixtures to match new TEI -- done
x Complete test data for new pih2tei.xsl:

x- Update openn/tests/data/           -- done
x
x        mscodex1223_prepped/         -- done
x        mscodex1589_prepped/         -- done
x        mscodex1223_complete/        -- done
x        mscodex1589_complete/        -- removed

x- run all tests with new pih2tei.xsl -- done
