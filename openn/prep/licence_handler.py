import re
from copy import deepcopy
from collections import defaultdict

from openn.openn_exception import OPennException

class LicenceHandler:
    NORMALIZE_RE = re.compile(r'\W')

    def __init__(self, licences_config):
        # just make a copy of the config
        self._config = deepcopy(licences_config)

    def format_statement(self, licence, content_type,
                         year=None, holder=None, title=None,
                         more_information=None, rights_url=None,
                         resource_url=None):

        """Format the licence statement with ``licence`` code, for
        ``content_type``, and the parameters ``year``, ``holder``,
        ``title``, ``more_information``.

        Important: Not all parameters are used for all licence types.
        For example, 'PD' does not require `year`.

          - ``licence``: 'CC-BY', 'CC0', 'PD', etc.

          - ``content_type``: 'metadata', 'images', or 'single_image'

          - ``year``: copyright year of the metadata, image, or images

          - ``holder``: copyright holder of the metadata, image, or
            images

          - ``title``: title of the work or image as you would like it
            to appear in the copyright statetement

          - ``rights_url``: link to page with page with information
            (not now used)

          - ``resource_url``: persistent link to a canonical page for
            the licensed resource on an institutional website (not now
            used)

          - ``more_information``: any additional information you would
            like to appear in the copyright statetment; for example,
            "For a full description of My University's licensing
            policy please see http://www.example.com/licenses"

                - _Important_: **Do not** add HTML, like ``<a>`` tags,
                  to ``more_information`` or any parameters.  Adding
                  links is handled automatically.

        Example:
        ::

           format_statement('CC-BY', 'metatda', year=2015,
                            holder='My Institution',
                            title='MS MI-12345 Bible')

        Extra information can be provided using extra keyword
        arguments, but they will be used only if the name fields occur
        in the statement string.

        """
        text = self.licence_text(licence, content_type)
        params = [
            'year', 'holder', 'title', 'more_information',
            'rights_url', 'resource_url'
        ]
        args = {}
        for x in params: args[x] = eval(x) or ''

        return text.format(**args)

    def licence_text(self, licence, content_type):
        return self._get_value_for_licence(licence, content_type)

    def legalcode_url(self, licence):
        return self._get_value_for_licence(licence, 'legalcode_url')

    def deed_url(self, licence):
        """Return URL if set in configuration; otherwise return
        ``None``. License deed URL is not required.

        """
        # lic_config = self._get_value(licence)
        # return lic_config.get('deed_url', None)
        return self._get_value_for_licence(licence, 'deed_url')

    def _get_value_for_licence(self, licence, key):
        # get the LICENSES dict
        name = 'licence'
        lic_dict = self._get_value(licence, self._config, name)

        # Add the key to the name; and get the specific value
        name += ": %s" % (key,)
        return self._get_value(key, lic_dict, name)

    def _get_value(self, key, adict, name='value'):
        try:
            return adict[key]
        except KeyError as ex:
            expected = ', '.join(adict.keys())
            msg = "Could not find %s named: '%s'; expected one of: %s" % (name, key, expected)
            raise OPennException(msg)
