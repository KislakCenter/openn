<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
  xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns="http://www.tei-c.org/ns/1.0"
  xmlns:marc="http://www.loc.gov/MARC21/slim" exclude-result-prefixes="xs xd marc tei" version="2.0">
  <xsl:import href="openn_templates.xsl"/>
  <xd:doc scope="stylesheet">
    <xd:desc>
      <xd:p><xd:b>Created:</xd:b> 2018</xd:p>
      <xd:p><xd:b>Author:</xd:b> emeryr</xd:p>
    
    </xd:desc>
  </xd:doc>
  <xsl:output indent="yes"/>
  <xsl:variable name="institution" select="//description/identification/repository_institution"/>
  <xsl:variable name="repository" select="//description/identification/repository_name"/>
  <xsl:variable name="call_number" select="//description/identification/call_numberid"/>
  <xsl:variable name="book_title" select="//description/title/title"/>
  <xsl:variable name="all_titles">
    <xsl:call-template name="join-text">
      <xsl:with-param name="nodes" select="//description/title/title"/>
      <xsl:with-param name="separator" select="'; '"/>
    </xsl:call-template>
  </xsl:variable>
  
  <xsl:variable name="tei_title">
    <xsl:variable name="tmp_title">
      <xsl:value-of select="$institution"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="$call_number"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="$all_titles"/>
    </xsl:variable>
    <xsl:value-of select="normalize-space($tmp_title)"/>
  </xsl:variable>
  
  <xsl:template match="/">
    <TEI xmlns="http://www.tei-c.org/ns/1.0">
      <teiHeader>
        <fileDesc>
          <titleStmt>
            <title>
              <xsl:value-of select="$tei_title"/>
            </title>
            <xsl:for-each select="//author">
              <author>
                <xsl:if test="./author_uri">
                <xsl:attribute name="ref" select="./author_uri"/>
                </xsl:if>
                <xsl:value-of select="./author_name"/>
              </author>
            </xsl:for-each>
            <xsl:for-each select="//translator">
              <respStmt>
                <resp>translator</resp>
                <name>
                  <xsl:if test="./translator_uri">
                    <xsl:attribute name="ref" select="./translator_uri"/>
                  </xsl:if>
                  <xsl:value-of select="./translator_name"/>
                </name>
              </respStmt>
            </xsl:for-each>
            <xsl:for-each select="//artist">
              <respStmt>
                <resp>artist</resp>
                <name>
                  <xsl:if test="./artist_uri">
                    <xsl:attribute name="ref" select="./artist_uri"/>
                  </xsl:if>
                  <xsl:value-of select="./artist_name"/>
                </name>
              </respStmt>
            </xsl:for-each>
          </titleStmt>
          <publicationStmt>
            <!-- Need a publisher: <publisher>The University of Pennsylvania Libraries</publisher>-->
            <publisher>PLACEHOLDER</publisher>
            <date>
              <xsl:attribute name="when">
                <xsl:value-of select="year-from-date(current-date())"/>
              </xsl:attribute>
            </date>
          </publicationStmt>
          <sourceDesc>
            <biblStruct>
              <monogr>
                <xsl:for-each select="//author">
                  <author>
                    <xsl:if test="./author_uri">
                      <xsl:attribute name="ref" select="./author_uri"/>
                    </xsl:if>
                    <xsl:value-of select="./author_name"/>
                  </author>
                </xsl:for-each>
                <xsl:for-each select="//translator">
                  <author>
                    <xsl:if test="./translator_uri">
                      <xsl:attribute name="ref" select="./translator_uri"/>
                    </xsl:if>
                    <xsl:value-of select="./translator_name"/>
                  </author>
                </xsl:for-each>
                <xsl:for-each select="//artist">
                  <author>
                    <xsl:if test="./artist_uri">
                      <xsl:attribute name="ref" select="./artist_uri"/>
                    </xsl:if>
                    <xsl:value-of select="./artist_name"/>
                  </author>
                </xsl:for-each>
                <xsl:for-each select="/doc/description/title">
                  <title>
                    <xsl:value-of select="./title"/>
                    <xsl:if test="./volume_number">
                      <xsl:text>, </xsl:text>
                      <xsl:value-of select="./volume_number"/>
                    </xsl:if>
                  </title>
                </xsl:for-each>
                <xsl:for-each select="/doc/description/edition">
                  <edition>
                    <xsl:value-of select="./edition"/>
                  </edition>
                </xsl:for-each>
                <imprint>
                  <xsl:for-each select="//publication">
                    <xsl:if test="./printer_publisher">
                      <publisher>
                        <name>
                        <xsl:if test="./printer_publisher_uri">
                          <xsl:attribute name="ref" select="./printer_publisher_uri"/>
                        </xsl:if>
                        <xsl:value-of select="./printer_publisher"/>
                        </name>
                      </publisher>
                    </xsl:if>
                    <xsl:if test="./place_of_publication">
                      <pubPlace>
                        <xsl:if test="./place_of_publication_uri">
                          <xsl:attribute name="ref" select="./place_of_publication_uri"/>
                        </xsl:if>
                        <xsl:value-of select="./place_of_publication"/>
                      </pubPlace>
                    </xsl:if>
                    <date>
                      <xsl:choose>
                        <xsl:when test="./date_single">
                          <xsl:attribute name="when" select="./date_single"/>
                        </xsl:when>
                        <xsl:otherwise>
                          <xsl:if test="./date_range_start">
                            <xsl:attribute name="from" select="./date_range_start"/>
                          </xsl:if>
                          <xsl:if test="./date_range_end">
                            <xsl:attribute name="to" select="./date_range_end"/>
                          </xsl:if>
                        </xsl:otherwise>
                      </xsl:choose>
                      <xsl:call-template name="standalone-date-string">
                        <xsl:with-param name="node" select="."/>
                      </xsl:call-template>
                    </date>
                  </xsl:for-each>
                </imprint>
                <xsl:if test="/doc/description/extent">
                  <extent>
                    <xsl:if test="/doc/description/extent/extent">
                      <xsl:value-of select="/doc/description/extent/extent"/>
                    </xsl:if>
                    <xsl:if test="/doc/description/extent/dimensions">
                      <dimensions>
                        <dim>
                          <xsl:value-of select="/doc/description/extent/dimensions"/>
                        </dim>
                      </dimensions>
                    </xsl:if>
                  </extent>
                </xsl:if>
              </monogr>
              <xsl:if test="//series">
                <series>
                  <title>
                    <xsl:value-of select="//series/series_title"/>
                  </title>
                </series>
              </xsl:if>
              <xsl:for-each select="//notes/note">
                <note>
                  <xsl:value-of select="normalize-space()"/>
                </note>
              </xsl:for-each>
              <idno>
                <xsl:attribute name="type">
                  <xsl:text>LC_call_number</xsl:text>
                </xsl:attribute>
                <xsl:value-of select="$call_number"/>
              </idno>
              <xsl:for-each select="//altId">
                <idno>
                  <xsl:attribute name="type" select="./alternate_id_type"/>
                  <xsl:value-of select="alternate_id"/>
                </idno>
              </xsl:for-each>
                <xsl:for-each select="//marc:datafield[@tag=740]">
                  <relatedItem>
                    <bibl>
                      <xsl:element name="title">
                        <xsl:call-template name="chopPunctuation">
                          <xsl:with-param name="chopString">
                            <xsl:value-of select="."/>
                          </xsl:with-param>
                        </xsl:call-template>
                      </xsl:element>
                    </bibl>
                  </relatedItem>
                </xsl:for-each>
            </biblStruct>
          </sourceDesc>
        </fileDesc>
        <encodingDesc>
          <classDecl>
          <taxonomy xml:id="LCC"><bibl>Library of Congress Classification</bibl></taxonomy>
          <taxonomy xml:id="LCSH"><bibl>Library of Congress Subject Headings</bibl></taxonomy>
          </classDecl>
        </encodingDesc>
        <profileDesc>
          <xsl:if test="/doc/description/language">
            <langUsage>
              <xsl:for-each select="/doc/description/language">
                <language>
                  <xsl:if test="./language">
                    <xsl:attribute name="ident" select="./language"/>
                  </xsl:if>
                  <xsl:if test="./language_name">
                    <xsl:value-of select="./language_name"/>
                  </xsl:if>
                </language>
              </xsl:for-each>
            </langUsage>
          </xsl:if>
          <textClass>
            <xsl:if test="/doc/description/subjects_names|/doc/description/subjects_geographic|/doc/description/subjects_topical">
              <keywords n="subjects">
                <xsl:for-each select="/doc/description/subjects_names|/doc/description/subjects_geographic|/doc/description/subjects_topical">
                  <term>
                    <xsl:if test="./subject_topical_uri | ./subject_geographic_uri | ./subject_names_uri">
                      <xsl:attribute name="target" select="./subject_topical_uri | ./subject_geographic_uri | ./subject_names_uri"/>
                    </xsl:if>
                    <xsl:value-of select="./subject_topical | ./subject_geographic | ./subject_names"/>
                  </term>
                </xsl:for-each>
              </keywords>
            </xsl:if>
            <xsl:if test="/doc/description/subjects_genreform">
              <keywords n="form/genre">
                <xsl:for-each select="/doc/description/subjects_genreform">
                  <term>
                    <xsl:if test="./subject_genreform_uri">
                      <xsl:attribute name="target" select="./subject_genreform_uri"/>
                    </xsl:if>
                    <xsl:value-of select="./subject_genreform"/>
                  </term>
                </xsl:for-each>
              </keywords>
            </xsl:if>
          </textClass>
        </profileDesc>
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
</xsl:stylesheet>