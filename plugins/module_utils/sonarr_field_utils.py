# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule


class FieldHelper():
    def __init__(self):
        # type: () -> None
        self.field_args = dict(
            name=dict(type='str'),
            value=dict(type='raw'),
        )

    def populate_fields(self, module):
        # type: (SonarrModule) -> list[sonarr.Field]
        fields = []

        for field in module.params['fields']:
            fields.append(
                sonarr.Field(**{
                    'name': field['name'],
                    'value': field['value'],
                }),
            )

        return fields
