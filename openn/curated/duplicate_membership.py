# -*- coding: utf-8 -*-

from openn.openn_exception import OPennException

class DuplicateMembership(OPennException):
    def __init__(self, message, cause=None, cause_text=None):
        super(DuplicateMembership, self).__init__(
            message=message, cause=cause, cause_text=cause_text)
