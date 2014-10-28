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
        </xd:desc>
    </xd:doc>

    <xsl:output indent="yes"/>

    <xsl:template match="/">
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title>
                            <xsl:call-template name="clean-up-text">
                                <xsl:with-param name="some-text">
                                    <xsl:text>Description of </xsl:text>
                                    <xsl:value-of
                                        select="/page/response/result/doc/arr[@name='titledate_field']/str"
                                    />
                                </xsl:with-param>
                            </xsl:call-template>
                        </title>

                    </titleStmt>
                    <publicationStmt>
                        <publisher>Schoenberg Center for Electronic Text and Image, University of
                            Pennsylvania</publisher>
                        <availability>
                            <licence
                                target="http://creativecommons.org/licenses/by-nc/4.0/legalcode">
                                This work and all referenced images are ©<xsl:value-of
                                    select="year-from-date(current-date())"/> University of
                                Pennsylvania. They are licensed under a Creative Commons
                                Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0),
                                http://creativecommons.org/licenses/by-nc/4.0/. </licence>
                        </availability>
                    </publicationStmt>
                    
                    <!-- DOT ADDED NOTESSTMT TO HOLD ALL THE RANDOM NOTES FROM THE MARC RECORD -->
                    <xsl:if
                        test="//marc:datafield[@tag='500']">
                        <notesStmt>
                            <xsl:for-each
                                select="//marc:datafield[@tag='500']">
                                <note>
                                    <xsl:value-of select="marc:subfield[@code='a']"/>
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
                                    <xsl:value-of
                                        select="/page/response/result/doc/xml[@name='marcrecord']/marc:record/marc:datafield[@tag='852']/marc:subfield[@code='a']"
                                    />
                                </institution>
                                <repository>
                                    <xsl:value-of
                                        select="/page/response/result/doc/xml[@name='marcrecord']/marc:record/marc:datafield[@tag='852']/marc:subfield[@code='b']"
                                    />
                                </repository>
                                <idno>
                                    <xsl:value-of
                                        select="/page/response/result/doc/arr[@name='call_number_field']/str"
                                    />
                                </idno>
                            </msIdentifier>
                            <msContents>
                                <summary>
                                    <xsl:value-of
                                        select="normalize-space((/page/response/result/doc/xml[@name='marcrecord']/marc:record/marc:datafield[@tag='520']/marc:subfield[@code='a'])[last()])"
                                    />
                                </summary>

                                <xsl:if
                                    test="/page/response/result/doc/arr[@name='language_field']/str">
                                    <textLang>
                                        <xsl:value-of
                                            select="normalize-space(/page/response/result/doc/arr[@name='language_field']/str)"
                                        />
                                    </textLang>
                                </xsl:if>
                                <msItem>
                                    <title>
                                        <xsl:call-template name="clean-up-text">
                                            <xsl:with-param name="some-text"
                                                select="/page/response/result/doc/arr[@name='title_field']/str"
                                            />
                                        </xsl:call-template>
                                    </title>
                                    <xsl:if
                                        test="/page/response/result/doc/arr[@name='author_field']/str">
                                        <author>
                                            <xsl:call-template name="clean-up-text">
                                                <xsl:with-param name="some-text"
                                                  select="normalize-space(/page/response/result/doc/arr[@name='author_field']/str)"
                                                />
                                            </xsl:call-template>
                                        </author>
                                    </xsl:if>
                                </msItem>

                                <xsl:for-each select="//page/tocentry[@name='toc']">
                                    <xsl:variable name="locus" select="./parent::page/@visiblepage"/>
                                    <msItem>
                                        <xsl:attribute name="n">
                                            <xsl:call-template name="clean-up-text">
                                                <xsl:with-param name="some-text">
                                                  <xsl:value-of select="$locus"/>
                                                </xsl:with-param>
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
                            <xsl:if test="count(//page/tocentry[@name='ill']) > 0">
                                <physDesc>
                                    <decoDesc>
                                        <xsl:for-each select="//page/tocentry[@name='ill']">
                                            <decoNote>
                                                <xsl:attribute name="n">
                                                  <xsl:call-template name="clean-up-text">
                                                  <xsl:with-param name="some-text">
                                                  <xsl:value-of select="./parent::page/@visiblepage"
                                                  />
                                                  </xsl:with-param>
                                                  </xsl:call-template>
                                                </xsl:attribute>
                                                <xsl:value-of select="normalize-space(.)"/>
                                            </decoNote>
                                        </xsl:for-each>
                                    </decoDesc>
                                </physDesc>
                            </xsl:if>
                            <history>
                                <origin>
                                    
                                    <!-- DOT ADDED AN IF STATEMENT AROUND ORIGDATE, SO IF THERE IS NO ORIGDATE IN THE MARC RECORD ORIGDATE WILL NOT BE CREATED -->
                                    <xsl:if test="/page/response/result/doc/arr[@name='probable_date_field']/str"><origDate>
                                        <xsl:choose>
                                            <xsl:when
                                                test="/page/response/result/doc/arr[@name='probable_date_field']/str">
                                                <xsl:value-of
                                                  select="/page/response/result/doc/arr[@name='probable_date_field']/str"
                                                />
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:value-of
                                                  select="/page/response/result/doc/xml[@name='marcrecord']/marc:record/marc:datafield[@tag='260']/marc:subfield[@code='c']"
                                                />
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </origDate></xsl:if>
                                    
                                    <!-- END DOT MOD -->
                                    
                                    <xsl:variable name="orig-place">
                                        <xsl:value-of
                                            select="/page/response/result/doc/xml[@name='marcrecord']/marc:record/marc:datafield[@tag='260']/marc:subfield[@code='a']"
                                        />
                                    </xsl:variable>
                                    <xsl:if test="$orig-place">
                                        <origPlace>
                                            <xsl:call-template name="clean-up-text">
                                                <xsl:with-param name="some-text"
                                                  select="$orig-place"/>
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
                        <xsl:if test="//marc:datafield[@tag='610']">
                            <keywords xmlns="http://www.tei-c.org/ns/1.0" n="subjects">
                                <list>
                                    <xsl:for-each select="//marc:datafield[@tag='610']">
                                        <item>
                                            <xsl:call-template name="join-subfields">
                                                <xsl:with-param name="datafield" select="."/>
                                            </xsl:call-template>
                                        </item>
                                    </xsl:for-each>
                                </list>
                            </keywords>
                        </xsl:if>
                        <xsl:if test="//marc:datafield[@tag='655']/marc:subfield[@code='a']">
                            <keywords n="form/genre">
                                <list>
                                    <xsl:for-each select="//marc:datafield[@tag='655']/marc:subfield[@code='a']">
                                        <item><xsl:value-of select="."/></item>
                                    </xsl:for-each>
                                </list>
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
        <xsl:value-of
            select="normalize-space(replace(replace(replace($some-text, '[\[\]]', ''), ' \)', ')'), ',$',''))"
        />
    </xsl:template>
    
    <xsl:template name="join-subfields">
        <xsl:param name="datafield"/>
        <xsl:for-each select="./marc:subfield">
           <xsl:value-of select="."/>
            <xsl:if test="position() != last()">
                <xsl:text> - </xsl:text>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>
    

</xsl:stylesheet>
