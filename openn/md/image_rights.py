# -*- coding: utf-8 -*-

from copy import deepcopy

class ImageRights:
    """
        'image_rights': {
            'Marked': 'False',
            'WebStatement': 'http://creativecommons.org/publicdomain/mark/1.0/',
            'UsageTerms': 'This image and its content are free of known
                           copyright restrictions and in the public domain.
                           See the Creative Commons Public Domain Mark page
                           for usage details,
                           http://creativecommons.org/publicdomain/mark/1.0/.',
            'rights': 'This image and its content are free of known copyright
                       restrictions and in the public domain. See the Creative
                       Commons Public Domain Mark page for usage details,
                       http://creativecommons.org/publicdomain/mark/1.0/.',
        },

    """

    def __init__(self, image, license):
        """Create return formatted licence strings and other values for
        image.

        """
        self._image = image
        self._document = image.document
        self._license = license

    def rights_properties(self):
        return {
            'Marked': str(self.marked()),
            'WebStatement': self.web_statement(),
            'UsageTerms': self.usage_terms(),
            'rights': self.usage_terms()
        }

    def marked(self):
        if self._license.code().startswith('PD'):
            return False

        return True

    def usage_terms(self):
        return self._license.format_single_image(**self._image.image_license_args())

    def web_statement(self):
        return self._license.deed_url()

    def lic_code(self):
        return '-'.join([self._license.code(), self._license.version()])
