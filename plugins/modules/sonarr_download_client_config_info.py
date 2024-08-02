#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_download_client_config_info

short_description: Get information about Sonarr download client config.

version_added: "0.5.0"

description: Get information about Sonarr download client config.

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch download client config
- name: fetch download client config
  devopsarr.sonarr.sonarr_download_client_config_info:
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Download client config ID.
    type: int
    returned: always
    sample: '1'
auto_redownload_failed:
    description: Auto redownload failed.
    returned: always
    type: bool
    sample: true
auto_redownload_failed_from_interactive_search:
    description: Auto redownload failed from interactive search.
    returned: always
    type: bool
    sample: true
enable_completed_download_handling:
    description: Enable completed download handling.
    returned: always
    type: bool
    sample: true
download_client_working_folders:
    description: download client working folders.
    returned: always
    type: str
    sample: '_UNPACK_|_FAILED_'
'''

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def get_download_client_config(result):
    try:
        return client.get_download_client_config()
    except sonarr.ApiException as e:
        module.fail_json('Error getting download client config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting download client config: {}'.format(to_native(e)), **result)


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec={},
        supports_check_mode=True,
    )
    # Init client and result.
    client = sonarr.DownloadClientConfigApi(module.api)
    result = dict(
        changed=False,
    )

    # Get resource.
    result.update(get_download_client_config(result).model_dump(by_alias=False))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
