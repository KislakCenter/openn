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

    def __init__(self, image, image_rights, licence_config):
        """Create return formatted licence strings and other values for
        image.

        """
        self._image             = image
        self._document          = image.document
        self._image_rights      = deepcopy(image_rights)
        self._licence_config    = deepcopy(licence_config)

    def rights_properties(self):
        if self._image_rights.get('dynamic', False):
            return self._do_build_properties()
        else:
            return self._image_rights

    def _do_build_properties(self):
        return {
            'Marked': str(self.marked()),
            'WebStatement': self.web_statement(),
            'UsageTerms': self.usage_terms(),
            'rights': self.usage_terms()
        }

    def marked(self):
        return False if self.lic_code() == 'PD' else True

    def usage_terms(self):
        template = self.single_image_template()
        params = {
            'title': self._image.full_name(),
            'holder': self._document.image_copyright_holder,
            'year': self._document.image_copyright_year,
            'more_information': self._document.image_rights_more_info,
        }
        return template.format(**params)

    def web_statement(self):
        data = self.licence_data()
        return data.get('deed_url', '')

    def lic_code(self):
        code = self._image.document.image_licence
        if code and len(code.strip()) > 0:
            return code.strip().upper()
        else:
            return 'PD'

    def single_image_template(self):
        return self.licence_data()['single_image']

    def licence_data(self):
        code = self.lic_code()
        return self._licence_config[code]
