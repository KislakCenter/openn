# -*- coding: utf-8 -*-
from django.db import models
from ordered_model.models import OrderedModel
from django.conf import settings
import httplib
import os
import re
import hashlib
import pytz
from datetime import datetime

class Repository(models.Model):
    """Repository is a collection to which a document belongs.

    """
    tag           = models.CharField(max_length = 50, null = False, default = None, blank = False, unique = True)
    metadata_type = models.CharField(max_length = 50, null = False, default = None, blank = False,
        choices = (('tei','TEI'), ('ead', 'EAD'), ('custom', 'Custom'), ('walters-tei', 'Walters TEI')))
    name          = models.CharField(max_length = 255, null = True, default = None, blank = True, unique = True)
    live          = models.BooleanField(default = False)
    blurb         = models.TextField(null = True, default = None, blank = True)
    include_file  = models.CharField(max_length = 255, null = True, default = None, blank = False, unique = True)
    no_document   = models.BooleanField(default = False)

    class Meta:
        ordering = ('tag',)

    def long_id(self):
        return "%04d" % (self.id,)

    def folder(self):
        self.long_id()

    def toc_file(self):
        return "%s.html" % (self.long_id(),)

    def csv_toc_file(self):
        return '%s_contents.csv' % (self.long_id())

    def web_dir(self):
        return "Data/%s" % (self.long_id(),)

    def html_dir(self):
        return "Data/%s/html" % (self.long_id(),)

    def __str__(self):
        return ("Repository: id={id:d}, tag={tag}").format(
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
    repository                = models.ForeignKey(Repository, default = None)

    @property
    def browse_basename(self):
        return '{0}.html'.format(self.base_dir)

    @property
    def browse_path(self):
        return '{0}/{1}'.format(self.repository.html_dir(), self.browse_basename)

    @property
    def package_dir(self):
        return '{0}/{1}'.format(self.repository.web_dir(), self.base_dir)

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
    def repository_tag(self):
        if self.repository is not None:
            return self.repository.tag
        else:
            return 'UNKNOWN'

    @property
    def repository_id_long(self):
        if self.repository is None:
            return None

        return self.repository.long_id()

    @property
    def metadata_type(self):
        if self.repository is None:
            return None

        return self.repository.metadata_type

    def image_license_args(self):
         # image_copyright_holder
         # image_copyright_year
         # image_rights_more_info
         return {'holder': self.image_copyright_holder,
                 'year': self.image_copyright_year,
                 'more_information': self.image_rights_more_info,
                 'title': self.title}

    def metadata_license_args(self):
         # metadata_copyright_holder
         # metadata_copyright_year
         # metadata_rights_more_info
         return {'holder': self.metadata_copyright_holder,
                 'year': self.metadata_copyright_year,
                 'more_information': self.metadata_rights_more_info,
                 'title': self.title}

    def is_live(self):
        c = httplib.HTTPConnection(settings.OPENN_HOST)
        path = '/%s' % (self.manifest_path, )
        c.request('HEAD', path)
        return c.getresponse().status < 400

    # Choosing collection, base_dir as the uniqueness columns
    # While the collection + call_number should be unique, the collection +
    # base_dir must be unique to prevent filesystem collisions on the host.
    class Meta:
        ordering        = ['repository', 'base_dir', 'call_number' ]
        unique_together = ('repository', 'base_dir')


    def __str__(self):
        return ("Document: id={id:d}, call_number={call_number}" +
                ", collection={collection}, base_dir={base_dir}" +
                ", is_online={is_online}" +
                ", image_licence={image_licence}" +
                ", image_copyright_year={image_copyright_year}" +
                ", image_rights_more_info={image_rights_more_info}" +
                ", metadata_licence={metadata_licence}" +
                ", metadata_copyright_holder={metadata_copyright_holder}" +
                ", metadata_copyright_year={metadata_copyright_year}" +
                ", metadata_rights_more_info={metadata_rights_more_info}" +
                ", created={created}, updated={updated}").format(
                        id=self.id,
                        call_number=self.call_number,
                        collection=self.collection,
                        base_dir=self.base_dir,
                        is_online=self.is_online,
                        image_licence=self.image_licence,
                        image_copyright_holder=self.image_copyright_holder,
                        image_copyright_year=self.image_copyright_year,
                        image_rights_more_info=self.image_rights_more_info,
                        metadata_licence=self.metadata_licence,
                        metadata_copyright_holder=self.metadata_copyright_holder,
                        metadata_copyright_year=self.metadata_copyright_year,
                        metadata_rights_more_info=self.metadata_rights_more_info,
                        created=self.created,
                        updated=self.updated)

class DocumentImageManager(models.Manager):
    def get_query_set(self):
        return super(DocumentImageManager, self).get_query_set().filter(image_type=u'document')

class ExtraImageManager(models.Manager):
    def get_query_set(self):
        return super(ExtraImageManager, self).get_query_set().filter(image_type=u'extra')


class CuratedCollection(models.Model):
    """An OPenn CuratedCollection is a secondary grouping of Documents from
        multiple Repositories. CuratedCollections group Documents from one or
        more collections.

    """
    tag          = models.CharField(max_length = 50,  null = False, default = None, blank = False, unique = True)
    name         = models.CharField(max_length = 255, null = False, default = None, blank = False, unique = True)
    blurb        = models.TextField(null = True, default = None, blank = True)
    csv_only     = models.BooleanField(default = True)
    include_file = models.CharField(max_length = 255, null = True, default = None, blank = False, unique = True)
    live         = models.BooleanField(default = False)
    created      = models.DateTimeField(auto_now_add = True)
    updated      = models.DateTimeField(auto_now = True)
    documents    = models.ManyToManyField(Document, through='CuratedMembership')

    def short_blurb(self):
        if self.blurb is not None and len(self.blurb) > 25:
            return self.blurb[:25] + '...'
        else:
            return self.blurb

    def csv_toc_file(self):
        return '%s_contents.csv' % (self.tag.lower(),)

    def toc_file(self):
        return '%s_contents.html' % (self.tag.lower(),)

    def has_documents(self):
        return self.documents.count() > 0

    def has_documents_on_line(self):
        if not self.has_documents():
            return False
        return self.documents.filter(is_online=True).count() > 0

    def last_updated(self):

        """ Return the data this curated_collection was modified or a document
        was added or removed from it.

        This method relies on
        `openn.curated.membership_manager.MembershipManager` to save the object
        whenever documents are added or removed.

        """
        return self.updated

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return ('CuratedCollection: id={id:d}' +
                ', tag="{tag}"' +
                ', name="{name}"' +
                ', blurb="{blurb}"' +
                ", csv_only={csv_only}" +
                ', include_file="{include_file}"' +
                ", live={live}" +
                ', created="{created}"' +
                ', updated="{updated}"').format(
                        id=self.id,
                        tag=self.tag,
                        name=self.name,
                        blurb=self.short_blurb(),
                        csv_only=self.csv_only,
                        include_file=self.include_file,
                        live=self.live,
                        created=self.created,
                        updated=self.updated)

class CuratedMembership(models.Model):
    """ A CuratedMembership links a Document to a CuratedCollection.
    """
    document           = models.ForeignKey(Document, on_delete=models.CASCADE)
    curated_collection = models.ForeignKey(CuratedCollection,  on_delete=models.CASCADE)
    created            = models.DateTimeField(auto_now_add = True)
    updated            = models.DateTimeField(auto_now = True)

    class Meta:
        unique_together = ('document', 'curated_collection',)

    def __str__(self):
        return ('CuratedMembership: id={id:d}' +
                ', curated_collection_id={curated_collection_id:d}' +
                ', document_id={document_id:d}').format(
                        id=self.id,
                        curated_collection_id=self.curated_collection_id,
                        document_id=self.document_id)

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

    def image_license_args(self):
        hmb_dict = self.document.image_license_args()
        hmb_dict.update({'title': self.full_name()})

        return hmb_dict

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
        repository = self.image.document.repository
        return "/Data/%s/%s/%s" % (
            repository.long_id(), self.image.document.base_dir, self.path)

    def basename(self):
        return os.path.splitext(os.path.basename(self.path))[0]

class TemplateHash(models.Model):
    """
    Model to hold hashes.
    """
    sha256 = models.CharField(max_length=64, null=True, default=None, blank=True)

    @staticmethod
    def find_or_create(sha256_hash):
        """ For outfile either find the SiteFile object or create in the database.
        """
        try:
            return TemplateHash.objects.get(sha256=sha256_hash)
        except TemplateHash.DoesNotExist:
            thash = TemplateHash(sha256=sha256_hash)
            thash.save()
            return thash

class TemplateFile(models.Model):
    """
    Model to hold template names.
    """
    name = models.CharField(max_length=255, null=False, default=None, blank=False,
                                     unique=True)

    @staticmethod
    def find_or_create(template_name):
        """ For outfile either find the SiteFile object or create in the database.
        """
        try:
            return TemplateFile.objects.get(name=template_name)
        except TemplateFile.DoesNotExist:
            templ = TemplateFile(name=template_name)
            templ.save()
            return templ

    def template_path(self):
        "Construct and returnt the path for this template"
        for dirname in settings.TEMPLATE_DIRS:
            tpath = os.path.join(settings.SITE_ROOT, dirname, self.name)
            if os.path.exists(tpath):
                return tpath

class SiteFile(models.Model):
    """
    Model to hold details about a given website file. It has the following fields.
    """

    # The name and relative path of the output file; required, unique
    output_file = models.CharField(max_length=255, null=False, default=None, blank=False,
                                   unique=True)
    # If an HTML page, the template name; optional
    template = models.ForeignKey(TemplateFile, null=True, default=None, blank=True,
                                        related_name='html_pages')
    # If an HTML page, the hash of the template; optional. Used to check
    # template changes.
    template_hash = models.ForeignKey(TemplateHash, null=True, default=None, blank=True,
                                        related_name='html_pages')
    # The date that this file was last generated.
    last_generated = models.DateTimeField(null=True, default=None, blank=True)

    # If an HTML page with include file, the include file name; optional
    include_file = models.ForeignKey(TemplateFile, null=True, default=None, blank=True,
                                            related_name='include_pages')
    # If SiteFile has an include_file, the hash of the file; optional. Used to check
    # include_file changes.
    include_file_hash = models.ForeignKey(TemplateHash, null=True, default=None, blank=True,
                                            related_name='include_pages')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def update_last_generated(self, dtime=None):
        if dtime is None:
            self.last_generated = datetime.now(pytz.utc)
        else:
            self.last_generated = dtime
        self.save()

    @staticmethod
    def find_or_create(outfile, **kwargs):
        """ For outfile either find the SiteFile object or create in the database.
        """
        try:
            sfile = SiteFile.objects.get(output_file=outfile)
        except SiteFile.DoesNotExist:
            sfile = SiteFile(output_file=outfile, **kwargs)
            sfile.save()

        return sfile

    def set_template(self, template_name):
        """ Set the template using the template_name
        """
        if self.template_name == template_name:
            return

        self.template = TemplateFile.find_or_create(template_name)
        self.save()

    def template_path(self):
        "Return the path to the template if template present; otherwise, None."
        return None if self.template is None else self.template.template_path()

    def template_name(self):
        "Return the name of the template if template present; otherwise, None."
        return None if self.template is None else self.template.name

    def set_template_hash(self, sha256):
        "Set the template_sha256 to the give hash."
        if self.template_hash is not None and self.template_hash.sha256 == sha256:
            return

        self.template_hash = TemplateHash.find_or_create(sha256)
        self.save()

    def template_sha256_on_disk(self):
        "Get the template sha256 on disk."
        return self._get_hash_on_disk('template_path')

    def template_has_changed(self):
        "Return true if the on disk hash is different from the stored hash."
        if self.template_hash is None:
            return True

        return self.template_sha256_on_disk() != self.template_hash.sha256

    def update_template_sha256(self):
        "Update the stored hash to the value on disk."
        self.set_template_hash(self.template_sha256_on_disk())

    def set_include_file(self, include_file_name):
        "Set the include_file using the include_file_name "
        if self.include_file_name == include_file_name:
            return

        self.include_file = TemplateFile.find_or_create(include_file_name)
        self.save()

    def include_file_path(self):
        "Return the path to the include_file if include_file present; otherwise, None."
        return None if self.include_file is None else self.include_file.template_path()

    def include_file_name(self):
        "Return the name of the include_file if include_file present; otherwise, None."
        return None if self.include_file is None else self.include_file.name

    def set_include_file_hash(self, sha256):
        "Set the include_file_sha256 to the given hash."
        if self.include_file_hash is not None and self.include_file_hash.sha256 == sha256:
            return

        self.include_file_hash = TemplateHash.find_or_create(sha256)
        self.save()

    def include_file_sha256_on_disk(self):
        "Get the include_file sha256 on disk."
        return self._get_hash_on_disk('include_file_path')

    def include_file_has_changed(self):
        "Return true if the on disk hash is different from the stored hash."
        if self.include_file_hash is None:
            return True

        return self.include_file_sha256_on_disk() != self.include_file_hash.sha256

    def update_include_file_sha256(self):
        "Update the store hash to the value on disk."
        self.set_include_file_hash(self.include_file_sha256_on_disk())

    def _get_hash_on_disk(self, path_attr):
        sha256 = hashlib.sha256()
        file_path = getattr(self, path_attr)()
        sha256.update(open(file_path).read())
        return sha256.hexdigest()

    def __str__(self):
        return ('SiteFile: id={id:d}'
                ', output_file="{output_file}"'
                ', template="{template}"'
                ', template_sha256="{template_sha256}"'
                ', last_generated="{last_generated}"'
                ', include_file="{include_file}"'
                ', include_file_sha256="{include_file_sha256}"'
                ', created="{created}"'
                ', updated="{updated}"').format(
                    id=self.id,
                    output_file=self.output_file,
                    template=self.template_name(),
                    template_sha256=self.template_hash,
                    last_generated=self.last_generated,
                    include_file=self.include_file_name(),
                    include_file_sha256=self.include_file_hash,
                    created=self.created,
                    updated=self.updated)
