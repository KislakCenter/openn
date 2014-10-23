# -*- coding: utf-8 -*-
from django.db import models
from ordered_model.models import OrderedModel
from django.conf import settings
import re

"""
Document corresponds to a set of OPenn images and metadata.

A Document records:

    - `call_number`: the shelfmark or other identfying ID; for example,
        'Ms Codex 1234'
    - `collection`: the name of the collection; this value will
        be used as the directory name of the images; for example, 'LJS',
        'PennMedRen'
    - `base_dir`: the base directory of the document folder, for example,
        'mscodex1234' or 'ljs223'
    - `is_online`: whether the document's images and other data are online
    - `tei_file_name`: the name of the document's TEI description
    - `created`: the date-time the record was created
    - `updated`: the date-time the record was last updated
"""
class Document(models.Model):
    call_number   = models.CharField(max_length = 255, null = False, default = None, blank = False)
    collection    = models.CharField(max_length = 30, null = False, default = None, blank = False)
    base_dir      = models.CharField(max_length = 30, null = False, default = None, blank = False)
    is_online     = models.BooleanField(default = False)
    tei_file_name = models.CharField(max_length = 40, null = True, default = None, blank = True)
    title         = models.TextField(null = False, default = None, blank = False)
    created       = models.DateTimeField(auto_now_add = True)
    updated       = models.DateTimeField(auto_now = True)
    tei_xml       = models.TextField(null = True, default = None, blank = True)

    @property
    def collection_config(self):
        return settings.COLLECTIONS[self.collection]

    @property
    def html_dir(self):
        return self.collection_config['html_dir']

    @property
    def web_dir(self):
        return self.collection_config['web_dir']

    @property
    def browse_basename(self):
        return '{0}.html'.format(self.base_dir)

    @property
    def browse_path(self):
        return '{0}/{1}'.format(self.html_dir, self.browse_basename)

    @property
    def package_dir(self):
        return '{0}/{1}'.format(self.web_dir, self.base_dir)

    @property
    def data_dir(self):
        return '{0}/data'.format(self.package_dir)

    @property
    def tei_basename(self):
        return '%04d_TEI.xml' % (self.id, )

    @property
    def tei_path(self):
        return '{0}/{1}'.format(self.data_dir, self.tei_basename)

    # Choosing collection, base_dir as the uniqueness columns
    # While the collection + call_number should be unique, the collection +
    # base_dir must be unique to prevent filesystem collisions on the host.
    class Meta:
        ordering        = ['collection', 'base_dir', 'call_number' ]
        unique_together = ('collection', 'base_dir')


    def __str__(self):
        return ("Document: id={id:d}, call_number={call_number}" +
                ", collection={collection}, base_dir={base_dir}" +
                ", is_online={is_online}, tei_file_name={tei_file_name}" +
                ", created={created}, updated={updated}").format(
                        id=self.id,
                        call_number=self.call_number,
                        collection=self.collection,
                        base_dir=self.base_dir,
                        is_online=self.is_online,
                        tei_file_name=self.tei_file_name,
                        created=self.created,
                        updated=self.updated)

class DocumentImageManager(models.Manager):
    def get_query_set(self):
        return super(DocumentImageManager, self).get_query_set().filter(image_type='d')

class ExtraImageManager(models.Manager):
    def get_query_set(self):
        return super(ExtraImageManager, self).get_query_set().filter(image_type='x')

class Image(OrderedModel):
    document              = models.ForeignKey(Document, default = None)
    label                 = models.CharField(max_length = 255, null = False, default = None, blank = False)
    filename              = models.CharField(max_length = 255, null = False, default = None, blank = False)
    image_type            = models.CharField(max_length = 20, choices=(('document', 'Document'), ('extra', 'Extra')))
    order_with_respect_to = 'document'
    objects               = models.Manager()
    images                = models.Manager()
    document_images       = DocumentImageManager()
    extra_images          = ExtraImageManager()

    BRACKET_RE = re.compile('^\[|\]$')

    def display_label(self):
        s = Image.BRACKET_RE.sub('', self.label)
        if re.search('\d+[rv]', s):
            return "fol. %s" % s
        else:
            return s

    def __unicode__(self):
        return u"label: %s, filename: %s" % (self.label, self.filename)

    def deriv(self, type_name):
        derivs = self.derivative_set.filter(deriv_type=type_name)
        return (len(derivs) > 0 and derivs[0]) or None

    def thumb(self):
        return self.deriv('thumb')

    def web(self):
        return self.deriv('web')

    def master(self):
        return self.deriv('master')

    class Meta(OrderedModel.Meta):
        pass

class Derivative(models.Model):
    image      = models.ForeignKey(Image, default = None)
    deriv_type = models.CharField(max_length  = 20, null  = False, default = None, blank = False)
    path       = models.CharField(max_length  = 255, null = False, default = None, blank = False)
    bytes      = models.IntegerField()
    width      = models.IntegerField()
    height     = models.IntegerField()

    class Meta:
        ordering = [ 'deriv_type' ]

    def url(self):
        collection = settings.COLLECTIONS[self.image.document.collection]
        return "/%s/%s/%s" % (collection['web_dir'], self.image.document.base_dir, self.path)
