import sys

# Don't run this stuff
sys.exit(1)

# UPDATE TEI from file system
from openn.xml.openn_tei import OPennTEI
doc = Document.objects.get(pk=6853)
tei = OPennTEI(open('/mnt/scratch02/openn/site/Data/0032/ms_or_044/data/ms_or_044_TEI.xml').read())
doc.tei_xml = tei.to_string()
doc.save()

names = (('0007', 'lehigh_002', 'lehigh_codex_002'),
    ('0007', 'lehigh_003', 'lehigh_codex_003'),
    ('0007', 'lehigh_006', 'lehigh_codex_006'),
    ('0007', 'lehigh_007', 'lehigh_codex_007'),
    ('0007', 'Antiphon_25', 'lehigh_codex_025'),
    ('0007', 'BookofHoursoftheRomanuse_18', 'lehigh_codex_018'),
    ('0003', 'BMCMS2', 'BMC_MS02'),
    ('0003', 'BMCMS5', 'BMC_MS05'),
    ('0003', 'BMCMS31', 'BMC_MS31'),
    ('0003', 'BMCMS32', 'BMC_MS32'),
    ('0003', 'BMCMS33', 'BMC_MS33'),
    ('0003', 'BMCMS34', 'BMC_MS34'),
    ('0003', 'BMC_MS8', 'BMC_MS08'),
    ('0003', 'BMC_MS9', 'BMC_MS09'),
    ('0003', 'BMC_MS7', 'BMC_MS07'),
    ('0003', 'BMC_MS4', 'BMC_MS04'),
    ('0003', 'BMC_MS6', 'BMC_MS06'),
    ('0003', 'BMC_MS3', 'BMC_MS03'),
    ('0012', 'ms2_2224q', 'lcp_ms02'),
    ('0012', 'ms3_1141f', 'lcp_ms03'),
    ('0012', 'lcp_ms024', 'lcp_ms24'),
    ('0012', 'lcp_ms1', 'lcp_ms01'),
    ('0012', 'lcp_ms4', 'lcp_ms04'),
    ('0012', 'lcp_ms5', 'lcp_ms05'),
    ('0012', 'lcp_ms6', 'lcp_ms06'),
    ('0012', 'lcp_ms7', 'lcp_ms07'),
    ('0012', 'lcp_ms8', 'lcp_ms08'),
    ('0012', 'lcp_ms9', 'lcp_ms09'))

for (repo, old, new) in names:
    doc = Document.objects.get(base_dir=old)
    doc.base_dir = new
    doc.is_online = False
    doc.save()
    doc = Document.objects.get(base_dir=new)
    print "%-30s %-20s %r" % (old, new, doc)