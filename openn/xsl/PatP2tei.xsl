<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
  xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns="http://www.tei-c.org/ns/1.0"
  xmlns:marc="http://www.loc.gov/MARC21/slim" exclude-result-prefixes="xs xd marc tei" version="2.0">
  <xsl:import href="openn_templates.xsl"/>
  <xd:doc scope="stylesheet">
    <xd:desc>
      <xd:p><xd:b>Created:</xd:b> 2018</xd:p>
      <xd:p><xd:b>Author:</xd:b> emeryr</xd:p>
    
    </xd:desc>
  </xd:doc>
  <xsl:output indent="yes"/>
  <xsl:param name="holdings_id"/>
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
    <xsl:variable name="holding" select="//marc:holding_id[text() = $holdings_id]/parent::node()"/>
    <xsl:value-of select="$holding/marc:location"/>
    <xsl:text> </xsl:text>
    <xsl:value-of select="$holding/marc:call_number"/>
    <!--<xsl:call-template name="clean-up-text">
      <xsl:with-param name="some-text" select="//marc:holding[1]/marc:call_number"/>
    </xsl:call-template>-->
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
          @done
      </xsl:comment>
      <xsl:comment>
        DE: I haven't looked at the title@level attribute. Need to make sure this being used consistently.
        A: Remove @level
        @done
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
            <xsl:comment>
              TODO:
              Ugh respStmt is all wrong. figure out what's going on here and fix. Which tags do we use?
            </xsl:comment>
            <xsl:for-each select="//marc:datafield[@tag=700]">
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
                  <xsl:call-template name="pubPlace">
                    <xsl:with-param name="marc752d" select="//marc:datafield[@tag=752]/marc:subfield[@code='d']"/>
                    <xsl:with-param name="marc752a" select="//marc:datafield[@tag=752]/marc:subfield[@code='a']"/>
                    <xsl:with-param name="marc260a" select="//marc:datafield[@tag=260]/marc:subfield[@code='a']"/>
                  </xsl:call-template>
                  <xsl:for-each select="//marc:datafield[@tag=260]/marc:subfield[@code='b']">
                    <publisher>
                      <xsl:call-template name="chopPunctuation">
                        <xsl:with-param name="chopString">
                          <xsl:value-of select="."/>
                        </xsl:with-param>
                      </xsl:call-template>
                    </publisher>
                  </xsl:for-each>

                  <!--
                    @done
                    
                    DE: Is this dangerous? Can it be a range? An LC partial date? Circa date?
                    They won't validate as date attributes. (DE)
                    A: pull ctrl field 008 positions 7-10; figure out if number.
                   
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
                    <date>
                      <xsl:call-template name="dateAttributes">
                        <xsl:with-param name="marc008" select="//marc:controlfield[@tag='008']"/>
                      </xsl:call-template>
                      <xsl:call-template name="dateString">
                        <xsl:with-param name="marc260c" select="//marc:controlfield[@tag='260']/marc:subfield[@code='c']"/>
                        <xsl:with-param name="marc008" select="//marc:controlfield[@tag='008']"/>
                      </xsl:call-template>
                    </date>
                </imprint>
                <!-- 
                  @done
                  DE: I'm skipping subfield 'b' here. It should be combined with 'a' if it exists.
                  A: Join $a $c; remove trailing :; and join with '; '
                -->
                <xsl:variable name="marc300a" select="//marc:datafield[@tag=300]/marc:subfield[@code='a']"/>
                <xsl:variable name="marc300c" select="//marc:datafield[@tag=300]/marc:subfield[@code='c']"/>
                <xsl:if test="$marc300a or $marc300c">
                  <extent>
                  <xsl:choose>
                    <xsl:when test="$marc300c">
                      <xsl:if test="$marc300a">
                        <xsl:value-of select="$marc300a"/>
                        <xsl:text>; </xsl:text>
                      </xsl:if>
                      <xsl:value-of select="$marc300c"/>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:value-of select="$marc300a"/>
                    </xsl:otherwise>
                  </xsl:choose>
                  </extent>
                </xsl:if>
              </monogr>
              <!--
                @done
                TODO: Need to examine our marc and figure out which to use. TEI
                recommends 4xx and 8xx be used here, without providing much detail. Need to
                investigate subfield. In sample marc, we use 440, 490, 810, 830, 856; the last
                being the facsimile.
                A: 440$a | 490$a | 830$a in that order, with $v if it is there
              -->
              <xsl:choose>
                <xsl:when test="//marc:datafield[@tag=440]/marc:subfield[@code='a']">
                  <xsl:call-template name="seriesTitle">
                    <xsl:with-param name="seriesElement" select="//marc:datafield[@tag=440]"/>
                  </xsl:call-template>
                </xsl:when>
                <xsl:when test="//marc:datafield[@tag=490]/marc:subfield[@code='a']">
                  <xsl:call-template name="seriesTitle">
                    <xsl:with-param name="seriesElement" select="//marc:datafield[@tag=490]"/>
                  </xsl:call-template>
                </xsl:when>
                <xsl:when test="//marc:datafield[@tag=830]/marc:subfield[@code='a']">
                  <xsl:call-template name="seriesTitle">
                    <xsl:with-param name="seriesElement" select="//marc:datafield[@tag=830]"/>
                  </xsl:call-template>
                </xsl:when>
              </xsl:choose>
              <xsl:if test="//marc:datafield[@tag='500']">
                <xsl:for-each select="//marc:datafield[@tag='500']">
                  <note>
                    <xsl:value-of select="normalize-space(marc:subfield[@code='a'])"/>
                  </note>
                </xsl:for-each>
              </xsl:if>
                <!--              
                The way call number is pulled now is bad. The XSL pulls the first
                holding from the list of holdings and gets that call number. How do
                we distinguish which call number? Require the holdings number as input?
                A: Require holding ID and translate and prepend subcollection `scforr`, `scsing`.
                @done
                -->              
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
          <xsl:if test="//marc:datafield[@tag='041']/marc:subfield[@code='a']">
            <langUsage>
            <xsl:for-each select="//marc:datafield[@tag='041']/marc:subfield[@code='a']">
                <language>
                  <xsl:attribute name="ident" select="."/>
                </language>
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
</xsl:stylesheet>