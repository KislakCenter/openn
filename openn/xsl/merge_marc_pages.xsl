<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:output indent="yes"/>
    
    <xsl:param name="MARC_PATH"/>
    <xsl:template match="/">
        <wrapper>
            <xml name="marc">
                <xsl:copy-of select="document($MARC_PATH)"/>
            </xml>
            <xml name="pages">
              <xsl:for-each select="//pages/page">
                <xsl:variable name="display-page" select="./display_page/text()"/>
                <!--                 <xsl:variable name="image-name" select="./file_name/text()"/>-->
                <xsl:variable name="image-base" select="replace(./file_name/text(), '\.(jpeg|jpg|tiff|tif)', '', 'i')"/>
                <page>
                  <xsl:attribute name="number" select="./serial_number/text()"/>
                  <xsl:attribute name="id" select="$image-base"/>
                  <xsl:attribute name="seq" select="./serial_number/text()"/>
                  <xsl:attribute name="side">
                    <xsl:choose>
                      <xsl:when test="matches($display-page, '\dr', 'i') or matches($display-page, 'recto', 'i')">
                        <xsl:text>recto</xsl:text>
                      </xsl:when>
                      <xsl:when test="matches($display-page, '\dv', 'i') or matches($display-page, 'verso', 'i')">
                        <xsl:text>verso</xsl:text>
                      </xsl:when>
                      <!-- OK. We don't have r|v or recto|verso; guess based on position: odd => recto, else => verso -->                        
                      <xsl:when test="position() mod 2 = 1">
                        <xsl:text>recto</xsl:text>
                      </xsl:when>
                      <xsl:otherwise>
                        <xsl:text>verso</xsl:text>
                      </xsl:otherwise>
                    </xsl:choose>
                  </xsl:attribute>
                  <xsl:attribute name="image.id" select="$image-base"/>
                  <xsl:attribute name="image" select="$image-base"/>
                  <xsl:attribute name="visiblepage" select="$display-page"/>
                  <xsl:for-each select="./tags/tag[matches(name/text(),'TOC', 'i')]">
                    <tocentry name="toc"><xsl:value-of select="./value/text()"/></tocentry>
                  </xsl:for-each>
                  <xsl:for-each select="./tags/tag[matches(name/text(),'DECO', 'i')]">
                    <tocentry name="ill"><xsl:value-of select="./value/text()"/></tocentry>
                  </xsl:for-each>
                </page>
              </xsl:for-each>
            </xml>
        </wrapper>
    </xsl:template>
</xsl:stylesheet>