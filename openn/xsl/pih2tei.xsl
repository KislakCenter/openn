<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    
    xmlns="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs xd"
    version="2.0">
    <xd:doc scope="stylesheet">
        <xd:desc>
            <xd:p><xd:b>Created on:</xd:b> Nov 19, 2013</xd:p>
            <xd:p><xd:b>Author:</xd:b> emeryr</xd:p>
            <xd:p>
                * title
                * creator (s)
                * date of origin
                * place of origin
                * summary/abstract
                * foliation so we can generate page labels
                * language(s)
                * item level content, if applicable, is optional
            </xd:p>
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
                                   <xsl:value-of select="/page/response/result/doc/arr[@name='titledate_field']/str"/>
                               </xsl:with-param>
                           </xsl:call-template>
                        </title>

                    </titleStmt>
                    <publicationStmt>
                        <publisher>Schoenberg Center for Electronic Text and Image, University of Pennsylvania</publisher>
                        <availability>
                            <p>This work and all referenced images are ©<xsl:value-of select="year-from-date(current-date())"></xsl:value-of> University of Pennsylvania. They are licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License, http://creativecommons.org/licenses/by-nc-sa/3.0/.</p>
                        </availability>
                    </publicationStmt>
                    <sourceDesc>
                        <msDesc>
                            <msIdentifier>
                                <settlement>Philadelphia</settlement>
                                <institution><xsl:value-of xmlns:marc="http://www.loc.gov/MARC21/slim" select="/page/response/result/doc/xml[@name='marcrecord']/marc:record/marc:datafield[@tag='852']/marc:subfield[@code='a']"></xsl:value-of></institution>
                                <repository><xsl:value-of xmlns:marc="http://www.loc.gov/MARC21/slim" select="/page/response/result/doc/xml[@name='marcrecord']/marc:record/marc:datafield[@tag='852']/marc:subfield[@code='b']"></xsl:value-of></repository>
                                <idno><xsl:value-of select="/page/response/result/doc/arr[@name='call_number_field']/str"></xsl:value-of></idno>
                            </msIdentifier>
                                <msContents>
                                    <summary>
                                        <xsl:value-of  xmlns:marc="http://www.loc.gov/MARC21/slim" select="normalize-space((/page/response/result/doc/xml[@name='marcrecord']/marc:record/marc:datafield[@tag='520']/marc:subfield[@code='a'])[last()])"/>
                                    </summary>
                                    <xsl:if test="/page/response/result/doc/arr[@name='language_field']/str">
                                        <textLang>
                                            <xsl:value-of select="normalize-space(/page/response/result/doc/arr[@name='language_field']/str)"/>
                                        </textLang>
                                    </xsl:if>
                                    <msItem>
                                        <title>
                                            <xsl:call-template name="clean-up-text">
                                                <xsl:with-param name="some-text" select="/page/response/result/doc/arr[@name='title_field']/str"/>
                                            </xsl:call-template>
                                        </title>
                                        <xsl:if test="/page/response/result/doc/arr[@name='author_field']/str">
                                        <author>
                                            <xsl:call-template name="clean-up-text">
                                                <xsl:with-param name="some-text" select="normalize-space(/page/response/result/doc/arr[@name='author_field']/str)"/>
                                            </xsl:call-template>
                                        </author>
                                        </xsl:if>
                                    </msItem>
                                    
                                </msContents>
                            <xsl:if test="count(//page/tocentry[@name='ill']) > 0">
                                <physDesc>
                                    <decoDesc>
                                        <xsl:for-each select="//page/tocentry[@name='ill']">
                                        <decoNote>
                                            <xsl:attribute name="n">
                                                <xsl:call-template name="clean-up-text">
                                                    <xsl:with-param name="some-text">
                                                        <xsl:value-of select="./parent::page/@visiblepage"/>
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
                                    <origDate>
                                        <xsl:choose  xmlns:marc="http://www.loc.gov/MARC21/slim" >
                                            <xsl:when test="/page/response/result/doc/arr[@name='probable_date_field']/str">
                                                <xsl:value-of select="/page/response/result/doc/arr[@name='probable_date_field']/str"></xsl:value-of>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:value-of select="/page/response/result/doc/xml[@name='marcrecord']/marc:record/marc:datafield[@tag='260']/marc:subfield[@code='c']"/>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </origDate>
                                    <xsl:variable name="orig-place">
                                        <xsl:value-of xmlns:marc="http://www.loc.gov/MARC21/slim" select="/page/response/result/doc/xml[@name='marcrecord']/marc:record/marc:datafield[@tag='260']/marc:subfield[@code='a']"></xsl:value-of>
                                    </xsl:variable>
                                    <xsl:if  test="$orig-place">
                                        <origPlace>
                                            <xsl:call-template name="clean-up-text"><xsl:with-param name="some-text" select="$orig-place"/></xsl:call-template>
                                        </origPlace>
                                    </xsl:if>
                                </origin>
                            </history>
                        </msDesc>
                    </sourceDesc>       
                </fileDesc>
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
            </facsimile>
        </TEI>
    </xsl:template>
    
    <xsl:template name="clean-up-text">
        <xsl:param name="some-text"/>
        <xsl:value-of select="normalize-space(replace(replace(replace($some-text, '[\[\]]', ''), ' \)', ')'), ',$',''))"></xsl:value-of>
    </xsl:template>
       
    
</xsl:stylesheet>
