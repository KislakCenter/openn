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
                select="//marc:datafield[@tag='099']/marc:subfield[@code='a']"/>
        </xsl:call-template>
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
                  <xsl:comment>
                    TODO: ? for Mitch/Dot/Will: CU MARC uses 588$a to give description provenance ('Item cataloged from digital facsimile and existing description.'). Should we include that?
                    ANSWER: NO
                  </xsl:comment>
                  <xsl:comment>
                    TODO: ? for Mitch/Dot: Do we include CU MARC 710$a for "name of agency of production" (AMREMM): "Muslim World Manuscripts (Columbia University. Rare Book and Manuscript Library)". Is so, where?
                    ANSWER: NO
                  </xsl:comment>
                    <titleStmt>
                        <title>
                            <xsl:value-of
                                select="normalize-space(concat('Description of ', $institution, ' ', $call_number, ': ', $ms_title))"
                            />
                        </title>
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
                    </publicationStmt>

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
                              <xsl:comment>
                                TODO: Shelfmark pulled from 099$a. CU MARC has 500$a => "Shelfmark: MS Or 355". Is this alw the same value as 099$a?
                                ANSWER: Value in  099$a and 500$a Shelfmark: will always be the same.
                              </xsl:comment>
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
                                <msItem>
                                    <title>
                                        <xsl:call-template name="clean-up-text">
                                            <xsl:with-param name="some-text" select="//marc:datafield[@tag='245']/marc:subfield[@code='a']" />
                                        </xsl:call-template>
                                    </title>
                                    <xsl:for-each select="//marc:datafield[@tag='110']/marc:subfield[@code='a']">
                                        <author>
                                            <xsl:call-template name="chomp-period">
                                                <xsl:with-param name="string" select="." />
                                            </xsl:call-template>
                                        </author>
                                    </xsl:for-each>
                                    <xsl:for-each select="//marc:datafield[@tag='100']">
                                        <author>
                                            <xsl:call-template name="extract-pn">
                                                <xsl:with-param name="datafield" select="."/>
                                            </xsl:call-template>
                                        </author>
                                    </xsl:for-each>
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
                          <xsl:comment>
                           TODO: Columbia binding in field 563
                           ANSWER: YES
                          </xsl:comment>
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
                              <xsl:comment>
                              TODO: Add Columbia orgin info: coming from field 264
                              ANSWER: NO
                              </xsl:comment>

                                <origin>
                                    <xsl:for-each select="//marc:datafield[@tag='500']/marc:subfield[@code='a' and starts-with(., 'Origin:')]">
                                        <p>
                                            <xsl:value-of select="normalize-space(substring(.,8))"/>
                                        </p>
                                    </xsl:for-each>
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
                                    <xsl:for-each select="//marc:datafield[@tag='260']/marc:subfield[@code='a']">
                                        <origPlace>
                                            <xsl:call-template name="clean-up-text">
                                                <xsl:with-param name="some-text" select="."/>                                            </xsl:call-template>
                                        </origPlace>
                                    </xsl:for-each>
                                </origin>
                                <xsl:comment>
                                  TODO: CU MARC uses 541$a for acquistion; Question for Mitch/Dot: Use tei:acquisition or tei:provenance for this? We don't use tei:acquisition in any of our other TEI.
                                  ANSWER: YES ADD TO PROVENANCE ONLY
                                </xsl:comment>
                                <xsl:for-each select="//marc:datafield[@tag='561']">
                                    <provenance>
                                        <xsl:value-of select="marc:subfield[@code='a']"/>
                                    </provenance>
                                </xsl:for-each>

                            </history>
                        </msDesc>
                    </sourceDesc>
                </fileDesc>

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

            </teiHeader>
            <facsimile>
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
