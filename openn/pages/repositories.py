# -*- coding: utf-8 -*-
import logging
import os

from django.template import Context, Template
from django.template.loader import get_template

from operator import itemgetter

from openn.pages.page import Page

class Repositories(Page):

    logger = logging.getLogger(__name__)

    def __init__(self, template_name, outdir, repo_configs,**kwargs):
        self._repo_configs = repo_configs
        super(Repositories,self).__init__(template_name, outdir, **kwargs)

    def get_context(self, ctx_dict={}):
        repositories = self.live_repositories()

        repositories.sort(key=lambda x: x.name())
        ctx = { 'repositories': repositories }
        ctx.update(ctx_dict)
        return super(Repositories, self).get_context(ctx)

    @property
    def title(self):
        return 'Repositories'

    def live_repositories(self, ):
        live_ones = []

        for repo in self._repo_configs.all_repositories():
            if repo.is_live():
                html_dir = os.path.join(self.outdir, repo.html_dir())
                if os.path.exists(html_dir):
                    msg = "Repository added to repositories page (%s)"
                    msg += " (repository is live and has 'html' dir: %s)"
                    msg = msg % (repo.tag(), html_dir)
                    live_ones.append(repo)
                elif repo.no_document():
                    # if this is a no-document repository, add it
                    msg = "Repository added to repositories page (%s)"
                    msg += " (repository is live and is marked no_document)"
                    msg = msg % (repo.tag())
                    live_ones.append(repo)
                else:
                    msg = "Repository not added to repositories page (%s);"
                    msg += " repository set to 'live',"
                    msg += " but HTML directory does not exist: '%s'"
                    msg = msg % (repo.tag(), html_dir,)
            else:
                msg = "Repository not added to repositories page (%s);"
                msg += " repository not set to 'live'"
                msg = msg % (repo.tag(),)
            self.logger.info(msg)

        return live_ones

    def is_needed(self):
        """If the repositories template exits; we always say it's needed.

        Why? If implemented, the tests for creating a new repositories list
        page would ask the following.  A Yes answer to any would trigger
        page generation.

        1. Is there no existing Repositories.html file?

        2. Is the template newer than the current Repositories.html file?

        3. Has the repository information in the settings file changed?

        4. Are there new TOC files for repositories not listed in the
           current Repositories.html?

        Nos. 3 and 4 are too complicated to make it worth figuring out.

        Therefore, we always say the page is needed.

        """
        return self.is_makeable()
