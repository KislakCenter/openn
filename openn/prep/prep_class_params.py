class PrepClassParams:
    def __init__(self, params_dict):
        """Create a PrepClassParams object. Params dict should have the
following format.

            {
                'xsl': os.path.join(SITE_ROOT, 'xsl/spreadsheet_xml2tei.xsl'),
                'image_rights': {
                    'dynamic': True,
                },
                'rights_statements': {
                    'images': {
                        'dynamic': True,
                    },
                    'metadata': {
                        'dynamic': True,
                    },
                },
            }

        """
        self._params_dict = params_dict

    def xsl(self):
