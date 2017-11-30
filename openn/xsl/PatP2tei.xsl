<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns="http://www.tei-c.org/ns/1.0"
    xmlns:marc="http://www.loc.gov/MARC21/slim" exclude-result-prefixes="xs xd marc tei"
    version="2.0">
    <xd:doc scope="stylesheet">
        <xd:desc>
            <xd:p><xd:b>Created on:</xd:b> Nov 19, 2013</xd:p>
            <xd:p><xd:b>Author:</xd:b> emeryr</xd:p>
            <xd:p> * title * creator (s) * date of origin * place of origin * summary/abstract *
                foliation so we can generate page labels * language(s) * item level content, if
                applicable, is optional </xd:p>
            <xd:p>
                <xd:b>dorp, October 27 2014, modified to add</xd:b>
            </xd:p>
            <xd:p> * provenance * subject terms * genre/form terms * notes</xd:p>
            <xd:p>
                <xd:b>rde, October 28, 2014, multiple chagnes</xd:b>
            </xd:p>
            <xd:p>Pulling data from marc fields, instead of Penn in Hand "*_field" elements</xd:p>
            <xd:p>Tighten code; remove mid-tag line breaks</xd:p>
            <xd:p><xd:b>dorp, January 23 2015, modified to add</xd:b></xd:p>
            <xd:p> *Foliation *Layout *Colophon *Collation *Script *Decoration *Binding *Origin *Watermarks *Signatures</xd:p>
            <xd:p><xd:b>emeryr, January 27 2015, fix bugs, tighten code to</xd:b></xd:p>
            <xd:p> prefer for-each elements to if/for-each combinations where possible</xd:p>
            <xd:p><xd:b>emeryr, February 5, 2015, modified to add</xd:b></xd:p>
            <xd:p> *Pagination; treated as *Foliation</xd:p>
        </xd:desc>
    </xd:doc>
<!--
    DE: Note that below I'm not consistent about marking the source marc field as @type.
      That's coming from a template I've copied *some* stuff from.-->
<!-- DE: I haven't looked at the title@level attribute. Need to figure out when to use and value. -->
    <xsl:output indent="yes"/>
    <xsl:variable name="institution">
        <xsl:call-template name="clean-up-text">
            <xsl:with-param name="some-text"
                select="//marc:record/marc:datafield[@tag='852']/marc:subfield[@code='a']"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="repository">
        <xsl:call-template name="clean-up-text">
            <xsl:with-param name="some-text"
                select="//marc:record/marc:datafield[@tag='852']/marc:subfield[@code='b']"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="call_number">
        <xsl:call-template name="clean-up-text">
            <xsl:with-param name="some-text"
                select="//marc:holding/marc:call_number"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="ms_title">
        <xsl:call-template name="clean-up-text">
            <xsl:with-param name="some-text"
                select="//marc:datafield[@tag='245']/marc:subfield[@code='a']"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="bibid">
      <xsl:call-template name="clean-up-text">
        <xsl:with-param name="some-text"
          select="//marc:records/marc:record/marc:controlfield[@tag='001']"/>
      </xsl:call-template>
    </xsl:variable>
    <xsl:template match="/">
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <xsl:for-each select="//marc:datafield[@tag=245]">
                            <xsl:for-each select="marc:subfield">
                                <xsl:if test="@code='a'">
                                    <title>
                                        <xsl:attribute name="level">m</xsl:attribute>
                                        <xsl:attribute name="type">marc245a</xsl:attribute>
                                        <xsl:call-template name="chopPunctuation">
                                            <xsl:with-param name="chopString">
                                                <xsl:value-of select="."/>
                                            </xsl:with-param>
                                        </xsl:call-template>
                                    </title>
                                </xsl:if>
                                <xsl:if test="@code='b'">
                                    <title>
                                        <xsl:attribute name="level">m</xsl:attribute>
                                        <xsl:attribute name="type">marc245b</xsl:attribute>
                                        <xsl:call-template name="chopPunctuation">
                                            <xsl:with-param name="chopString">
                                                <xsl:value-of select="."/>
                                            </xsl:with-param>
                                        </xsl:call-template>
                                    </title>
                                </xsl:if>
                            </xsl:for-each>
                        </xsl:for-each>
                      <xsl:for-each select="//marc:datafield[@tag=100]|//marc:datafield[@tag=110]|//marc:datafield[@tag=111]">
                        <author>
                          <xsl:call-template name="subfieldSelect">
                            <xsl:with-param name="codes">abcdgu</xsl:with-param>
                          </xsl:call-template>
                        </author>
                      </xsl:for-each>
                      <xsl:for-each select="//marc:datafield[@tag=700]|//marc:datafield[@tag=710]|//marc:datafield[@tag=500]">
                        <respStmt>
                          <resp>Contributor</resp>
                          <name>
                            <xsl:call-template name="subfieldSelect">
                              <xsl:with-param name="codes">abcdgu</xsl:with-param>
                            </xsl:call-template>
                          </name>
                        </respStmt>
                      </xsl:for-each>
                    </titleStmt>
                    <publicationStmt>
                      <publisher>The University of Pennsylvania Libraries</publisher>
                      <availability>
                          <licence target="http://creativecommons.org/licenses/by/4.0/legalcode">
                              This description is ©<xsl:value-of select="year-from-date(current-date())"/> University of
                              Pennsylvania Libraries. It is licensed under a Creative Commons
                              Attribution License version 4.0 (CC-BY-4.0
                              https://creativecommons.org/licenses/by/4.0/legalcode. For a
                              description of the terms of use see the Creative Commons Deed
                              https://creativecommons.org/licenses/by/4.0/. </licence>
                          <licence target="http://creativecommons.org/publicdomain/mark/1.0/"> All
                              referenced images and their content are free of known copyright
                              restrictions and in the public domain. See the Creative Commons
                              Public Domain Mark page for usage details,
                              http://creativecommons.org/publicdomain/mark/1.0/. </licence>
                      </availability>
                      <!-- DE: We haven't had an ID for our TEI. Should we? If so, what? -->
                      <!--<idno>SOME VALUE</idno>-->
                      <!-- DE: We also haven't had a publicatoin date. We should. Date the TEI is generated? -->
                      <date>
                        <xsl:attribute name="when">
                          <xsl:value-of select="format-date(current-date(), '[Y0001]-[M01]-[D01]')"/>
                        </xsl:attribute>
                      </date>
                    </publicationStmt>
                    <sourceDesc>
                      <biblStruct>
                        <monogr>
                          <xsl:for-each select="//marc:datafield[@tag=100]|//marc:datafield[@tag=110]|//marc:datafield[@tag=700]|//marc:datafield[@tag=710]">
                            <author>
                              <xsl:call-template name="subfieldSelect">
                                <xsl:with-param name="codes">abcdgu</xsl:with-param>
                              </xsl:call-template>
                            </author>
                          </xsl:for-each>
                          <xsl:for-each select="//marc:datafield[@tag=245]">
                            <xsl:for-each select="marc:subfield">
                              <xsl:if test="@code='a'">
                                <title>
                                  <xsl:attribute name="level">m</xsl:attribute>
                                  <xsl:attribute name="type">marc245a</xsl:attribute>
                                  <xsl:call-template name="chopPunctuation">
                                    <xsl:with-param name="chopString">
                                      <xsl:value-of select="."/>
                                    </xsl:with-param>
                                  </xsl:call-template>
                                </title>
                              </xsl:if>
                              <xsl:if test="@code='b'">
                                <title>
                                  <xsl:attribute name="level">m</xsl:attribute>
                                  <xsl:attribute name="type">marc245b</xsl:attribute>
                                  <xsl:call-template name="chopPunctuation">
                                    <xsl:with-param name="chopString">
                                      <xsl:value-of select="."/>
                                    </xsl:with-param>
                                  </xsl:call-template>
                                </title>
                              </xsl:if>
                            </xsl:for-each>
                          </xsl:for-each>
                          <xsl:for-each select="//marc:datafield[@tag=130]|//marc:datafield[@tag=240]|//marc:datafield[@tag=246]">
                            <title>
                            <xsl:call-template name="subfieldSelect">
                              <xsl:with-param name="codes">abcdgu</xsl:with-param>
                            </xsl:call-template>
                            </title>
                          </xsl:for-each>
                          <xsl:for-each select="//marc:datafield[@tag=250]">
                            <edition>
                              <xsl:call-template name="subfieldSelect">
                                <xsl:with-param name="codes">abcdgu</xsl:with-param>
                              </xsl:call-template>
                            </edition>
                          </xsl:for-each>
                          <imprint>
                            <xsl:for-each select="//marc:datafield[@tag=260]/marc:subfield[@code='a']">
                              <pubPlace>
                                <xsl:call-template name="chopPunctuation">
                                  <xsl:with-param name="chopString">
                                    <xsl:value-of select="."/>
                                  </xsl:with-param>
                                </xsl:call-template>
                              </pubPlace>
                            </xsl:for-each>
                            <xsl:for-each select="//marc:datafield[@tag=260]/marc:subfield[@code='b']">
                              <publisher>
                                <xsl:call-template name="chopPunctuation">
                                  <xsl:with-param name="chopString">
                                    <xsl:value-of select="."/>
                                  </xsl:with-param>
                                </xsl:call-template>
                              </publisher>
                            </xsl:for-each>
                            <xsl:for-each select="//marc:datafield[@tag=260]/marc:subfield[@code='c']">
                              <xsl:variable name="pubDate">
                                <xsl:call-template name="chopPunctuation">
                                  <xsl:with-param name="chopString">
                                    <xsl:value-of select="."/>
                                  </xsl:with-param>
                                </xsl:call-template>
                              </xsl:variable>
                              <!--
                                DE: Is this dangerous? Can it be a range? An LC partial date? Circa date?
                                    They won't validate as date attributes.
                              -->
                              <date>
                                <xsl:attribute name="when" select="$pubDate"/>
                                <xsl:value-of select="$pubDate"/>
                              </date>
                            </xsl:for-each>
                          </imprint>
                            <xsl:for-each select="//marc:datafield[@tag=300]/marc:subfield">
                              <!--  DE: I'm skipping subfield 'b' here. It should be combined with 'a' if it
                                    exists. -->
                              <xsl:if test="@code='a'">
                                <extent>
                                  <xsl:call-template name="chopPunctuation">
                                    <xsl:with-param name="chopString">
                                      <xsl:value-of select="."/>
                                    </xsl:with-param>
                                  </xsl:call-template>
                                </extent>
                              </xsl:if>
                              <xsl:if test="@code='c'">
                                <extent>
                                  <xsl:call-template name="chopPunctuation">
                                    <xsl:with-param name="chopString">
                                      <xsl:value-of select="."/>
                                    </xsl:with-param>
                                  </xsl:call-template>
                                </extent>
                              </xsl:if>
                            </xsl:for-each>
                        </monogr>
                        <series>
                          <title level="s">Need to examine our marc and figure out which to use.
                            TEI recommends 4xx and 8xx be used here, without providing much detail.
                            Need to investigate subfield.
                            In sample marc, we use 440, 490, 810, 830, 856; the last being the facsimile.
                          </title>
                        </series>
                        <xsl:if test="//marc:datafield[@tag='500']">
                          <xsl:for-each select="//marc:datafield[@tag='500']">
                            <note>
                              <xsl:value-of
                                select="normalize-space(marc:subfield[@code='a'])"/>
                            </note>
                          </xsl:for-each>
                        </xsl:if>
                        <!-- DE: Add idno -->
                      </biblStruct>
                        <msDesc>
                            <msIdentifier>
                                <settlement>Philadelphia</settlement>
                                <institution>
                                    <xsl:value-of select="$institution"/>
                                </institution>
                                <repository>
                                    <xsl:value-of select="$repository"/>
                                </repository>
                                <idno type="call-number">
                                    <xsl:value-of select="$call_number"/>
                                </idno>
                                <xsl:if
                                    test="//marc:datafield[@tag='856']/marc:subfield[@code='z' and matches(text(), 'facsimile', 'i')]">
                                    <altIdentifier type="resource">
                                        <idno>
                                            <xsl:value-of select="//marc:datafield[@tag='856']/marc:subfield[@code='z' and matches(text(), 'facsimile', 'i')]/parent::marc:datafield/marc:subfield[@code='u']"/>
                                        </idno>
                                    </altIdentifier>
                                </xsl:if>
                            </msIdentifier>
                            <msContents>
                                <summary>
                                    <xsl:value-of select="normalize-space((//marc:datafield[@tag='520']/marc:subfield[@code='a'])[last()])"/>
                                </summary>
                                <xsl:if test="//marc:datafield[@tag='546']/marc:subfield[@code='a']">
                                    <textLang>
                                        <xsl:if test="//marc:datafield[@tag='041']/marc:subfield[@code='a']">
                                            <xsl:attribute name="mainLang" select="//marc:datafield[@tag='041']/marc:subfield[@code='a'][1]"/>
                                            <xsl:if test="count(//marc:datafield[@tag='041']/marc:subfield[@code='a']) &gt; 1">
                                                <xsl:attribute name="otherLangs">
                                                    <xsl:call-template name="other-langs">
                                                        <xsl:with-param name="tags" select="//marc:datafield[@tag='041']/marc:subfield[@code='a']" />
                                                    </xsl:call-template>
                                                </xsl:attribute>
                                            </xsl:if>
                                        </xsl:if>
                                        <xsl:call-template name="chomp-period">
                                            <xsl:with-param name="string" select="normalize-space(//marc:datafield[@tag='546']/marc:subfield[@code='a'])" />
                                        </xsl:call-template>
                                    </textLang>
                                </xsl:if>
                                <msItem>
                                    <title>
                                        <xsl:call-template name="clean-up-text">
                                            <xsl:with-param name="some-text" select="//marc:datafield[@tag='245']/marc:subfield[@code='a']" />
                                        </xsl:call-template>
                                    </title>
                                    <!-- DE: Grab authors from marc 110, 100 and 700 -->
                                    <!-- DE: marc 110 is a corporate author -->
                                    <xsl:for-each select="//marc:datafield[@tag='110']/marc:subfield[@code='a']">
                                        <author>
                                            <xsl:call-template name="chomp-period">
                                                <xsl:with-param name="string" select="." />
                                            </xsl:call-template>
                                        </author>
                                    </xsl:for-each>
                                    <!-- marc 100: primary author, person -->
                                    <xsl:for-each select="//marc:datafield[@tag='100']">
                                        <author>
                                            <xsl:call-template name="extract-pn">
                                                <xsl:with-param name="datafield" select="."/>
                                            </xsl:call-template>
                                        </author>
                                    </xsl:for-each>
                                    <!-- DE: marc 700's w/o a relator (code='e') are secondary authors -->
                                    <xsl:for-each select="//marc:datafield[@tag='700' and not(child::marc:subfield[@code='e'])]">
                                        <author>
                                            <xsl:call-template name="extract-pn">
                                                <xsl:with-param name="datafield" select="."/>
                                            </xsl:call-template>
                                        </author>
                                    </xsl:for-each>
                                    <xsl:for-each select="//marc:datafield[@tag='700']/marc:subfield[@code='e']">
                                        <respStmt>
                                            <resp>
                                                <xsl:call-template name="chomp-period">
                                                    <xsl:with-param name="string">
                                                        <xsl:call-template name="clean-up-text">
                                                            <xsl:with-param name="some-text" select="."/>
                                                        </xsl:call-template>
                                                    </xsl:with-param>
                                                </xsl:call-template>
                                            </resp>
                                            <persName>
                                                <xsl:call-template name="chomp-period">
                                                    <xsl:with-param name="string">
                                                        <xsl:call-template name="clean-up-text">
                                                            <xsl:with-param name="some-text">
                                                                <xsl:call-template name="extract-pn">
                                                                    <xsl:with-param name="datafield" select="./parent::marc:datafield"/>
                                                                </xsl:call-template>
                                                            </xsl:with-param>
                                                        </xsl:call-template>
                                                    </xsl:with-param>
                                                </xsl:call-template>
                                            </persName>
                                        </respStmt>
                                    </xsl:for-each>
                                    <xsl:for-each select="//marc:datafield[@tag='500']/marc:subfield[@code='a']">
                                        <xsl:choose>
                                            <xsl:when test="starts-with(.,'Colophon')">
                                                <colophon>
                                                    <xsl:value-of select="normalize-space(.)"/>
                                                </colophon>
                                            </xsl:when>
                                        </xsl:choose>
                                    </xsl:for-each>
                                </msItem>
                                <xsl:for-each select="//page/tocentry[@name='toc']">
                                    <xsl:variable name="locus" select="./parent::page/@visiblepage"/>
                                    <msItem>
                                        <xsl:attribute name="n">
                                            <xsl:call-template name="clean-up-text">
                                                <xsl:with-param name="some-text" select="$locus"/>
                                            </xsl:call-template>
                                        </xsl:attribute>
                                        <locus>
                                            <xsl:value-of select="$locus"/>
                                        </locus>
                                        <title>
                                            <xsl:value-of select="normalize-space(.)"/>
                                        </title>
                                    </msItem>
                                </xsl:for-each>
                            </msContents>
                            <physDesc>
                                <xsl:if test="//marc:datafield[@tag='300']">
                                    <xsl:variable name="datafield" select="//marc:datafield[@tag='300']"/>
                                    <xsl:variable name="support" select="normalize-space(tokenize($datafield/marc:subfield[@code='b'], '[,;]')[1])"/>
                                    <xsl:variable name="mixed">
                                      <xsl:call-template name="matches-two">
                                        <xsl:with-param name="source" select="$support"/>
                                        <xsl:with-param name="strings" select="'parch paper papyrus palm'"/>
                                      </xsl:call-template>
                                    </xsl:variable>
                                    <objectDesc>
                                        <supportDesc>
                                            <xsl:if test="$support">
                                                <xsl:attribute name="material">
                                                    <xsl:choose>
                                                        <xsl:when test="$mixed">
                                                            <xsl:text>mixed</xsl:text>
                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                            <xsl:value-of select="string-join(tokenize(normalize-space($support), '\s+'), '-')"/>
                                                        </xsl:otherwise>
                                                    </xsl:choose>
                                                </xsl:attribute>
                                            </xsl:if>
                                            <xsl:if test="$support">
                                                <support>
                                                    <p>
                                                        <xsl:value-of select="$support"/>
                                                    </p>
                                                    <xsl:for-each select="//marc:datafield[@tag='500']/marc:subfield[@code='a' and (starts-with(., 'Watermark:') or starts-with(., 'Watermarks:'))]">
                                                        <watermark>
                                                            <xsl:value-of select="normalize-space(substring(.,12))"/>
                                                        </watermark>
                                                    </xsl:for-each>
                                                </support>
                                            </xsl:if>
                                            <xsl:if test="$datafield/marc:subfield[@code='a'] or $datafield/marc:subfield[@code='c']">
                                                <extent>
                                                    <xsl:call-template name="chomp-period">
                                                        <xsl:with-param name="string">
                                                            <xsl:value-of select="normalize-space(concat($datafield/marc:subfield[@code='a'], ' ', $datafield/marc:subfield[@code='c']))"/>
                                                        </xsl:with-param>
                                                    </xsl:call-template>
                                                </extent>
                                            </xsl:if>
                                            <xsl:for-each select="//marc:datafield[@tag='500']/marc:subfield[@code='a' and (starts-with(., 'Foliation:') or starts-with(., 'Pagination:'))]">
                                                <foliation>
                                                    <xsl:choose>
                                                        <xsl:when test="starts-with(., 'Foliation:')">
                                                            <xsl:value-of select="normalize-space(substring(.,11))"/>
                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                            <xsl:value-of select="normalize-space(substring(.,12))"/>
                                                        </xsl:otherwise>
                                                    </xsl:choose>
                                                </foliation>
                                            </xsl:for-each>
                                            <xsl:if test="contains(.,'Collation:') or contains(.,'Signatures')">
                                                <collation>
                                                    <xsl:for-each select="//marc:datafield[@tag='500']/marc:subfield[@code='a' and starts-with(., 'Collation:')]">
                                                        <p>
                                                            <xsl:value-of select="normalize-space(substring(.,12))"/>
                                                        </p>
                                                    </xsl:for-each>
                                                    <xsl:for-each select="//marc:datafield[@tag='500']/marc:subfield[@code='a' and starts-with(., 'Signatures:')]">
                                                        <p>
                                                            <signatures>
                                                                <xsl:value-of select="normalize-space(substring(.,12))"/>
                                                            </signatures>
                                                        </p>
                                                    </xsl:for-each>
                                                </collation>
                                            </xsl:if>
                                        </supportDesc>
                                        <xsl:for-each select="//marc:datafield[@tag='500']/marc:subfield[@code='a' and starts-with(.,'Layout:')]">
                                            <layoutDesc>
                                                <layout>
                                                    <xsl:value-of select="normalize-space(substring(.,8))"/>
                                                </layout>
                                            </layoutDesc>
                                        </xsl:for-each>
                                    </objectDesc>
                                </xsl:if>
                                <xsl:for-each select="//marc:datafield[@tag='500']/marc:subfield[@code='a' and starts-with(., 'Script:')]">
                                    <scriptDesc>
                                        <scriptNote>
                                            <xsl:value-of select="normalize-space(substring(.,8))"/>
                                        </scriptNote>
                                    </scriptDesc>
                                </xsl:for-each>
                                <xsl:if test="starts-with(.,'Decoration:') or count(//page/tocentry[@name='ill']) > 0">
                                    <decoDesc>
                                        <xsl:for-each select="//marc:datafield[@tag='500']/marc:subfield[@code='a'and starts-with(., 'Decoration:')]">
                                            <decoNote>
                                                <xsl:value-of select="normalize-space(substring(.,12))"/>
                                            </decoNote>
                                        </xsl:for-each>
                                        <xsl:for-each select="//page/tocentry[@name='ill']">
                                            <decoNote>
                                                <xsl:attribute name="n">
                                                    <xsl:call-template name="clean-up-text">
                                                        <xsl:with-param name="some-text" select="./parent::page/@visiblepage"/>
                                                    </xsl:call-template>
                                                </xsl:attribute>
                                                <xsl:value-of select="normalize-space(.)"/>
                                            </decoNote>
                                        </xsl:for-each>
                                    </decoDesc>
                                </xsl:if>
                                <xsl:for-each select="//marc:datafield[@tag='500']/marc:subfield[@code='a' and starts-with(., 'Binding:')]">
                                    <bindingDesc>
                                        <binding>
                                            <p>
                                                <xsl:value-of select="normalize-space(substring(.,9))"/>
                                            </p>
                                        </binding>
                                    </bindingDesc>
                                </xsl:for-each>
                            </physDesc>
                            <history>
                                <origin>
                                    <xsl:for-each select="//marc:datafield[@tag='500']/marc:subfield[@code='a' and starts-with(., 'Origin:')]">
                                        <p>
                                            <xsl:value-of select="normalize-space(substring(.,8))"/>
                                        </p>
                                    </xsl:for-each>
                                    <!-- DOT ADDED AN IF STATEMENT AROUND ORIGDATE, SO IF THERE IS NO ORIGDATE IN THE MARC RECORD ORIGDATE WILL NOT BE CREATED -->
                                    <!-- DE: just use the marc field -->
                                    <xsl:for-each select="//marc:datafield[@tag='260']/marc:subfield[@code='c']">
                                        <origDate>
                                            <xsl:call-template name="chomp-period">
                                                <xsl:with-param name="string">
                                                    <xsl:call-template name="clean-up-text">
                                                        <xsl:with-param name="some-text" select="." />
                                                    </xsl:call-template>
                                                </xsl:with-param>
                                            </xsl:call-template>
                                        </origDate>
                                    </xsl:for-each>
                                    <!-- END DOT MOD -->
                                    <!-- DE: Cleaner code for origPlace; add only if present -->
                                    <xsl:for-each select="//marc:datafield[@tag='260']/marc:subfield[@code='a']">
                                        <origPlace>
                                            <xsl:call-template name="clean-up-text">
                                                <xsl:with-param name="some-text" select="."/>                                            </xsl:call-template>
                                        </origPlace>
                                    </xsl:for-each>
                                </origin>
                                <!-- DOT ADDED PROVENANCE -->
                                <xsl:for-each select="//marc:datafield[@tag='561']">
                                    <provenance>
                                        <xsl:value-of select="marc:subfield[@code='a']"/>
                                    </provenance>
                                </xsl:for-each>
                                <!-- END DOT MOD -->
                            </history>
                        </msDesc>
                    </sourceDesc>
                </fileDesc>
                <!-- DOT ADDED KEYWORDS FOR SUBJECTS AND GENRE/FORM -->
                <profileDesc>
                    <textClass>
                        <!-- DE: Switching to marc 610 and joining subfields -->
                        <xsl:if test="//marc:datafield[@tag='610' or @tag='650']">
                            <keywords xmlns="http://www.tei-c.org/ns/1.0" n="subjects">
                                <xsl:for-each select="//marc:datafield[@tag='610' or @tag='650']">
                                    <term>
                                        <xsl:call-template name="join-keywords">
                                            <xsl:with-param name="datafield" select="."/>
                                        </xsl:call-template>
                                    </term>
                                </xsl:for-each>
                            </keywords>
                        </xsl:if>
                        <xsl:if test="//marc:datafield[@tag='655']/marc:subfield[@code='a']">
                            <keywords n="form/genre">
                                <xsl:for-each select="//marc:datafield[@tag='655' and child::marc:subfield[@code='a']]">
                                    <term>
                                        <xsl:call-template name="join-genre">
                                            <xsl:with-param name="datafield" select="."/>
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
    <!--  Return true if two or more of the items in $strings match the source. -->
    <xsl:template name="matches-two">
      <xsl:param name="source"/> <!-- 'paper with parchment tags' -->
      <xsl:param name="strings"/> <!-- 'paper parch papyrus palm'  -->
      <xsl:variable name="matches" as="xs:string*">
        <xsl:for-each select="tokenize($strings, '\s+')">
          <xsl:if test="matches($source, ., 'i')">
            <xsl:value-of select="."/>
          </xsl:if>
        </xsl:for-each>
      </xsl:variable>
      <xsl:value-of select="count($matches) &gt; 1"/>
    </xsl:template>
    <xsl:template name="datafield">
        <xsl:param name="tag"/>
        <xsl:param name="ind1"><xsl:text> </xsl:text></xsl:param>
        <xsl:param name="ind2"><xsl:text> </xsl:text></xsl:param>
        <xsl:param name="subfields"/>
        <xsl:element name="datafield">
            <xsl:attribute name="tag">
                <xsl:value-of select="$tag"/>
            </xsl:attribute>
            <xsl:attribute name="ind1">
                <xsl:value-of select="$ind1"/>
            </xsl:attribute>
            <xsl:attribute name="ind2">
                <xsl:value-of select="$ind2"/>
            </xsl:attribute>
            <xsl:copy-of select="$subfields"/>
        </xsl:element>
    </xsl:template>
    <xsl:template name="subfieldSelect">
        <xsl:param name="codes"/>
        <xsl:param name="delimeter"><xsl:text> </xsl:text></xsl:param>
        <xsl:variable name="str">
            <xsl:for-each select="marc:subfield">
                <xsl:if test="contains($codes, @code)">
                    <xsl:value-of select="text()"/><xsl:value-of select="$delimeter"/>
                </xsl:if>
            </xsl:for-each>
        </xsl:variable>
        <xsl:value-of select="substring($str,1,string-length($str)-string-length($delimeter))"/>
    </xsl:template>
    <xsl:template name="buildSpaces">
        <xsl:param name="spaces"/>
        <xsl:param name="char"><xsl:text> </xsl:text></xsl:param>
        <xsl:if test="$spaces>0">
            <xsl:value-of select="$char"/>
            <xsl:call-template name="buildSpaces">
                <xsl:with-param name="spaces" select="$spaces - 1"/>
                <xsl:with-param name="char" select="$char"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>
    <xsl:template name="chopPunctuationFront">
        <xsl:param name="chopString"/>
        <xsl:variable name="length" select="string-length($chopString)"/>
        <xsl:choose>
            <xsl:when test="$length=0"/>
            <xsl:when test="contains('.:,;/[ ', substring($chopString,1,1))">
                <xsl:call-template name="chopPunctuationFront">
                    <xsl:with-param name="chopString" select="substring($chopString,2,$length - 1)"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="not($chopString)"/>
            <xsl:otherwise><xsl:value-of select="$chopString"/></xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="chopPunctuation">
        <xsl:param name="chopString"/>
        <xsl:variable name="length" select="string-length($chopString)"/>
        <xsl:choose>
            <xsl:when test="$length=0"/>
            <xsl:when test="contains('.:,;/ ', substring($chopString,$length,1))">
                <xsl:call-template name="chopPunctuation">
                    <xsl:with-param name="chopString" select="substring($chopString,1,$length - 1)"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="not($chopString)"/>
            <xsl:otherwise><xsl:value-of select="$chopString"/></xsl:otherwise>
        </xsl:choose>
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
</xsl:stylesheet>