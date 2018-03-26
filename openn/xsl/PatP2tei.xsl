<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
  xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns="http://www.tei-c.org/ns/1.0"
  xmlns:marc="http://www.loc.gov/MARC21/slim" exclude-result-prefixes="xs xd marc tei" version="2.0">
  <xd:doc scope="stylesheet">
    <xd:desc>
      <xd:p><xd:b>Created on:</xd:b> Nov 19, 2013</xd:p>
      <xd:p><xd:b>Author:</xd:b> emeryr</xd:p>
      <xd:p> * title * creator (s) * date of origin * place of origin * summary/abstract * foliation
        so we can generate page labels * language(s) * item level content, if applicable, is
        optional </xd:p>
      <xd:p>
        <xd:b>dorp, October 27 2014, modified to add</xd:b>
      </xd:p>
      <xd:p> * provenance * subject terms * genre/form terms * notes</xd:p>
      <xd:p>
        <xd:b>rde, October 28, 2014, multiple chagnes</xd:b>
      </xd:p>
      <xd:p>Pulling data from marc fields, instead of Penn in Hand "*_field" elements</xd:p>
      <xd:p>Tighten code; remove mid-tag line breaks</xd:p>
      <xd:p>
        <xd:b>dorp, January 23 2015, modified to add</xd:b>
      </xd:p>
      <xd:p> *Foliation *Layout *Colophon *Collation *Script *Decoration *Binding *Origin
        *Watermarks *Signatures</xd:p>
      <xd:p>
        <xd:b>emeryr, January 27 2015, fix bugs, tighten code to</xd:b>
      </xd:p>
      <xd:p> prefer for-each elements to if/for-each combinations where possible</xd:p>
      <xd:p>
        <xd:b>emeryr, February 5, 2015, modified to add</xd:b>
      </xd:p>
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
  <!--  The way call number is pulled now is bad. The XSL pulls the first
        holding from the list of holdings and gets that call number. How do
        we distinguish which call number? Require the holdings number as input?
        A: We will need to build a way to pull the correct holding, probably using
        holdings ID.
  -->
  <xsl:variable name="call_number">
    <xsl:call-template name="clean-up-text">
      <xsl:with-param name="some-text" select="//marc:holding[1]/marc:call_number"/>
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
      <xsl:comment>
        DE: Note that below I'm not consistent about marking the source marc field as @type.
          That's coming from a template I've copied *some* stuff from.
          A: Use type: with 245a have "Description of xxxxx..."
      </xsl:comment>
      <xsl:comment>
        DE: I haven't looked at the title@level attribute. Need to make sure this being used consistently.
        A: Remove @level
      </xsl:comment>
      <teiHeader>
        <fileDesc>
          <titleStmt>
            <xsl:for-each select="//marc:datafield[@tag=245]">
              <xsl:for-each select="marc:subfield">
                <xsl:if test="@code='a'">
                  <title>
                    <xsl:attribute name="type">marc245a</xsl:attribute>
                    <xsl:text>Description of </xsl:text>
                    <xsl:call-template name="chopPunctuation">
                      <xsl:with-param name="chopString">
                        <xsl:value-of select="."/>
                      </xsl:with-param>
                    </xsl:call-template>
                  </title>
                </xsl:if>
              </xsl:for-each>
            </xsl:for-each>
            <xsl:for-each
              select="//marc:datafield[@tag=100]|//marc:datafield[@tag=110]|//marc:datafield[@tag=111]">
<!--              No author for Penn catalog records. -->
              <author>
                <xsl:call-template name="subfieldSelect">
                  <xsl:with-param name="codes">abcdgu</xsl:with-param>
                </xsl:call-template>
              </author>
            </xsl:for-each>
            <xsl:for-each
              select="//marc:datafield[@tag=700]|//marc:datafield[@tag=710]|//marc:datafield[@tag=500]">
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
<!--              Only Public Domain print works will go on OPenn -->
              <licence target="http://creativecommons.org/licenses/by/4.0/legalcode"> This
                description is ©<xsl:value-of select="year-from-date(current-date())"/> University
                of Pennsylvania Libraries. It is licensed under a Creative Commons Attribution
                License version 4.0 (CC-BY-4.0
                https://creativecommons.org/licenses/by/4.0/legalcode. For a description of the
                terms of use see the Creative Commons Deed
                https://creativecommons.org/licenses/by/4.0/. </licence>
              <licence target="http://creativecommons.org/publicdomain/mark/1.0/"> All referenced
                images and their content are free of known copyright restrictions and in the public
                domain. See the Creative Commons Public Domain Mark page for usage details,
                http://creativecommons.org/publicdomain/mark/1.0/. </licence>
            </availability>
            <xsl:comment>
              DE: We also haven't had a publication date. We should. Date the TEI is generated?
              A: use year
              @done
            </xsl:comment>
            <date>
              <xsl:attribute name="when">
                <xsl:value-of select="year-from-date(current-date())"/>
              </xsl:attribute>
            </date>
          </publicationStmt>
          <sourceDesc>
            <biblStruct>
              <monogr>
                <xsl:for-each
                  select="//marc:datafield[@tag=100]|//marc:datafield[@tag=110]|//marc:datafield[@tag=700]">
                  <!-- Don't pull 710. That's the collection @done -->
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
                <xsl:for-each
                  select="//marc:datafield[@tag=130]|//marc:datafield[@tag=240]|//marc:datafield[@tag=246]">
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
                  <!--
                    pubPlace pull prefer 752$a$d (order: '$d, $a'); fallback to 260$a @done
                  -->
                  <xsl:variable name="marc752a">
                    <xsl:call-template name="chopPunctuation">
                      <xsl:with-param name="chopString" select="//marc:datafield[@tag=752]/marc:subfield[@code='a']"/>
                    </xsl:call-template>
                  </xsl:variable>
                  <xsl:variable name="marc752d">
                    <xsl:call-template name="chopPunctuation">
                      <xsl:with-param name="chopString" select="//marc:datafield[@tag=752]/marc:subfield[@code='d']"/>
                    </xsl:call-template>
                  </xsl:variable>
                  <xsl:variable name="marc260a">
                    <xsl:call-template name="chopPunctuation">
                      <xsl:with-param name="chopString" select="//marc:datafield[@tag=260]/marc:subfield[@code='a']"/>
                    </xsl:call-template>
                  </xsl:variable>
                  <xsl:call-template name="pubPlace">
                    <xsl:with-param name="marc752d" select="$marc752d"/>
                    <xsl:with-param name="marc752a" select="$marc752a"/>
                    <xsl:with-param name="marc260a" select="$marc260a"/>
                  </xsl:call-template>
                  <xsl:choose>
                    <xsl:when test="//marc:datafield[@tag=752]/marc:subfield[@code='a']|//marc:datafield[@tag=752]/marc:subfield[@code='d']">
                      <pubPlace>
                      <xsl:choose>
                        <xsl:when test="//marc:datafield[@tag=752]/marc:subfield[@code='a'] and //marc:datafield[@tag=752]/marc:subfield[@code='d']">
                          <xsl:call-template name="chopPunctuation">
                            <xsl:with-param name="chopString">
                              <xsl:value-of select="//marc:datafield[@tag=752]/marc:subfield[@code='d']"/>
                            </xsl:with-param>
                          </xsl:call-template>
                          <xsl:text>, </xsl:text>
                          <xsl:call-template name="chopPunctuation">
                            <xsl:with-param name="chopString">
                              <xsl:value-of select="//marc:datafield[@tag=752]/marc:subfield[@code='a']"/>
                            </xsl:with-param>
                          </xsl:call-template>
                        </xsl:when>
                        <xsl:when test="//marc:datafield[@tag=752]/marc:subfield[@code='a']">
                          <xsl:call-template name="chopPunctuation">
                            <xsl:with-param name="chopString">
                              <xsl:value-of select="//marc:datafield[@tag=752]/marc:subfield[@code='a']"/>
                            </xsl:with-param>
                          </xsl:call-template>
                        </xsl:when>
                        <xsl:otherwise>
                          <xsl:call-template name="chopPunctuation">
                            <xsl:with-param name="chopString">
                              <xsl:value-of select="//marc:datafield[@tag=752]/marc:subfield[@code='d']"/>
                            </xsl:with-param>
                          </xsl:call-template>
                        </xsl:otherwise>
                      </xsl:choose>
                      </pubPlace>
                    </xsl:when>
                    <xsl:when test="//marc:datafield[@tag=260]/marc:subfield[@code='a']">
                      <pubPlace>
                        <xsl:call-template name="chopPunctuation">
                          <xsl:with-param name="chopString">
                            <xsl:value-of select="//marc:datafield[@tag=260]/marc:subfield[@code='a']"/>
                          </xsl:with-param>
                        </xsl:call-template>
                      </pubPlace>
                    </xsl:when>
                  </xsl:choose>
                  <xsl:for-each select="//marc:datafield[@tag=260]/marc:subfield[@code='b']">
                    <publisher>
                      <xsl:call-template name="chopPunctuation">
                        <xsl:with-param name="chopString">
                          <xsl:value-of select="."/>
                        </xsl:with-param>
                      </xsl:call-template>
                    </publisher>
                  </xsl:for-each>
                  <xsl:variable name="marc008" select="//marc:controlfield[@tag='008']"/>
                  <xsl:variable name="pubDateFrom">
                    <xsl:call-template name="extractPubDateFrom">
                      <xsl:with-param name="marc008" select="$marc008"/>
                    </xsl:call-template>
                  </xsl:variable>
                  <xsl:variable name="pubDateTo">
                    <xsl:call-template name="extractPubDateTo">
                      <xsl:with-param name="marc008" select="$marc008"/>
                    </xsl:call-template>
                  </xsl:variable>
                  <xsl:variable name="pubDateWhen">
                    <xsl:call-template name="extractPubDateWhen">
                      <xsl:with-param name="marc008" select="$marc008"/>
                    </xsl:call-template>
                  </xsl:variable>
                  <xsl:variable name="marc260c">
                    <xsl:call-template name="chopPunctuation">
                      <xsl:with-param name="chopString">
                        <xsl:value-of select="//marc:controlfield[@tag='260']/marc:subfield[@code='c']"/>
                      </xsl:with-param>
                    </xsl:call-template>
                  </xsl:variable>
                  <xsl:variable name="pubDateText">
                    <xsl:call-template name="dateString">
                      <xsl:with-param name="marc260c" select="$marc260c"/>
                      <xsl:with-param name="dateWhen" select="$pubDateWhen"/>
                      <xsl:with-param name="dateFrom" select="$pubDateFrom"/>
                      <xsl:with-param name="dateTo"   select="$pubDateTo"/>
                    </xsl:call-template>
                  </xsl:variable>
                  <!--
                    DE: Is this dangerous? Can it be a range? An LC partial date? Circa date?
                    They won't validate as date attributes. (DE)
                    A: pull ctrl field 008 positions 7-10; figure out if number.
                    @done
                    Samples:
                    #12345678901234567890
                    #131218q19001936mr
                    #12345678901234567890
                    #930202s1980
                    See: https://www.loc.gov/marc/bibliographic/bd008a.html
                    06 - Type of date/Publication status
                          b - No dates given; B.C. date involved
                          c - Continuing resource currently published
                          d - Continuing resource ceased publication
                          e - Detailed date
                          i - Inclusive dates of collection
                          k - Range of years of bulk of collection
                          m - Multiple dates
                          n - Dates unknown
                    Common s, q, m, new data starts at character 15.
                    Multiple date codes: c, d, i, k, m
                    For 'c' see: https://franklin.library.upenn.edu/catalog/FRANKLIN_9937563503681
                        008 920427c18459999nyumr p 0 a0eng
                    TODO: 260$c for publication date - the title page date in brackets if not on title page and 'n.d.' if 'no date';
                    'n.d.' algorithm: strip non-alnum chars; downcase; if val == 'nd' => 'no date'
                    -->
                  <xsl:if test="$pubDateFrom or $pubDateTo or $pubDateWhen">
                    <date>
                      <xsl:choose>
                        <xsl:when test="$pubDateWhen">
                          <xsl:attribute name="when" select="$pubDateWhen"/>
                        </xsl:when>
                        <xsl:otherwise>
                          <xsl:if test="$pubDateFrom">
                            <xsl:attribute name="from" select="$pubDateFrom"/>
                          </xsl:if>
                          <xsl:if test="$pubDateTo">
                            <xsl:attribute name="to" select="$pubDateTo"/>
                          </xsl:if>
                        </xsl:otherwise>
                      </xsl:choose>
                    </date>
                  </xsl:if>
                </imprint>
                <xsl:comment>
                    DE: I'm skipping subfield 'b' here. It should be combined with 'a' if it exists.
                    A: Join $a $c; remove trailing :; and join with '; '
                 </xsl:comment>
                <xsl:for-each select="//marc:datafield[@tag=300]/marc:subfield">
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
                <xsl:comment>
                TODO: Need to examine our marc and figure out which to use. TEI
                  recommends 4xx and 8xx be used here, without providing much detail. Need to
                  investigate subfield. In sample marc, we use 440, 490, 810, 830, 856; the last
                  being the facsimile.
                  A: 440$a | 490$a | 830$a in that order, with $v if it is there
                </xsl:comment>
                <title level="s">????</title>
              </series>
              <xsl:if test="//marc:datafield[@tag='500']">
                <xsl:for-each select="//marc:datafield[@tag='500']">
                  <note>
                    <xsl:value-of select="normalize-space(marc:subfield[@code='a'])"/>
                  </note>
                </xsl:for-each>
              </xsl:if>
              <xsl:comment>
                <xsl:text>
                  The way call number is pulled now is bad. The XSL pulls the first
                  holding from the list of holdings and gets that call number. How do
                  we distinguish which call number? Require the holdings number as input?
                  A: Require holding ID and translate and prepend subcollection `scforr`, `scsing`.
                </xsl:text>
              </xsl:comment>
              <idno>
                <xsl:attribute name="type">
                  <xsl:text>LC_call_number</xsl:text>
                </xsl:attribute>
                <xsl:value-of select="$call_number"/>
              </idno>
              <idno>
                <xsl:attribute name="type">
                  <xsl:text>bibid</xsl:text>
                </xsl:attribute>
                <xsl:value-of select="$bibid"/>
              </idno>
              <xsl:comment>
                DE: Related item -- TEI recommendations only have pulling from 740 field, but
                    also mention &lt;author&gt;, without saying where to pull the value. Can
                    we provide author, based on how we catalog?
              </xsl:comment>
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
        <xsl:comment>
          DE: Stuff to address, lost to the removal of msDesc:
              - provenance
              - section, chapter names?
              - illustrations?
           A: email Dot, cc'ing group; also LVT to find examples
        </xsl:comment>
        <encodingDesc>
          <xsl:comment>
            DE: We haven't had  projectDesc. Do we want one?
          </xsl:comment>
          <projectDesc><p>????</p></projectDesc>
          <classDecl>
          <xsl:comment>
            DE: Do we want to use these taxonomy tags for keywords? If so, what taxonomy goes with what?
          </xsl:comment>
          <taxonomy xml:id="LCC"><bibl>Library of Congress Classification</bibl></taxonomy>
          <taxonomy xml:id="LCSH"><bibl>Library of Congress Subject Headings</bibl></taxonomy>
          </classDecl>
        </encodingDesc>
        <profileDesc>
          <xsl:comment>
            Language: Found an item (bibid: 1761820, 9917618203503681) with 041$a (=eng)
            and 041$h (=fre). Work is an English translation from French. How to handle?
            A: Pull 041$a however many times it occurs -- can be multiple.
            https://www.loc.gov/marc/bibliographic/bd041.html
          </xsl:comment>
          <xsl:if test="//marc:datafield[@tag='041']">
            <langUsage>
            <xsl:for-each select="//marc:datafield[@tag='041']">
              <xsl:for-each select="marc:subfield">
                <language>
                  <xsl:attribute name="ident" select="."/>
                </language>
              </xsl:for-each>
            </xsl:for-each>
            </langUsage>
          </xsl:if>
          <textClass>
            <xsl:comment>
              DE: classCode@scheme based on 050-099 -- Do we want to map these?
            </xsl:comment>
            <xsl:comment>
              DE: Keywords -- Which types/tags will we have? Do we want to map them to
              the taxonomies as suggested in the TEI recommendations (see above)?
            </xsl:comment>
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
                <xsl:for-each
                  select="//marc:datafield[@tag='655' and child::marc:subfield[@code='a']]">
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
    <xsl:param name="marc260c"/>
    <xsl:param name="dateWhen"/>
    <xsl:param name="dateFrom"/>
    <xsl:param name="dateTo"/>
    <xsl:choose>
      <xsl:when test="$marc260c">
        <xsl:value-of select="$marc260c"/>
      </xsl:when>
      <xsl:when test="$dateWhen">
        <xsl:value-of select="$dateWhen"/>
      </xsl:when>
      <xsl:when test="$dateFrom or $dateTo">
        <xsl:variable name="text">
          <xsl:value-of select="$dateFrom"/>
          <xsl:text> - </xsl:text>
          <xsl:value-of select="$dateTo"/>
        </xsl:variable>
          <xsl:value-of select="normalize-space($text)"/>
      </xsl:when>
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
          <xsl:value-of select="$marc752d"/>
          <xsl:if test="$marc752a">
            <xsl:text>, </xsl:text>
            <xsl:value-of select="$marc752a"/>
          </xsl:if>
        </xsl:when>
        <xsl:when test="$marc752a">
          <xsl:value-of select="$marc752a"/>
        </xsl:when>
        <xsl:when test="$marc260a">
         <xsl:value-of select="$marc260a"/>
        </xsl:when>
      </xsl:choose>
      </pubPlace>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>