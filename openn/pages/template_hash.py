from django.conf import settings

import os
import hashlib

class TemplateHash(object):
    """ Class to check and manipulate the hash of template_attr for page_obj.
    The page_obj may be SiteFile, Repository, or CuratedCollection model
    object.
    """

    def __init__(self, page_obj, template_attr='template'):
        self.page_object = page_obj
        self.template_attr = template_attr

    def current_template_sha256(self):
        """ Return the hash of the template file on disk.
        """
        sha256 = hashlib.sha256()
        sha256.update(open(self.template_path()).read())
        return sha256.hexdigest()

    def template_has_changed(self):
        """ Return True if the template file on disk has a different hash.
        """
        return self.page_object.template_sha256 != self.current_template_sha256()

    def update_template_sha256(self):
        """ Update the template_sha256 to match the file system
        """
        self.page_object.template_sha256 = self.current_template_sha256()
        self.page_object.save()

    def template_path(self):
        """ Return the full path to the the template file on disk.
        """
        if self.template_name() is None:
            return None

        return os.path.join(settings.SITE_ROOT, 'templates', self.template_name())

    def template_name(self):
        """ Return the name of the the template from the page_object
        """
        return getattr(self.page_object, self.template_attr)
