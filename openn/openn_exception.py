# -*- coding: utf-8 -*-

class OPennException(Exception):
    def __init__(self, message, cause=None):
        if cause is None:
            super(OPennException, self).__init__(message)
        else:
            super(OPennException, self).__init__(message + u', caused by ' + repr(cause))
        self.cause = cause
