import sys

# Don't run this stuff
sys.exit(1)

# UPDATE TEI from file system
from openn.xml.openn_tei import OPennTEI
doc = Document.objects.get(pk=6853)
tei = OPennTEI(open('/mnt/scratch02/openn/site/Data/0032/ms_or_044/data/ms_or_044_TEI.xml').read())
doc.tei_xml = tei.to_string()
doc.save()