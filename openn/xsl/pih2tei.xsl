<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns="http://www.tei-c.org/ns/1.0"
    xmlns:marc="http://www.loc.gov/MARC21/slim" exclude-result-prefixes="xs xd marc tei"
    version="2.0">
  <xsl:import href="openn_templates.xsl"/>
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

    <xsl:output indent="yes"/>

  <xsl:param name="HOLDING_ID"/>

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
        <xsl:choose>
            <xsl:when test="//marc:holdings/marc:holding">

                <xsl:choose>
                    <xsl:when test="$HOLDING_ID">
                        <xsl:if test="not(//marc:holding_id/text() = $HOLDING_ID)">
                            <xsl:message terminate="yes">
                                ERROR: No entry found for holding ID: '<xsl:value-of select="$HOLDING_ID"/>'.
                            </xsl:message>
                        </xsl:if>
                        <xsl:value-of select="//marc:holding_id[text() = $HOLDING_ID]/parent::marc:holding/marc:call_number"/>
                    </xsl:when>
                    <xsl:when test="count(//marc:holding) &gt; 1">
                        <xsl:message terminate="yes">
                            ERROR: Record has more than one holding; please provide HOLDING_ID:
                            <xsl:copy-of select="//marc:holdings"/>
                        </xsl:message>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="//marc:holding[1]/marc:call_number/text()"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="//marc:record/marc:datafield[@tag='099']/marc:subfield[@code='a']"/>
            </xsl:otherwise>
        </xsl:choose>
        <!--
            Datafield 773 is used to indicate a constituent unit within an item.

            Penn uses 773$g to indicate the item number for objects in a collection.
            From the specification:

                $g - Related parts (R)

        -->
        <xsl:if test="//marc:record/marc:datafield[@tag='773']/marc:subfield[@code='g']">
            <xsl:text> </xsl:text>
            <xsl:value-of select="//marc:record/marc:datafield[@tag='773']/marc:subfield[@code='g']"/>
        </xsl:if>
    </xsl:variable>

    <xsl:variable name="ms_title">
        <xsl:call-template name="clean-up-text">
            <xsl:with-param name="some-text"
                select="//marc:datafield[@tag='245']/marc:subfield[@code='a']"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:template match="/">

        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title>
                            <xsl:value-of
                                select="normalize-space(concat('Description of ', $institution, ' ', $call_number, ': ', $ms_title))"
                            />
                        </title>
                    </titleStmt>
                    <xsl:comment>
                        TODO: Change publisher, licence information for MMW Columnbia, FLP, etc.
                    </xsl:comment>
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
                    </publicationStmt>

                    <!-- DOT ADDED NOTESSTMT TO HOLD ALL THE RANDOM NOTES FROM THE MARC RECORD -->
                    <xsl:if test="//marc:datafield[@tag='500']">
                        <notesStmt>
                            <xsl:for-each select="//marc:datafield[@tag='500']">
                                <xsl:variable name="test" select="marc:subfield[@code='a']"/>
                                <xsl:choose>
                                    <xsl:when
                                        test="not(starts-with($test,'Pagination:')) and not(starts-with($test,'Foliation:')) and not(starts-with($test,'Layout:')) and not(starts-with($test,'Colophon:')) and not(starts-with($test,'Collation:')) and not(starts-with($test,'Script:')) and not(starts-with($test,'Decoration:')) and not(starts-with($test,'Binding:')) and not(starts-with($test,'Origin:')) and not(starts-with($test,'Watermarks:')) and not(starts-with($test,'Watermark:')) and not(starts-with($test,'Signatures:'))">
                                        <note>
                                            <xsl:value-of
                                                select="normalize-space(marc:subfield[@code='a'])"/>
                                        </note>
                                    </xsl:when>
                                </xsl:choose>
                            </xsl:for-each>
                        </notesStmt>
                    </xsl:if>
                    <!-- END DOT MOD -->

                    <sourceDesc>
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
                                <altIdentifier type="bibid">
                                    <idno>
                                        <xsl:value-of select="//marc:controlfield[@tag='001']"/>
                                    </idno>
                                </altIdentifier>
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
                                <!--
                                    For now for vernacular scripts, extracting just the text of the name, subfield $a

                                    TODO: Looking into concatenating bidirectional strings; i.e., adding vernacular arabic script with latin character dates

                                    Experiments using the recommendations here have not worked:

                                        https://www.w3.org/International/questions/qa-bidi-unicode-controls

                                    At least in Oxygen, the bidi codes I used show up as little boxes rather than afffect character orientation

                                    Would need to check the orientation code in the linkage; e.g. the '/r' in '100-01/r'* ,

                                        <marc:datafield tag="880" ind1="1" ind2=" ">
                                          <marc:subfield code="6">100-01/r</marc:subfield>
                                          <marc:subfield code="a">جزولي، محمد بن سليمان،</marc:subfield>
                                          <marc:subfield code="d">-1465</marc:subfield>
                                        </marc:datafield>

                                    MARC page with details on orientatiion codes for lingage control subfield, '$6':

                                        https://www.loc.gov/marc/bibliographic/ecbdcntf.html

                                    *Note that '/r' is not defined in the MARC spec for linkage '$6'.

                                -->
                                <msItem>
                                    <title>
                                        <xsl:call-template name="clean-up-text">
                                            <xsl:with-param name="some-text" select="//marc:datafield[@tag='245']/marc:subfield[@code='a']" />
                                        </xsl:call-template>
                                    </title>
                                    <xsl:if test="starts-with(//marc:datafield[@tag='245']/marc:subfield[@code='6']/text(), '880')">
                                        <title type="vernacular">
                                            <xsl:variable name="datafield880" as="node()">
                                                <xsl:call-template name="locate880">
                                                    <xsl:with-param name="datafield" select="//marc:datafield[@tag='245']"/>
                                                </xsl:call-template>
                                            </xsl:variable>
                                            <xsl:call-template name="chopPunctuation">
                                                <xsl:with-param name="chopString" select="$datafield880/marc:subfield[@code='a']"/>
                                            </xsl:call-template>
                                        </title>
                                    </xsl:if>

                                    <!-- DE: Grab authors from marc 110, 100 and 700 -->
                                    <!-- DE: marc 110 is a corporate author -->
                                    <xsl:for-each select="//marc:datafield[@tag='110' and ./marc:subfield[@code='a']]">
                                        <author>
                                          <name type="authority">
                                            <xsl:call-template name="chopPunctuation">
                                                <xsl:with-param name="chopString" select="./marc:subfield[@code='a']" />
                                            </xsl:call-template>
                                          </name>
                                            <!-- Look for an associaed graphical representation of the name -->
                                            <xsl:if test="starts-with(./marc:subfield[@code='6']/text(), '880')">
                                                <name type="vernacular">
                                                    <xsl:variable name="datafield880" as="node()">
                                                        <xsl:call-template name="locate880">
                                                            <xsl:with-param name="datafield" select="."/>
                                                        </xsl:call-template>
                                                    </xsl:variable>
                                                    <xsl:call-template name="chopPunctuation">
                                                        <xsl:with-param name="chopString" select="$datafield880/marc:subfield[@code='a']"/>
                                                    </xsl:call-template>
                                                </name>
                                            </xsl:if>
                                        </author>
                                    </xsl:for-each>
                                    <!-- marc 100: primary author, person -->
                                    <xsl:for-each select="//marc:datafield[@tag='100']">
                                        <author>
                                          <persName type="authority">
                                            <xsl:call-template name="extract-pn">
                                                <xsl:with-param name="datafield" select="."/>
                                            </xsl:call-template>
                                          </persName>
                                            <!-- Look for an associaed graphical representation of the name -->
                                            <xsl:if test="starts-with(./marc:subfield[@code='6']/text(), '880')">
                                                <persName type="vernacular">
                                                    <xsl:variable name="datafield880" as="node()">
                                                        <xsl:call-template name="locate880">
                                                            <xsl:with-param name="datafield" select="."/>
                                                        </xsl:call-template>
                                                    </xsl:variable>
                                                    <xsl:call-template name="chopPunctuation">
                                                        <xsl:with-param name="chopString" select="$datafield880/marc:subfield[@code='a']"/>
                                                    </xsl:call-template>
                                                </persName>
                                            </xsl:if>
                                        </author>
                                    </xsl:for-each>
                                    <!-- DE: marc 700's w/o a relator (code='e') are secondary authors -->
                                    <xsl:for-each select="//marc:datafield[@tag='700' and not(child::marc:subfield[@code='e'])]">
                                        <author>
                                          <persName type="authority">
                                            <xsl:call-template name="extract-pn">
                                                <xsl:with-param name="datafield" select="."/>
                                            </xsl:call-template>
                                          </persName>
                                            <!-- Look for an associaed graphical representation of the name -->
                                            <xsl:if test="starts-with(./marc:subfield[@code='6']/text(), '880')">
                                                <persName type="vernacular">
                                                  <xsl:variable name="datafield880" as="node()">
                                                      <xsl:call-template name="locate880">
                                                          <xsl:with-param name="datafield" select="."/>
                                                      </xsl:call-template>
                                                  </xsl:variable>
                                                  <xsl:call-template name="chopPunctuation">
                                                      <xsl:with-param name="chopString" select="$datafield880/marc:subfield[@code='a']"/>
                                                  </xsl:call-template>
                                              </persName>
                                          </xsl:if>
                                        </author>
                                    </xsl:for-each>
                                    <xsl:for-each select="//marc:datafield[@tag='700' and ./marc:subfield[@code='e']]">
                                        <respStmt>
                                            <resp>
                                                <xsl:call-template name="chopPunctuation">
                                                    <xsl:with-param name="chopString">
                                                        <xsl:call-template name="clean-up-text">
                                                            <xsl:with-param name="some-text" select="./marc:subfield[@code='e']"/>
                                                        </xsl:call-template>
                                                    </xsl:with-param>
                                                </xsl:call-template>
                                            </resp>
                                            <persName type="authority">
                                                <xsl:call-template name="clean-up-text">
                                                    <xsl:with-param name="some-text">
                                                        <xsl:call-template name="extract-pn">
                                                            <xsl:with-param name="datafield" select="."/>
                                                        </xsl:call-template>
                                                    </xsl:with-param>
                                                </xsl:call-template>
                                            </persName>

                                            <!-- Look for an associaed graphical representation of the name -->
                                            <xsl:if test="starts-with(./marc:subfield[@code='6']/text(), '880')">
                                                <persName type="vernacular">
                                                    <xsl:variable name="datafield880" as="node()">
                                                        <xsl:call-template name="locate880">
                                                            <xsl:with-param name="datafield" select="."/>
                                                        </xsl:call-template>
                                                    </xsl:variable>
                                                    <xsl:value-of select="$datafield880/marc:subfield[@code='a']"/>
                                                </persName>
                                            </xsl:if>
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
                                                          <xsl:value-of select="normalize-space(concat($datafield/marc:subfield[@code='a'], ' ', $datafield/marc:subfield[@code='f'], ' ', $datafield/marc:subfield[@code='c']))"/>
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
                <graphic url=""/>
            </facsimile>
        </TEI>
    </xsl:template>

</xsl:stylesheet>
