# -*- coding: utf-8 -*-
import logging
import re

from django.db.utils import IntegrityError

from openn.models import *
from openn.curated.duplicate_membership import DuplicateMembership

class MembershipManager(object):
    """Class to Manage membership of Documents in CuratedCollections"""

    logger = logging.getLogger(__name__)

    def add_document(self, curated_tag, doc_tag, repo_tag=None):
        """ Add specified document to CuratedCollection with tag 'curated_tag'.

        Parameters
        ----------

        curated_tag : string
            A string equal to the curated collection's tag; e.g.,
            'bibliophilly'; case sensitive

        doc_tag  : string
            Either the integer Document identifier or 'base_dir' string; case
            sensitive

        repo_tag : string
            The string tag for the Repository; required if 'base_dir'
            is provided and ambigous; case sensitive

        'add_document' will attempt to add the doc based on the specification
        of doc_tag' plus a possible 'repo_tag'.

        If 'doc_tag' is the Document identifier, 'repo_tag' is not required.

        If 'doc_tag' is the Document 'base_dir' and 'based_dir' occurs in more
        than one repository, the 'repo_tag' is required.

        Exceptions
        ----------

        In the event of a bad or ambigous specification the appropriate Django
        ORM exception is raised: models.DoesNotExist or
        models.MultipleObjectsReturned.

        If the document already belongs to the curated collection,
        openn.curated.duplicate_membership.DuplicateMembership is raised.

        """
        curated  = CuratedCollection.objects.get(tag=curated_tag.lower())
        document = self.find_document(doc_tag=doc_tag, repo_tag=repo_tag)
        try:
            membership = CuratedMembership.objects.create(
                curated_collection=curated, document=document)
        except IntegrityError as ie:
            if re.search('Duplicate entry', str(ie)):
                msg = "Membership already exists for document %d/%s and curated %s" % (
                    document.pk,
                    document.base_dir,
                    curated.tag, )
                raise DuplicateMembership(msg)
            else:
                raise

    def remove_document(self, curated_tag, doc_tag, repo_tag=None):
        curated    = CuratedCollection.objects.get(tag=curated_tag.lower())
        document   = self.find_document(doc_tag=doc_tag, repo_tag=repo_tag)

        membership = CuratedMembership.objects.get(curated_collection_id=curated.pk, document_id=document.pk)
        membership.delete()

    def find_document(self, doc_tag, repo_tag=None):
        if self.is_integer(doc_tag):
            return Document.objects.get(pk=int(doc_tag))

        if repo_tag is None:
            return self.doc_by_base_dir(base_dir=doc_tag)

        return self.doc_by_base_dir_and_repo(base_dir=doc_tag, repo_tag=repo_tag)

    def doc_by_base_dir(self, base_dir):
        return Document.objects.get(base_dir=base_dir)

    def doc_by_base_dir_and_repo(self, base_dir, repo_tag):
        repo     = Repository.objects.get(tag=repo_tag.lower())
        return Document.objects.get(repository_id=repo.pk, base_dir=base_dir)

    @staticmethod
    def active_collections():
        """ Return all collections that are 'live' and have documents  marked
        'is_online'. """

        live_curated_ids = set(CuratedMembership.objects.
                               filter(curated_collection__live=True, document__is_online=True).
                               values_list('curated_collection__pk', flat=True))
        colls = list(CuratedCollection.objects.filter(pk__in=live_curated_ids))

        if logging.getLogger().getEffectiveLevel() <= logging.INFO:
            MembershipManager.logger.info("Found %d live curated collections: ", len(colls))
            for coll in colls:
                MembershipManager.logger.info("Add active collection: %s", coll.tag)

        return colls


    def is_integer(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False