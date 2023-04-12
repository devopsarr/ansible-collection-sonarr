#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_download_client_config

short_description: Manages Sonarr download client config.

version_added: "0.5.0"

description: Manages Sonarr download client config.

options:
    auto_redownload_failed:
        description: Auto redownload failed.
        required: true
        type: bool
    enable_completed_download_handling:
        description: Enable completed download handling.
        required: true
        type: bool

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update download client config
- name: Update download client config
  devopsarr.sonarr.sonarr_download_client_config:
    auto_redownload_failed: false
    enable_completed_download_handling: true
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Download client config ID.
    type: int
    returned: always
    sample: '1'
auto_redownload_failed:
    description: Maximum size.
    returned: always
    type: bool
    sample: true
enable_completed_download_handling:
    description: Minimum age.
    returned: always
    type: bool
    sample: true
download_client_working_folders:
    description: Retention.
    returned: always
    type: string
    sample: '_UNPACK_|_FAILED_'
'''

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule
from ansible.module_utils.common.text.converters import to_native


try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        enable_completed_download_handling=dict(type='bool', required=True),
        auto_redownload_failed=dict(type='bool', required=True),
    )

    result = dict(
        changed=False,
        id=0,
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    client = sonarr.DownloadClientConfigApi(module.api)

    # Get resource.
    try:
        client_config = client.get_download_client_config()
    except Exception as e:
        module.fail_json('Error getting download client config: %s' % to_native(e.reason), **result)

    result.update(client_config.dict(by_alias=False))

    want = sonarr.DownloadClientConfigResource(**{
        'enable_completed_download_handling': module.params['enable_completed_download_handling'],
        'auto_redownload_failed': module.params['auto_redownload_failed'],
        'download_client_working_folders': '_UNPACK_|_FAILED_',
        'id': 1,
    })

    # Update an existing resource.
    if want != client_config:
        result['changed'] = True
        if not module.check_mode:
            try:
                response = client.update_download_client_config(download_client_config_resource=want, id=str(want.id))
            except Exception as e:
                module.fail_json('Error updating download client config: %s' % to_native(e.reason), **result)
        result.update(response.dict(by_alias=False))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
