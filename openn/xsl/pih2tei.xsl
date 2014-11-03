<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns="http://www.tei-c.org/ns/1.0"
    xmlns:marc="http://www.loc.gov/MARC21/slim"
    exclude-result-prefixes="xs xd marc tei" version="2.0">
    <xd:doc scope="stylesheet">
        <xd:desc>
            <xd:p><xd:b>Created on:</xd:b> Nov 19, 2013</xd:p>
            <xd:p><xd:b>Author:</xd:b> emeryr</xd:p>
            <xd:p> * title * creator (s) * date of origin * place of origin * summary/abstract *
                foliation so we can generate page labels * language(s) * item level content, if
                applicable, is optional </xd:p>
            <xd:p><xd:b>dorp, October 27 2014, modified to add</xd:b></xd:p>
            <xd:p> * provenance * subject terms * genre/form terms * notes</xd:p>
            <xd:p><xd:b>rde, October 28, 2014, multiple chagnes</xd:b></xd:p>
            <xd:p>Pulling data from marc fields, instead of Penn in Hand "*_field" elements</xd:p>
            <xd:p>Tighten code; remove mid-tag line breaks</xd:p>
        </xd:desc>
    </xd:doc>

    <xsl:output indent="yes"/>

    <xsl:variable name="institution">
        <xsl:call-template name="clean-up-text">
            <xsl:with-param name="some-text" select="//marc:record/marc:datafield[@tag='852']/marc:subfield[@code='a']"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="repository">
        <xsl:call-template name="clean-up-text">
            <xsl:with-param name="some-text" select="//marc:record/marc:datafield[@tag='852']/marc:subfield[@code='b']"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="call_number">
        <xsl:call-template name="clean-up-text">
            <xsl:with-param name="some-text" select="//marc:datafield[@tag='099']/marc:subfield[@code='a']"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="ms_title">
        <xsl:call-template name="clean-up-text">
            <xsl:with-param name="some-text" select="//marc:datafield[@tag='245']/marc:subfield[@code='a']"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:template match="/">

        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title>
                            <xsl:value-of select="normalize-space(concat('Description of ', $institution, ' ', $call_number, ': ', $ms_title))"/>
                        </title>
                    </titleStmt>
                    <publicationStmt>
                        <publisher>The University of Pennsylvania Libraries</publisher>
                        <availability>
                            <licence target="http://creativecommons.org/licenses/by/4.0/legalcode">
                                This description is ©<xsl:value-of select="year-from-date(current-date())"/> University of Pennsylvania Libraries. It is licensed under a Creative Commons Attribution 4.0 International License (CC-BY 4.0), http://creativecommons.org/licenses/by/4.0/. Please see the license deed for details, http://creativecommons.org/licenses/by/4.0/.
                            </licence>
                            <licence target="http://creativecommons.org/publicdomain/mark/1.0/">
                                All images referenced here are in the public domain and are free for any use commercal or private. Please see the Creative Commons Public Domain Mark page for details, http://creativecommons.org/publicdomain/mark/1.0/.
                            </licence>
                        </availability>
                    </publicationStmt>

                    <!-- DOT ADDED NOTESSTMT TO HOLD ALL THE RANDOM NOTES FROM THE MARC RECORD -->
                    <xsl:if test="//marc:datafield[@tag='500']">
                        <notesStmt>
                            <xsl:for-each select="//marc:datafield[@tag='500']">
                                <note>
                                    <xsl:value-of select="normalize-space(marc:subfield[@code='a'])"/>
                                </note>
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
                                <idno type="call-number"><xsl:value-of select="$call_number"/></idno>
                                <altIdentifier type="bibid">
                                    <idno><xsl:value-of select="//marc:controlfield[@tag='001']"/></idno>
                                </altIdentifier>
                                <xsl:if test="//marc:datafield[@tag='856']/marc:subfield[@code='z' and matches(text(), 'facsimile', 'i')]">
                                    <altIdentifier type="hdl">
                                        <idno><xsl:value-of select="//marc:datafield[@tag='856']/marc:subfield[@code='z' and matches(text(), 'facsimile', 'i')]/parent::marc:datafield/marc:subfield[@code='u']"></xsl:value-of></idno>
                                    </altIdentifier>
                                </xsl:if>
                            </msIdentifier>
                            <msContents>
                                <summary>
                                    <xsl:value-of select="normalize-space((//marc:datafield[@tag='520']/marc:subfield[@code='a'])[last()])" />
                                </summary>

                                <xsl:if test="//marc:datafield[@tag='546']/marc:subfield[@code='a']">
                                    <textLang>
                                        <xsl:if test="//marc:datafield[@tag='041']/marc:subfield[@code='a']">
                                            <xsl:attribute name="mainLang" select="//marc:datafield[@tag='041']/marc:subfield[@code='a'][1]"/>
                                            <xsl:if test="count(//marc:datafield[@tag='041']/marc:subfield[@code='a']) &gt; 1">
                                                <xsl:attribute name="otherLangs">
                                                    <xsl:call-template name="other-langs">
                                                        <xsl:with-param name="tags" select="//marc:datafield[@tag='041']/marc:subfield[@code='a']"/>
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
                                    <xsl:if test="//marc:datafield[@tag='110']">
                                        <author>
                                            <xsl:call-template name="chomp-period">
                                                <xsl:with-param name="string" select="//marc:datafield[@tag='110']/marc:subfield[@code='a']"/>
                                            </xsl:call-template>
                                        </author>
                                    </xsl:if>
                                    <!-- marc 100: primary author, person -->
                                    <xsl:if test="//marc:datafield[@tag='100']">
                                        <author>
                                            <xsl:call-template name="extract-pn">
                                                <xsl:with-param name="datafield" select="//marc:datafield[@tag='100']"/>
                                            </xsl:call-template>
                                        </author>
                                    </xsl:if>
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
                                        <xsl:variable name="mixed" select="matches($support, 'parchment', 'i') and matches($support, 'paper', 'i')"/>
                                        <objectDesc>
                                            <supportDesc>
                                                <xsl:if test="$support">
                                                    <xsl:attribute name="material">
                                                        <xsl:choose>
                                                            <xsl:when test="$mixed">
                                                                <xsl:text>mixed</xsl:text>
                                                            </xsl:when>
                                                            <xsl:otherwise>
                                                                <xsl:value-of select="normalize-space($support)"/>
                                                            </xsl:otherwise>
                                                        </xsl:choose>
                                                    </xsl:attribute>
                                                </xsl:if>
                                                <xsl:if test="$support">
                                                    <support><xsl:value-of select="$support"/></support>
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
                                            </supportDesc>
                                        </objectDesc>
                                    </xsl:if>
                                    <xsl:if test="count(//page/tocentry[@name='ill']) > 0">
                                        <decoDesc>
                                        <xsl:for-each select="//page/tocentry[@name='ill']">
                                            <decoNote>
                                                <xsl:attribute name="n">
                                                  <xsl:call-template name="clean-up-text">
                                                  <xsl:with-param name="some-text" select="./parent::page/@visiblepage" />
                                                  </xsl:call-template>
                                                </xsl:attribute>
                                                <xsl:value-of select="normalize-space(.)"/>
                                            </decoNote>
                                        </xsl:for-each>
                                    </decoDesc>
                                    </xsl:if>
                                </physDesc>
                            <history>
                                <origin>

                                    <!-- DOT ADDED AN IF STATEMENT AROUND ORIGDATE, SO IF THERE IS NO ORIGDATE IN THE MARC RECORD ORIGDATE WILL NOT BE CREATED -->
                                    <!-- DE: just use the marc field -->
                                    <xsl:if test="//marc:datafield[@tag='260']/marc:subfield[@code='c']">
                                        <origDate>
                                            <xsl:call-template name="clean-up-text">
                                                <xsl:with-param name="some-text" select="//marc:datafield[@tag='260']/marc:subfield[@code='c']"/>
                                            </xsl:call-template>
                                        </origDate>
                                    </xsl:if>
                                    <!-- END DOT MOD -->

                                    <!-- DE: Cleaner code for origPlace; add only if present -->
                                    <xsl:if test="//marc:datafield[@tag='260']/marc:subfield[@code='a']">
                                        <origPlace>
                                            <xsl:call-template name="clean-up-text">
                                                <xsl:with-param name="some-text" select="//marc:datafield[@tag='260']/marc:subfield[@code='a']"/>
                                            </xsl:call-template>
                                        </origPlace>
                                    </xsl:if>
                                </origin>

                                <!-- DOT ADDED PROVENANCE -->
                                <xsl:if test="//marc:datafield[@tag='561']">
                                    <xsl:for-each select="//marc:datafield[@tag='561']">
                                        <provenance>
                                            <xsl:value-of select="marc:subfield[@code='a']"/>
                                        </provenance>
                                    </xsl:for-each>
                                </xsl:if>
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
        <xsl:value-of select="normalize-space(replace(replace(replace($some-text, '[\[\]]', ''), ' \)', ')'), ',$',''))"
        />
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
