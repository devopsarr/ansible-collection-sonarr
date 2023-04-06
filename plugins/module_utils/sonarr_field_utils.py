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


class FieldException():
    def __init__(self, api, py):
        # type: (str, str) -> None
        self.api = api
        self.py = py

    def __getitem__(self, item):
        return getattr(self, item)


class FieldHelper():
    def __init__(self, fields):
        # type: (list[str]) -> None
        self.fields = fields
        self.exceptions = [
            FieldException(
                api='seedCriteria.seasonPackSeedTime',
                py='season_pack_seed_time',
            ),
            FieldException(
                api='seedCriteria.seedRatio',
                py='seed_ratio',
            ),
            FieldException(
                api='seedCriteria.seedTime',
                py='seed_time',
            ),
        ]

    def __getitem__(self, item):
        return getattr(self, item)

    def _to_camel_case(self, snake_str):
        # type: (str) -> str
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def _api_value(self, py_value):
        # type: (str) -> str
        for field in self.exceptions:
            if py_value == field['py']:
                return field['api']
        return self._to_camel_case(py_value)

    def populate_fields(self, module):
        # type: (SonarrModule) -> list[sonarr.Field]
        fields = []

        for field in self.fields:
            if field in module.params:
                fields.append(
                    sonarr.Field(**{
                        'name': self._api_value(field),
                        'value': module.params[field],
                    }),
                )

        return fields
