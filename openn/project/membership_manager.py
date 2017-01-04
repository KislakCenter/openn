# -*- coding: utf-8 -*-
import logging
import re

from django.db.utils import IntegrityError

from openn.models import *
from openn.project.duplicate_membership import DuplicateMembership

class MembershipManager(object):
    """Class to Manage membership of Documents in Projects"""

    logger = logging.getLogger(__name__)

    def add_document(self, proj_tag, doc_tag, coll_tag=None):
        """ Add specified document to Project with tag 'proj_tag'.

        Parameters
        ----------

        proj_tag : string
            A string equal to the project's tag; e.g., 'bibliophilly';
            case sensitive

        doc_tag  : string
            Either the integer Document identifier or 'base_dir' string; case
            sensitive

        coll_tag : string
            The string tag for the OPennCollection; required if 'base_dir'
            is provided and ambigous; case sensitive

        'add_document' will attempt to add the doc based on the specification
        of doc_tag' plus a possible 'coll_tag'.

        If 'doc_tag' is the Document identifier, 'coll_tag' is not required.

        If 'doc_tag' is the Document 'base_dir' and 'based_dir' occurs in more
        than one collection, the 'coll_tag' is required.

        Exceptions
        ----------

        In the event of a bad or ambigous specification the appropriate Django
        ORM exception is raised: models.DoesNotExist or
        models.MultipleObjectsReturned.

        If the document already belongs to the project,
        openn.project.duplicate_membership.DuplicateMembership is raised.

        """
        project  = Project.objects.get(tag=proj_tag.lower())
        document = self.find_document(doc_tag=doc_tag, coll_tag=coll_tag)
        try:
            membership = ProjectMembership.objects.create(
                project=project, document=document)
        except IntegrityError as ie:
            if re.search('Duplicate entry', str(ie)):
                msg = "Membership already exists for document %d/%s and project %s" % (
                    document.pk,
                    document.base_dir,
                    project.tag, )
                raise DuplicateMembership(msg)
            else:
                raise

    def remove_document(self, proj_tag, doc_tag, coll_tag=None):
        project    = Project.objects.get(tag=proj_tag.lower())
        document   = self.find_document(doc_tag=doc_tag, coll_tag=coll_tag)

        membership = ProjectMembership.objects.get(project_id=project.pk, document_id=document.pk)
        membership.delete()

    def find_document(self, doc_tag, coll_tag=None):
        if self.is_integer(doc_tag):
            return Document.objects.get(pk=int(doc_tag))

        if coll_tag is None:
            return self.doc_by_base_dir(base_dir=doc_tag)

        return self.doc_by_base_dir_and_coll(base_dir=doc_tag, coll_tag=coll_tag)

    def doc_by_base_dir(self, base_dir):
        return Document.objects.get(base_dir=base_dir)

    def doc_by_base_dir_and_coll(self, base_dir, coll_tag):
        coll     = OPennCollection.objects.get(tag=coll_tag.lower())
        return Document.objects.get(openn_collection_id=coll.pk, base_dir=base_dir)

    def is_integer(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False