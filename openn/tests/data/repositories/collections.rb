
require 'json'

data = {
        collections: [
                      {
                       tag: "pennmss",
                       metadata_type: "TEI",
                       live: true,
                       name: "Penn Manuscripts",
                       blurb: "These manuscripts are from the collections of the Rare Books and Manuscripts Library at the University of Pennsylvania or are hosted by Penn with the permission of their owners.  Penn holds over 2,000 Western manuscripts produced before the 19th century; medieval and Renaissance manuscripts comprise approximately 900 items, the earliest dating from 1000 A.D. The medieval manuscripts, now a collection of approximately 250 items, have been considered and used as a research collection since the private library of church historian Henry Charles Lea came to the University in the early 20th century. Most of the manuscripts are in Latin, but the medieval vernacular languages of Middle English, Middle French, Italian, Spanish, German, Dutch, and Judaeo-Arabic are each represented by one or more manuscripts. The collection is particularly strong in the fields of church history and history of science, with secondary strengths in liturgy and liturgical chant, theology and philosophy, and legal documents.",
                       include_file: "PennManuscripts.html"
                      },
                      {
                       tag: "ljs",
                       metadata_type: "TEI",
                       live: true,
                       name: "Lawrence J. Schoenberg Manuscripts",
                       blurb: "These manuscripts are from the Lawrence J. Schoenberg collection in the Rare Books and Manuscripts Library at the University of Pennsylvania.",
                       include_file: "LJSchoenbergManuscripts.html"
                      },
                      {
                       tag: "brynmawr",
                       metadata_type: "TEI",
                       live: false,
                       name: "Special Collections, Bryn Mawr College",
                       blurb: "Documents from Special Collections, Bryn Mawr College.",
                       include_file: "BrynMawrCollege.html"
                      },
                      {
                       tag: "drexarc",
                       name: "Drexel University Archives",
                       live: false,
                       blurb: "Documents from Drexel University Archives.",
                       include_file: "DrexelUniversity.html"
                      },
                      {
                       tag: "drexmed",
                       name: "Legacy Center Archives & Special Collection, Drexel University College of Medicine.",
                       live: false,
                       blurb: "Documents from the Legacy Center Archives & Special Collection, Drexel University College of Medicine.",
                       include_file: "DrexelMedicine.html"
                      },
                      {
                       tag: "haverford",
                       name: "Quaker and Special Collections, Haverford College",
                       live: false,
                       blurb: "Documents from Quaker and Special Collections, Haverford College.",
                       include_file: "HaverfordCollege.html"
                      },
                      {
                       tag: "lehigh",
                       name: "Special Collections, Lehigh University",
                       live: false,
                       blurb: "Documents from Special Collections, Lehigh University.",
                       include_file: "SpecialCollectionsLehighUniversity.html"
                      },
                      {
                       tag: "tlc",
                       name: "The Library Company of Philadelphia",
                       live: false,
                       blurb: "Documents from the Library Company of Philadelphia.",
                       include_file: "LibraryCompany.html"
                      },
                      {
                       tag: "libpa",
                       name: "Rare Collections Library, State Library of Pennsylvania",
                       live: false,
                       blurb: "Documents from the Rare Collections Library, State Library of Pennsylvania.",
                       include_file: "StateLibraryOfPennsylvania.html"
                      },
                      {
                       tag: "friendshl",
                       name: "Friends Historical Library, Swarthmare College",
                       live: false,
                       blurb: "Documents from the Friends Historical Library, Swarthmare College.",
                       include_file: "FriendsHistoricalLibrary.html"
                      },
                      {
                       tag: "hsp",
                       name: "Historical Society of Pennsylvania",
                       live: false,
                       blurb: "Documents from the Historical Society of Pennsylvania.",
                       include_file: "HistoricalSocietyOfPennsylvania.html"
                      },
                      {
                       tag: "lts",
                       name: "Lutheran Theological Seminary",
                       live: false,
                       blurb: "Documents from Lutheran Theological Seminary.",
                       include_file: "LutheranTheologicalSeminary.html"
                      },
                      {
                       tag: "ulp",
                       name: "Union League of Philadelphia",
                       live: false,
                       blurb: "Documents from the Union League of Philadelphia.",
                       include_file: "UnionLeagueOfPhiladelphia.html"
                      }
                     ],

        collection_validation: {
                                unique_fields: [
                                                "tag",
                                                "name",
                                                "include_file"
                                               ],
                                required_fields: [
                                                  "tag",
                                                  "live",
                                                  "name",
                                                  "blurb",
                                                  "include_file"
                                                 ]
                               }
       }

        puts JSON.generate(data)
