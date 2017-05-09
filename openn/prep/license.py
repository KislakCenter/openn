# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
import pytz

class License(object):
    """docstring for LicenseGroup"""
    def __init__(self, license_dict):
        super(License, self).__init__()
        self.license_dict = deepcopy(license_dict)

    def format_metadata(self, **license_args):
        return self._do_format(self.license_dict['metadata'], **license_args)

    def format_images(self, **license_args):
        return self._do_format(self.license_dict['images'], **license_args)

    def format_single_image(self, **license_args):
        return self._do_format(self.license_dict['single_image'], **license_args)

    def is_marked(self):
        return self.license_dict.get('marked', True)

    def legalcode_url(self):
        return self.license_dict['legalcode_url']

    def deed_url(self):
        return self.license_dict['deed_url']

    def version(self):
        return self.license_dict['version']

    def code(self):
        return self.license_dict['code']

    def _do_format(self, text, **license_args):
        kwargs = {}

        for k in license_args:
            if license_args[k] is None:
                kwargs[k] = ''
            else:
                kwargs[k] = license_args[k]

        outstr = text.format(**kwargs)

        return outstr.strip()

class LicenseFactory(object):
    "Factory to return License objects."

    def __init__(self, licenses_dict):
        super(LicenseFactory, self).__init__()
        self._licenses_dict = deepcopy(licenses_dict)

    def license(self, code):
        return License(self._licenses_dict[code])
