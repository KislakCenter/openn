from openn.prep.virtual_field import VirtualField

class CallNumberField(VirtualField):
    def values(self, validatable_sheet, arg_fields=[]):
        values = self.build_values(validatable_sheet, arg_fields)
        vals = [ unicode(x) for x in values ]
        return [ ', '.join(vals) ]

    def build_values(self, validatable_sheet, arg_fields):
        d = self.extract_values(validatable_sheet, arg_fields)
        vals = []
        if 'call_numberid' in d:
            vals.append(d['call_numberid'])
        if 'archival_drawer' in d:
            vals.append("Drawer %s" %(d['archival_drawer'],))
        if 'archival_box' in d:
            vals.append("Box %s" %(d['archival_box'],))
        if 'archival_folder' in d:
            vals.append("Folder %s" %(d['archival_folder'],))
        if 'archival_item' in d:
            vals.append("Item %s" %(d['archival_item'],))

        return vals

    def extract_values(self, validatable_sheet, arg_fields):
        h = {}
        for field in arg_fields:
            vals = validatable_sheet.values(field)
            val = None if vals is None or len(vals) == 0 else vals[0]
            if val:
                h[field] = val

        return h
