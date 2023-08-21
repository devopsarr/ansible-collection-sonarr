# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_field_utils import FieldHelper


class SpecificationHelper():
    def __init__(self):
        # type: () -> None
        self.field_helper = FieldHelper()

        self.specification_args = dict(
            name=dict(type='str'),
            implementation=dict(type='str'),
            negate=dict(type='bool'),
            required=dict(type='bool'),
            fields=dict(type='list', elements='dict', options=self.field_helper.field_args),
        )

    def populate_specifications(self, specification_list, type):
        # type: (list, str) -> list
        specifications = []

        for specification in specification_list:
            spec = {
                'name': specification['name'],
                'implementation': specification['implementation'],
                'negate': specification['negate'],
                'required': specification['required'],
                'fields': self.field_helper.populate_fields(specification['fields']),
            }

            if type == "custom_format":
                specifications.append(
                    sonarr.CustomFormatSpecificationSchema(**spec),
                )
            if type == "auto_tag":
                specifications.append(
                    sonarr.AutoTaggingSpecificationSchema(**spec),
                )

        return specifications
