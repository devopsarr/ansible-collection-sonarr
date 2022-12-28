# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

try:
    from devopsarr import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False

# have urlparse for backwards compatibility
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from ansible.module_utils.basic import AnsibleModule, env_fallback


class SonarrModule(AnsibleModule):
    def __init__(self, *args, **kwargs):
        # self._validate()
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

        url = urlparse(self.params["sonarr_url"])
        self.api = sonarr.Client(
            hostname=url.hostname,
            port=url.port,
            api_key=self.params["sonarr_api_key"],
            protocol=url.scheme,
            ver="v3",
        )

    def _validate(self):
        if not HAS_SONARR_LIBRARY:
            self.fail_json(msg="Please install the sonarr library")

    def _merge_dictionaries(self, a, b):
        new = a.copy()
        new.update(b)
        return new
