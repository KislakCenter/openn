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
                   <page></page>
               </xsl:for-each>
            </xml>
        </wrapper>
    </xsl:template>
</xsl:stylesheet>