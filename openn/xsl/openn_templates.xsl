<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
  xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns="http://www.tei-c.org/ns/1.0"
  xmlns:marc="http://www.loc.gov/MARC21/slim" exclude-result-prefixes="xs xd marc tei"
  version="2.0">
  <xd:doc scope="stylesheet">
    <xd:desc>
      <xd:p><xd:b>Created on:</xd:b> Mar 29, 2018</xd:p>
      <xd:p><xd:b>Author:</xd:b> emeryr</xd:p>
      <xd:p></xd:p>
    </xd:desc>
  </xd:doc>
  <xsl:template name="clean-up-text">
    <xsl:param name="some-text"/>
    <xsl:value-of
      select="normalize-space(replace(replace(replace($some-text, '[\[\]]', ''), ' \)', ')'), ',$',''))"
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
        <xsl:for-each
          select="$datafield/marc:subfield[@code='a' or @code='b' or @code='c' or @code='d']">
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
    <xsl:param name="source"/>
    <!-- 'paper with parchment tags' -->
    <xsl:param name="strings"/>
    <!-- 'paper parch papyrus palm'  -->
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
    <xsl:param name="ind1">
      <xsl:text> </xsl:text>
    </xsl:param>
    <xsl:param name="ind2">
      <xsl:text> </xsl:text>
    </xsl:param>
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
    <xsl:param name="delimeter">
      <xsl:text> </xsl:text>
    </xsl:param>
    <xsl:variable name="str">
      <xsl:for-each select="marc:subfield">
        <xsl:if test="contains($codes, @code)">
          <xsl:value-of select="text()"/>
          <xsl:value-of select="$delimeter"/>
        </xsl:if>
      </xsl:for-each>
    </xsl:variable>
    <xsl:value-of select="substring($str,1,string-length($str)-string-length($delimeter))"/>
  </xsl:template>
  <xsl:template name="buildSpaces">
    <xsl:param name="spaces"/>
    <xsl:param name="char">
      <xsl:text> </xsl:text>
    </xsl:param>
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
      <xsl:otherwise>
        <xsl:value-of select="$chopString"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  <xsl:template name="chopPunctuation">
    <xsl:param name="chopString"/>
    <xsl:variable name="length" select="string-length($chopString)"/>
    <xsl:choose>
      <xsl:when test="$length=0"/>
      <xsl:when test="contains('..:,;/ ', substring($chopString,$length,1))">
        <xsl:call-template name="chopPunctuation">
          <xsl:with-param name="chopString" select="substring($chopString,1,$length - 1)"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:when test="not($chopString)"/>
      <xsl:otherwise>
        <xsl:value-of select="$chopString"/>
      </xsl:otherwise>
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
  <xsl:template name="extractPubDateWhen">
    <xsl:param name="marc008"/>
    <xsl:variable name="dateCode" select="substring($marc008, 7, 1)"/>
    <!--  Use multiple date codes: c, d, i, k, m-->
    <xsl:if test="not(contains('cdikm', $dateCode))">
      <xsl:variable name="datePortion" select="substring($marc008, 8, 4)"/>
      <xsl:if test="matches($datePortion, '^\d+$')">
        <xsl:value-of select="$datePortion"/>
      </xsl:if>
    </xsl:if>
  </xsl:template>
  <xsl:template name="extractPubDateFrom">
    <xsl:param name="marc008"/>
    <xsl:variable name="dateCode" select="substring($marc008, 7, 1)"/>
    <!--  Use multiple date codes: c, d, i, k, m-->
    <xsl:if test="$dateCode = 'm'">
      <xsl:variable name="datePortion" select="substring($marc008, 8, 4)"/>
      <xsl:if test="contains('cdikm', $dateCode)">
        <xsl:value-of select="$datePortion"/>
      </xsl:if>
    </xsl:if>
  </xsl:template>
  <xsl:template name="extractPubDateTo">
    <xsl:param name="marc008"/>
    <xsl:variable name="dateCode" select="substring($marc008, 7, 1)"/>
    <!--  Use multiple date codes: c, d, i, k, m-->
    <xsl:if test="contains('cdikm', $dateCode)">
      <xsl:variable name="toDatePortion" select="substring($marc008, 12, 4)"/>
      <xsl:if test="matches($toDatePortion, '^\d+$')">
        <xsl:value-of select="$toDatePortion"/>
      </xsl:if>
    </xsl:if>
  </xsl:template>
  
  <xsl:template name="dateString">
<!--    
      TODO: Is this how we want to sdo this, or should we prefer the 260c for the date string? 
    -->
    <xsl:param name="marc260c"/>
    <xsl:param name="marc008"/>
    <xsl:variable name="dateCode" select="substring($marc008, 7, 1)"/>
    <xsl:choose>
      <xsl:when test="$marc260c">
        <xsl:call-template name="chopPunctuation">
          <xsl:with-param name="chopString" select="$marc260c"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:when test="contains('cdikm', $dateCode)">
        <xsl:value-of select="substring($marc008, 8, 4)"/>
        <xsl:text> - </xsl:text>
        <xsl:value-of select="substring($marc008, 12, 4)"/>
       </xsl:when>
      <xsl:when test="not(contains('cdikm', $dateCode))">
        <xsl:value-of select="substring($marc008, 8, 4)"/>
      </xsl:when>
    </xsl:choose>
  </xsl:template>
  
  
  <xsl:template name="dateAttributes">
    <xsl:param name="marc008"/>
    <xsl:variable name="dateCode" select="substring($marc008, 7, 1)"/>
    <xsl:choose>
      <xsl:when test="contains('cdikm', $dateCode)">
        <xsl:variable name="fromDatePortion" select="substring($marc008, 8, 4)"/>
        <xsl:variable name="toDatePortion" select="substring($marc008, 12, 4)"/>
        <xsl:if test="matches($fromDatePortion, '^\d+$')">
          <xsl:attribute name="from" select="$fromDatePortion"/>
        </xsl:if>
        <xsl:if test="matches($toDatePortion, '^\d+$')">
          <xsl:attribute name="to" select="$toDatePortion"/>
        </xsl:if>
      </xsl:when>
      <xsl:otherwise>
        <xsl:variable name="datePortion" select="substring($marc008, 8, 4)"/>
        <xsl:if test="matches($datePortion, '^\d+$')">
          <xsl:attribute name="when" select="$datePortion"/>
        </xsl:if>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
  <xsl:template name="pubPlace">
    <xsl:param name="marc752d"/>
    <xsl:param name="marc752a"/>
    <xsl:param name="marc260a"/>
    <xsl:if test="$marc752d or $marc752a or $marc260a">
      <pubPlace>
        <xsl:choose>
          <xsl:when test="$marc752d">
            <xsl:call-template name="chopPunctuation">
              <xsl:with-param name="chopString" select="$marc752d"/>
            </xsl:call-template>
            <xsl:if test="$marc752a">
              <xsl:text>, </xsl:text>
              <xsl:call-template name="chopPunctuation">
                <xsl:with-param name="chopString" select="$marc752a"/>
              </xsl:call-template>
            </xsl:if>
          </xsl:when>
          <xsl:when test="$marc752a">
            <xsl:call-template name="chopPunctuation">
              <xsl:with-param name="chopString" select="$marc752a"/>
            </xsl:call-template>
          </xsl:when>
          <xsl:when test="$marc260a">
            <xsl:call-template name="chopPunctuation">
              <xsl:with-param name="chopString" select="$marc260a"/>
            </xsl:call-template>
          </xsl:when>
        </xsl:choose>
      </pubPlace>
    </xsl:if>
  </xsl:template>
  
  <xsl:template name="seriesTitle">
    <xsl:param name="seriesElement"/>
    <series>
      <title>
        <xsl:call-template name="chopPunctuation">
          <xsl:with-param name="chopString" select="$seriesElement/marc:subfield[@code='a']"/>
        </xsl:call-template>
        <xsl:if test="$seriesElement/marc:subfield[@code='v']">
          <xsl:text> </xsl:text>
          <xsl:call-template name="chopPunctuation">
            <xsl:with-param name="chopString" select="$seriesElement/marc:subfield[@code='v']"/>
          </xsl:call-template>
        </xsl:if>
      </title>
    </series>
  </xsl:template>
  
  <xsl:template name="join-text">
    <xsl:param name="nodes"/>
    <xsl:param name="separator" select="', '"/>
    <xsl:for-each select="$nodes">
      <xsl:value-of select="text()"/>
      <xsl:if test="position() != last()">
        <xsl:value-of select="$separator"/>
      </xsl:if>
    </xsl:for-each>
  </xsl:template>
</xsl:stylesheet>