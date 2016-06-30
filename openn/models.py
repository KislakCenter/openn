# -*- coding: utf-8 -*-
from django.db import models
from ordered_model.models import OrderedModel
from django.conf import settings
import httplib
import os
import re

class OPennCollection(models.Model):
    """OPennCollection is a collection to which a document belongs.

    """
    tag = models.CharField(max_length = 50, null = False, default = None, blank = False, unique = True)
    metadata_type = models.CharField(
        max_length = 50, null = False, default = None, blank = False,
        choices = (('tei','TEI'), ('ead', 'EAD'), ('custom', 'Custom'), ('walters-tei', 'Walters TEI')))

    class Meta:
        ordering = ('tag',)

    def long_id(self):
        return "%04d" % (self.id,)

    def folder(self):
        self.long_id()

    def toc_file(self):
        return "%s.html" % (self.long_id(),)

    def web_dir(self):
        return "Data/%s" % (self.long_id(),)

    def html_dir(self):
        return "Data/%s/html" % (self.long_id(),)

    def __str__(self):
        return ("OPennCollection: id={id:d}, tag={tag}").format(
                        id=self.id, tag=self.tag)

    def __repr__(self):
        return self.__str__()

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
    call_number               = models.CharField(max_length = 255, null = True, default = None, blank = True)
    collection                = models.CharField(max_length = 30, null = True, default = None, blank = True)
    base_dir                  = models.CharField(max_length = 30, null = False, default = None, blank = False)
    image_licence             = models.CharField(max_length = 10, null = True, default = 'PD', blank = True)
    metadata_licence          = models.CharField(max_length = 10, null = True, default = 'CC-BY', blank = True)
    is_online                 = models.BooleanField(default = False)
    title                     = models.TextField(null = True, default = None, blank = True)
    created                   = models.DateTimeField(auto_now_add = True)
    updated                   = models.DateTimeField(auto_now = True)
    tei_xml                   = models.TextField(null = True, default = None, blank = True)
    image_copyright_holder    = models.CharField(max_length = 255, null = True, default = None, blank = True)
    image_copyright_year      = models.IntegerField(null = True, default = None, blank = True)
    image_rights_more_info    = models.TextField(null = True, default = None, blank = True)
    metadata_copyright_holder = models.CharField(max_length = 255, null = True, default = None, blank = True)
    metadata_copyright_year   = models.IntegerField(null = True, default = None, blank = True)
    metadata_rights_more_info = models.TextField(null = True, default = None, blank = True)
    openn_collection          = models.ForeignKey(OPennCollection, default = None)

    @property
    def browse_basename(self):
        return '{0}.html'.format(self.base_dir)

    @property
    def browse_path(self):
        return '{0}/{1}'.format(self.openn_collection.html_dir(), self.browse_basename)

    @property
    def package_dir(self):
        return '{0}/{1}'.format(self.openn_collection.web_dir(), self.base_dir)

    @property
    def data_dir(self):
        return '{0}/data'.format(self.package_dir)

    @property
    def tei_basename(self):
        return '%s_TEI.xml' % (self.base_dir, )

    @property
    def tei_path(self):
        return '{0}/{1}'.format(self.data_dir, self.tei_basename)

    @property
    def manifest_path(self):
        return '%s/manifest-sha1.txt' % (self.package_dir, )

    @property
    def is_prepped(self):
        return (self.prepstatus and self.prepstatus.succeeded) or False

    @property
    def collection_tag(self):
        if self.openn_collection is not None:
            return self.openn_collection.tag
        else:
            return 'UNKNOWN'


    def is_live(self):
        c = httplib.HTTPConnection(settings.OPENN_HOST)
        path = '/%s' % (self.manifest_path, )
        c.request('HEAD', path)
        return c.getresponse().status < 400

    # Choosing collection, base_dir as the uniqueness columns
    # While the collection + call_number should be unique, the collection +
    # base_dir must be unique to prevent filesystem collisions on the host.
    class Meta:
        ordering        = ['openn_collection', 'base_dir', 'call_number' ]
        unique_together = ('openn_collection', 'base_dir')


    def __str__(self):
        return ("Document: id={id:d}, call_number={call_number}" +
                ", collection={collection}, base_dir={base_dir}" +
                ", is_online={is_online}" +
                ", created={created}, updated={updated}").format(
                        id=self.id,
                        call_number=self.call_number,
                        collection=self.collection,
                        base_dir=self.base_dir,
                        is_online=self.is_online,
                        created=self.created,
                        updated=self.updated)

class DocumentImageManager(models.Manager):
    def get_query_set(self):
        return super(DocumentImageManager, self).get_query_set().filter(image_type=u'document')

class ExtraImageManager(models.Manager):
    def get_query_set(self):
        return super(ExtraImageManager, self).get_query_set().filter(image_type=u'extra')

class PrepStatus(models.Model):
    document  = models.OneToOneField(Document, primary_key = True)
    started   = models.DateTimeField(auto_now_add = True)
    updated   = models.DateTimeField(auto_now = True)
    finished  = models.DateTimeField(null = True, default = None, blank = True)
    succeeded = models.BooleanField(default = False)
    error     = models.TextField(null = True, default = None, blank = True)

class Version(OrderedModel):
    document              = models.ForeignKey(Document, default = None)
    major_version         = models.IntegerField(null = False, default = 1)
    minor_version         = models.IntegerField(null = False, default = 0)
    patch_version         = models.IntegerField(null = False, default = 0)
    description           = models.TextField(null = False, default = None, blank = False)
    created               = models.DateTimeField(auto_now_add = True)
    updated               = models.DateTimeField(auto_now = True)
    order_with_respect_to = 'document'

    class Meta:
        ordering        = [ 'document', 'major_version', 'minor_version', 'patch_version' ]
        unique_together = [ 'document', 'major_version', 'minor_version', 'patch_version' ]

    @property
    def text(self):
        """Return the composed version of the document as a string; for
        example. '1.0.0'

        """
        return '.'.join([ str(i) for i in self.version ])

    @property
    def version(self):
        """Return the version as tuple of

            - (major_version, minor_version, patch_version)

        For example, ``(1,0,0)``.
        """
        return ( self.major_version, self.minor_version, self.patch_version )

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
    created               = models.DateTimeField(auto_now_add = True)
    updated               = models.DateTimeField(auto_now = True)

    BRACKET_RE = re.compile('^\[|\]$')

    def display_label(self):
        s = Image.BRACKET_RE.sub('', self.label)
        if re.search('\d+[rv]', s):
            return "fol. %s" % s
        else:
            return s

    def __unicode__(self):
        return u"label: %s, filename: %s" % (self.label, self.filename)

    def full_name(self):
        return u'%s %s, %s' % (
            self.document.call_number, self.document.title, self.label)

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
    created    = models.DateTimeField(auto_now_add = True)
    updated    = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = [ 'deriv_type' ]

    def url(self):
        collection = self.image.document.openn_collection
        return "/Data/%s/%s/%s" % (
            collection.long_id(), self.image.document.base_dir, self.path)

    def basename(self):
        return os.path.splitext(os.path.basename(self.path))[0]
