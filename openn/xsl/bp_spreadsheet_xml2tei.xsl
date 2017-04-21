<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns="http://www.tei-c.org/ns/1.0"
    xmlns:marc="http://www.loc.gov/MARC21/slim" exclude-result-prefixes="xs xd marc tei"
    version="2.0">
    <xd:doc scope="stylesheet">
        <xd:desc>
            <xd:p><xd:b>Created on:</xd:b> June 14, 2015</xd:p>
            <xd:p><xd:b>Author:</xd:b> emeryr</xd:p>
        </xd:desc>
    </xd:doc>
    <!-- TODO: metadata creator  -->
    <xsl:output indent="yes"/>
    <xsl:param name="project_path" required="yes"/>
    <xsl:variable name="bibliophilly-keywords-xml" select="concat($project_path,'/vendor/bibliophilly-keywords/bibliophilly-keywords.xml')"/>
    <xsl:variable name="repository">
        <xsl:call-template name="clean-up-text">
            <xsl:with-param name="some-text"
              select="//description/identification/repository_name"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="call_number">
        <xsl:call-template name="clean-up-text">
            <xsl:with-param name="some-text" select="//description/identification/full_call_number"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="volume_number">
      <xsl:call-template name="clean-up-text">
        <xsl:with-param name="some-text"
          select="//description/identification/volume_number"/>
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="ms_title">
        <xsl:call-template name="clean-up-text">
            <xsl:with-param name="some-text"
                select="//description/title/title"/>
        </xsl:call-template>
      <xsl:if test="//identification/volume_number">
        <xsl:text>, vol. </xsl:text>
        <xsl:value-of select="//identification/volume_number"></xsl:value-of>
      </xsl:if>
    </xsl:variable>
    <xsl:template match="/">
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title>
                            <xsl:value-of
                                select="normalize-space(concat('Description of ', $repository, ', ', $call_number, ': ', $ms_title))"
                            />
                        </title>
                      <xsl:if test="//contrib_cataloger">
                        <respStmt>
                          <resp>contributor</resp>
                          <persName><xsl:value-of select="//contrib_cataloger[1]/metadata_creator"/></persName>
                        </respStmt>
                      </xsl:if>
                      <xsl:for-each select="//contrib_cataloger">
                        <xsl:if test="position() &gt; 1">
                          <respStmt>
                            <resp>cataloger</resp>
                            <persName><xsl:value-of select="./metadata_creator"/></persName>
                          </respStmt>                          
                        </xsl:if>
                      </xsl:for-each>
                    </titleStmt>
                    <publicationStmt>
                        <publisher><xsl:value-of select="$repository"/></publisher>
                      <!-- If licence info present; generate license stanza(s). -->
                      <xsl:if test="//description/metadata_rights/legalcode_url | //description/metadata_rights/text | //description/image_rights/legalcode_url | //description/image_rights/text">
                        <availability>
                          <xsl:call-template name="license">
                            <xsl:with-param name="license_url" select="//description/metadata_rights/legalcode_url"/>
                            <xsl:with-param name="license_text" select="//description/metadata_rights/text"/>
                          </xsl:call-template>
                          <xsl:call-template name="license">
                            <xsl:with-param name="license_url" select="//description/image_rights/legalcode_url"/>
                            <xsl:with-param name="license_text" select="//description/image_rights/text"/>
                          </xsl:call-template>
                         </availability>
                      </xsl:if>
                    </publicationStmt>
                    <!-- DOT ADDED NOTESSTMT TO HOLD ALL THE RANDOM NOTES FROM THE MARC RECORD -->
                    <xsl:if test="//notes">
                      <notesStmt>
                        <xsl:for-each select="//notes/note/node()">
                          <note><xsl:value-of select="."/></note>
                        </xsl:for-each>
                        <xsl:for-each select="//related">
                          <note>
                            <xsl:if test="./related_resource_url">
                              <xsl:attribute name="target" select="./related_resource_url"/>
                            </xsl:if>
                            <xsl:value-of select="./related_resource"/>
                          </note>
                        </xsl:for-each>
                      </notesStmt>
                    </xsl:if>
                    <!-- END DOT MOD -->
                    <sourceDesc>
                        <msDesc>
                            <msIdentifier>
                              <xsl:if test="//identification/repository_country">
                                  <country>
                                    <xsl:value-of select="//identification/repository_country"/>
                                  </country>
                              </xsl:if>
                              <settlement><xsl:value-of select="//identification/repository_city"/></settlement>
                              <xsl:if test="//identification/repository_institution">
                                <institution>
                                  <xsl:value-of select="//identification/repository_institution"/>
                                </institution>
                              </xsl:if>
                                <repository>
                                    <xsl:value-of select="$repository"/>
                                </repository>
                                <xsl:for-each select="//identification/source_collection">
                                  <collection><xsl:value-of select="."/></collection>
                                </xsl:for-each>
                                <idno type="call-number">
                                    <xsl:value-of select="$call_number"/>
                                </idno>
                                <xsl:if test="//identification/record_url">
                                  <altIdentifier type="resource">
                                    <idno>
                                    <xsl:value-of select="//identification/record_url"/>
                                    </idno>
                                  </altIdentifier>
                                </xsl:if>
                                <xsl:for-each select="//altId">
                                  <altIdentifier>
                                    <xsl:if test="./alternate_id_type">
                                        <xsl:attribute name="type" select="./alternate_id_type"/>
                                    </xsl:if>
                                    <idno>
                                      <xsl:value-of select="./alternate_id"/>
                                    </idno>
                                  </altIdentifier>
                                </xsl:for-each>
                            </msIdentifier>
                            <msContents>
                              <xsl:if test="//description">
                                <summary>
                                    <xsl:value-of select="//summary/description"/>
                                </summary>
                              </xsl:if>
                                <xsl:if test="//language">
                                    <textLang>
                                      <xsl:attribute name="mainLang" select="//description/language[1]/language"/>
                                      <xsl:if test="count(//description/language) &gt; 1">
                                        <xsl:attribute name="otherLangs">
                                          <xsl:for-each select="//description/language">
                                            <xsl:if test="position() &gt; 1">
                                              <xsl:value-of select="language"/>
                                              <xsl:if test="position() != last()">
                                                <xsl:text> </xsl:text>
                                              </xsl:if>
                                            </xsl:if>
                                          </xsl:for-each>
                                        </xsl:attribute>
                                      </xsl:if>
                                      <xsl:call-template name="lang-names">
                                        <xsl:with-param name="langs" select="//description/language"/>
                                      </xsl:call-template>
<!--                                      TODO Add language name-->
                                    </textLang>
                                </xsl:if>
                                <msItem>
                                    <title>
                                        <xsl:call-template name="clean-up-text">
                                            <xsl:with-param name="some-text" select="//title/title" />
                                        </xsl:call-template>
                                    </title>
                                  <xsl:if test="//creator">
                                    <xsl:for-each select="//creator">
                                      <author>
                                        <xsl:if test="./creator_uri">
                                          <xsl:attribute name="ref">
                                          <xsl:value-of select="./creator_uri"/>
                                          </xsl:attribute>
                                        </xsl:if>
                                        <xsl:value-of select="./creator_name"/>
                                      </author>
                                    </xsl:for-each>
                                  </xsl:if>
                                  <xsl:for-each select="//translator">
                                    <xsl:call-template name="build_resp">
                                      <xsl:with-param name="resp">translator</xsl:with-param>
                                      <xsl:with-param name="personName" select="./translator_name"/>
                                      <xsl:with-param name="ref" select="./translator_uri"></xsl:with-param>
                                    </xsl:call-template>
                                  </xsl:for-each>
                                  <xsl:for-each select="//artist">
                                    <xsl:call-template name="build_resp">
                                      <xsl:with-param name="resp">artist</xsl:with-param>
                                      <xsl:with-param name="personName" select="./artist_name"/>
                                      <xsl:with-param name="ref" select="./artist_uri"></xsl:with-param>
                                    </xsl:call-template>
                                  </xsl:for-each>
                                  <xsl:for-each select="//former_owner">
                                    <xsl:call-template name="build_resp">
                                      <xsl:with-param name="resp">former owner</xsl:with-param>
                                      <xsl:with-param name="personName" select="./former_owner_name"/>
                                      <xsl:with-param name="ref" select="./former_owner_uri"></xsl:with-param>
                                    </xsl:call-template>
                                  </xsl:for-each>
                                  <xsl:if test="//colophon/colophon">
                                    <colophon>
                                      <xsl:value-of select="//colophon/colophon"/>
                                    </colophon>
                                  </xsl:if>
                                </msItem>
                              <xsl:for-each select="//tags/tag/name[matches(text(), '^TOC')]">
                                <xsl:variable name="locus" select="ancestor::page/display_page"/>
                                <msItem>
                                  <xsl:attribute name="n" select="$locus"/>
                                  <locus><xsl:value-of select="$locus"/></locus>
                                  <title><xsl:value-of select="parent::tag/value"/></title>
                                </msItem>
                              </xsl:for-each>
                            </msContents>
                          <physDesc>
                              <xsl:if test="//support | //supportDesc | //boundDim | //collation | //boundDim | //pageDim | //extent">
                                <objectDesc>
                                  <supportDesc>
                                    <xsl:if test="//support/support_material">
                                      <xsl:attribute name="material" select="//support/support_material"/>
                                    </xsl:if>
                                    <xsl:if test="//support">
                                      <support>
                                        <xsl:if test="//support/support_material">
                                        <p>
                                          <xsl:value-of select="//support/support_material"/>
                                        </p>
                                        </xsl:if>
                                        <xsl:for-each select="//support/watermarks">
                                          <watermark>
                                            <xsl:value-of select="."/>
                                          </watermark>
                                        </xsl:for-each>
                                      </support>
                                    </xsl:if>
                                    <xsl:if test="//boundDim | //pageDim | //extent">
                                      <extent>
                                        <xsl:if test="//extent/flyleaves_leaves">
                                          <xsl:value-of select="//extent/flyleaves_leaves"/><xsl:text>; </xsl:text>
                                        </xsl:if>
                                        <xsl:for-each select=" //pageDim/page_dimensions">
                                          <xsl:value-of select="."/><xsl:text> </xsl:text>
                                        </xsl:for-each>
                                        <xsl:if test="//boundDim/bound_dimensions">
                                          <xsl:text>bound to </xsl:text><xsl:value-of select="//boundDim/bound_dimensions"/>
                                        </xsl:if>
                                      </extent>
                                    </xsl:if>
                                    <xsl:if test="//supportDesc/pagination_foliation">
                                      <foliation>
                                        <xsl:value-of select="//supportDesc/pagination_foliation"></xsl:value-of>
                                      </foliation>
                                    </xsl:if>
                                    <xsl:if test="//collation/collation">
                                      <collation>
                                        <p>
                                          <xsl:value-of select="//collation/collation"/>
                                        </p>
                                        <xsl:if test="//collation/signatures">
                                        <p>
                                          <signatures>
                                            <xsl:value-of select="//collation/signatures"/>
                                          </signatures>
                                        </p>
                                       </xsl:if>
                                       <xsl:if test="//collation/catchwords">
                                         <p>
                                           <catchwords>
                                           <xsl:value-of select="//collation/catchwords"/>
                                           </catchwords>
                                         </p>
                                       </xsl:if>
                                      </collation>
                                    </xsl:if>
                                  </supportDesc>
                                <xsl:if test="//layout/layout">
                                  <layoutDesc>
                                    <layout><xsl:value-of select="//layout/layout"/></layout>
                                  </layoutDesc>
                                </xsl:if>
                                </objectDesc>
                              </xsl:if>
                              <xsl:if test="//scriptNote/script">
                                <scriptDesc>
                                  <xsl:for-each select="//scriptNote/script">
                                  <scriptNote><xsl:value-of select="."/></scriptNote>
                                  </xsl:for-each>
                                </scriptDesc>
                              </xsl:if>
                            <xsl:if test="//decoNote/decoration | //tags/tag/name[text() = 'ILL']">
                              <decoDesc>
                                <xsl:if test="//decoNote/decoration">
                                  <decoNote>
                                    <xsl:value-of select="//decoNote/decoration"/>
                                  </decoNote>
                                </xsl:if>
                                <xsl:for-each select="//tags/tag/name[text() = 'ILL']">
                                   <decoNote>
                                     <xsl:attribute name="n">
                                       <xsl:value-of select="ancestor::page/display_page/text()"/>
                                     </xsl:attribute>
                                     <xsl:value-of select="ancestor::tag/value"/>
                                   </decoNote>
                                </xsl:for-each>
                              </decoDesc>
                              </xsl:if>
                              <xsl:if test="//binding/binding">
                                <bindingDesc>
                                  <binding>
                                    <p>
                                      <xsl:value-of select="//binding/binding"/>
                                    </p>
                                  </binding>
                                </bindingDesc>
                              </xsl:if>
                            </physDesc>
                            <history>
                              <xsl:if test="//origin">
                                <xsl:variable name="date_string" select="//origin/date_narrative"/>
                                <xsl:variable name="date_when" select="//origin/date_single"/>
                                <xsl:variable name="date_notAfter" select="//origin/date_range_end"/>
                                <xsl:variable name="date_notBefore" select="//origin/date_range_start"/>
                                <xsl:variable name="orig_place" select="//origin/place_of_origin"/>
                                <xsl:variable name="orig_details" select="//origin/origin_details"/>
                                <origin>
                                  <xsl:if test="//origin/origin">
                                    <p>
                                      <xsl:value-of select="normalize-space(substring(.,8))"/>
                                    </p>
                                  </xsl:if>
                                  <xsl:variable name="o" select="//origin"/>
                                  <xsl:if test="$date_string or $date_when or $date_notBefore or $date_notAfter">
                                    <origDate>
                                      <xsl:choose>
                                        <xsl:when test="$date_when">
                                          <xsl:attribute name="when" select="$date_when"/>
                                        </xsl:when>
                                        <xsl:when test="$date_notBefore">
                                          <xsl:attribute name="notBefore" select="$date_notBefore"/>
                                          <xsl:attribute name="notAfter" select="$date_notAfter"/>
                                        </xsl:when>
                                      </xsl:choose>
                                      <xsl:choose>
                                        <xsl:when test="$date_string">
                                          <xsl:value-of select="$date_string"/>
                                        </xsl:when>
                                        <xsl:when test="$date_when">
                                          <xsl:value-of select="$date_when"/>
                                        </xsl:when>
                                        <xsl:when test="$date_notBefore and $date_notAfter">
                                          <xsl:text>Between </xsl:text>
                                          <xsl:value-of select="$date_notBefore"/>
                                          <xsl:text> and </xsl:text>
                                          <xsl:value-of select="$date_notAfter"/>
                                        </xsl:when>
                                      </xsl:choose>
                                    </origDate>
                                  </xsl:if>
                                  <xsl:if test="$orig_place">
                                    <xsl:for-each select="//place_of_origin">
                                    <origPlace>
                                      <xsl:value-of select="."/>
                                    </origPlace>
                                    </xsl:for-each>
                                  </xsl:if>
                                  <xsl:if test="$orig_details">
                                    <p><xsl:value-of select="$orig_details"/></p>
                                  </xsl:if>
                                </origin>
                              </xsl:if>
                              <xsl:if test="//provenance/provenance_details">
                                <provenance><xsl:value-of select="//provenance/provenance_details"/></provenance>
                              </xsl:if>
                            </history>
                        </msDesc>
                    </sourceDesc>
                </fileDesc>
<!--              <xsl:value-of select="$bibliophilly-keywords-xml"/>-->
              <xsl:copy-of select="document($bibliophilly-keywords-xml)"/>
                <!-- DOT ADDED KEYWORDS FOR SUBJECTS AND GENRE/FORM -->
              <profileDesc>
                <textClass>
                  <!-- DE: Switching to marc 610 and joining subfields -->
                  <xsl:if test="//subjects_keywords">
                    <keywords n="keywords">
                      <xsl:for-each select="//subjects_keywords">
                        <term>
                          <xsl:call-template name="chomp-period">
                            <xsl:with-param name="string" select="./subject_keyword"/>
                          </xsl:call-template>
                        </term>
                      </xsl:for-each>
                    </keywords>
                  </xsl:if>
                  <xsl:if test="//subjects_topical | //subjects_names | //subjects_geographic">
                    <keywords n="subjects">
                      <xsl:for-each select="//subjects_topical">
                        <term>
                          <xsl:if test="./subject_topical_uri">
                            <xsl:attribute name="target">
                              <xsl:value-of select="./subject_topical_uri"/>
                            </xsl:attribute>
                          </xsl:if>
                          <xsl:call-template name="chomp-period">
                            <xsl:with-param name="string" select="./subject_topical"/>
                          </xsl:call-template>
                        </term>
                      </xsl:for-each>
                      <xsl:for-each select="//subjects_geographic">
                        <term>
                          <xsl:if test="./subject_geographic_uri">
                            <xsl:attribute name="target">
                              <xsl:value-of select="./subject_geographic_uri"/>
                            </xsl:attribute>
                          </xsl:if>
                          <xsl:call-template name="chomp-period">
                            <xsl:with-param name="string" select="./subject_geographic"/>
                          </xsl:call-template>
                        </term>
                      </xsl:for-each>
                      <xsl:for-each select="//subjects_names">
                        <term>
                          <xsl:if test="./subject_names_uri">
                            <xsl:attribute name="target">
                              <xsl:value-of select="./subject_names_uri"/>
                            </xsl:attribute>
                          </xsl:if>
                          <xsl:call-template name="chomp-period">
                            <xsl:with-param name="string" select="./subject_names"/>
                          </xsl:call-template>
                        </term>
                      </xsl:for-each>
                    </keywords>
                  </xsl:if>
                  <xsl:if test="//subjects_genreform">
                    <keywords n="form/genre">
                      <xsl:for-each select="//subjects_genreform">
                        <term>
                          <xsl:if test="./subject_genreform_uri">
                            <xsl:attribute name="target">
                              <xsl:value-of select="./subject_genreform_uri"/>
                            </xsl:attribute>
                          </xsl:if>
                          <xsl:call-template name="chomp-period">
                            <xsl:with-param name="string" select="./subject_genreform"/>
                          </xsl:call-template>
                        </term>
                      </xsl:for-each>
                    </keywords>
                  </xsl:if>
                </textClass>
              </profileDesc>
              <!-- DOT MOD ENDS HERE -->
            </teiHeader>
            <facsimile>
                <!--
                    <xsl:for-each select="//xml[@name='pages']/page">
                    <surface>
                    <xsl:attribute name="n">
                    <xsl:call-template name="clean-up-text">
                    <xsl:with-param name="some-text">
                    <xsl:value-of select="./@visiblepage"/>
                    </xsl:with-param>
                    </xsl:call-template>
                    </xsl:attribute>
                    <graphic url="{concat(./@image, '.tif')}"/>
                    </surface>
                    </xsl:for-each>
                -->
                <graphic url=""/>
            </facsimile>
        </TEI>
    </xsl:template>
    <xsl:template name="clean-up-text">
        <xsl:param name="some-text"/>
        <xsl:value-of select="normalize-space(replace(replace(replace($some-text, '[\[\]]', ''), ' \)', ')'), ',$',''))" />
    </xsl:template>
    <xsl:template name="chomp-period">
        <xsl:param name="string"/>
        <xsl:value-of select="replace(normalize-space($string), '\.$', '')"/>
    </xsl:template>
    <xsl:template name="lang-names">
        <xsl:param name="langs" as="node()*"/>
          <xsl:if test="count($langs) &gt; 0">
            <xsl:text>Primary language: </xsl:text>
            <xsl:value-of select="normalize-space($langs[1]/language_name)"/>
            <xsl:choose>
              <xsl:when test="count($langs) = 2">
                <xsl:text>. Secondary language: </xsl:text>
                <xsl:value-of select="normalize-space($langs[2]/language_name)"/>
              </xsl:when>
              <xsl:when test="count($langs) &gt; 2">
                <xsl:text>. Secondary languages: </xsl:text>
                <xsl:for-each select="$langs">
                  <xsl:if test="position() &gt; 1">
                    <xsl:value-of select="language_name"/>
                    <xsl:if test="position() != last()">
                      <xsl:text>; </xsl:text>
                    </xsl:if>
                  </xsl:if>
                </xsl:for-each>
              </xsl:when>
            </xsl:choose>
            <xsl:text>.</xsl:text>
          </xsl:if>
    </xsl:template>
    <xsl:template name="join-keywords">
        <xsl:param name="datafield"/>
        <xsl:call-template name="chomp-period">
            <xsl:with-param name="string">
                <xsl:for-each select="./marc:subfield">
                    <xsl:value-of select="."/>
                    <xsl:if test="position() != last()">
                        <xsl:text>--</xsl:text>
                    </xsl:if>
                </xsl:for-each>
            </xsl:with-param>
        </xsl:call-template>
    </xsl:template>
    <xsl:template name="join-genre">
        <xsl:param name="datafield"/>
        <xsl:call-template name="chomp-period">
            <xsl:with-param name="string">
                <xsl:for-each select="./marc:subfield[matches(@code, '[abcvxyz]')]">
                    <xsl:value-of select="."/>
                    <xsl:if test="position() != last()">
                        <xsl:text>--</xsl:text>
                    </xsl:if>
                </xsl:for-each>
            </xsl:with-param>
        </xsl:call-template>
    </xsl:template>
  <xsl:template name="join-text">
    <xsl:param name="items"/>
    <xsl:param name="sep"/>
        <xsl:for-each select="$items">
          <xsl:value-of select="."/>
          <xsl:if test="position() != last()">
            <xsl:value-of select="$sep"/>
          </xsl:if>
        </xsl:for-each>
  </xsl:template>
  <!-- Extract personal names, employing the date if present. -->
    <xsl:template name="extract-pn">
        <xsl:param name="datafield"/>
        <xsl:call-template name="chomp-period">
            <xsl:with-param name="string">
                <xsl:for-each select="$datafield/marc:subfield[@code='a' or @code='b' or @code='c' or @code='d']">
                    <xsl:value-of select="."/>
                    <xsl:if test="position() != last()">
                        <xsl:text> </xsl:text>
                    </xsl:if>
                </xsl:for-each>
            </xsl:with-param>
        </xsl:call-template>
    </xsl:template>
    <xsl:template name="other-langs">
        <xsl:param name="tags"/>
        <xsl:for-each select="$tags">
            <xsl:if test="position() > 1">
                <xsl:value-of select="."/>
                <xsl:if test="position() != last()">
                    <xsl:text> </xsl:text>
                </xsl:if>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>
    <!-- Generate a license stanza if license_url or license_text are present. -->
    <xsl:template name="license">
      <xsl:param name="license_url"/>
      <xsl:param name="license_text"/>
      <xsl:if test="$license_url | $license_text">
        <licence>
          <xsl:if test="$license_url">
            <xsl:attribute name="target" select="$license_url"/>
          </xsl:if>
          <xsl:if test="$license_text">
            <xsl:value-of select="$license_text"/>
          </xsl:if>
        </licence>
      </xsl:if>
    </xsl:template>
    <xsl:template name="build_resp">
      <xsl:param name="resp"/>
      <xsl:param name="personName"/>
      <xsl:param name="ref"/>
      <respStmt>
        <resp><xsl:value-of select="$resp"/></resp>
        <persName>
          <xsl:if test="$ref">
            <xsl:attribute name="ref">
              <xsl:value-of select="$ref"/>
            </xsl:attribute>
          </xsl:if>
          <xsl:value-of select="$personName"/>
        </persName>
      </respStmt>
    </xsl:template>
</xsl:stylesheet>