# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

try:
    from pyarr import SonarrAPI
    HAS_PYARR_LIBRARIY = True
except ImportError:
    HAS_PYARR_LIBRARIY = False

from ansible.module_utils.basic import AnsibleModule, env_fallback


class SonarrModule(AnsibleModule):
    def __init__(self, *args, **kwargs):
        arg_spec = kwargs.get('argument_spec', {})

        kwargs['argument_spec'] = self._merge_dictionaries(
            arg_spec,
            dict(
                sonarr_url=dict(
                    required=True,
                    type='str',
                    fallback=(env_fallback, ['SONARR_URL'])),
                sonarr_api_key=dict(
                    required=True,
                    type='str',
                    fallback=(env_fallback, ['SONARR_API_KEY']),
                    no_log=True)
            )
        )

        AnsibleModule.__init__(self, *args, **kwargs)

        self.api = SonarrAPI(self.params["sonarr_url"], self.params["sonarr_api_key"], "/v3")

    def _validate(self):
        if not HAS_PYARR_LIBRARIY:
            self.module.fail_json(msg="Please install the pyarr library")

    def _merge_dictionaries(self, a, b):
        new = a.copy()
        new.update(b)
        return new
