#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_download_client_info

short_description: Get information about Sonarr download client.

version_added: "0.6.0"

description: Get information about Sonarr download client.

options:
    name:
        description: Name.
        type: str

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all download clients.
- name: Gather information about all download clients
  devopsarr.sonarr.sonarr_download_client_info:

# Gather information about a single download client.
- name: Gather information about a single download client
  devopsarr.sonarr.sonarr_download_client_info:
    name: Example
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
download_clients:
    description: A list of download client.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: download clientID.
            type: int
            returned: always
            sample: 1
        name:
            description: Name.
            returned: always
            type: str
            sample: "Example"
        remove_completed_downloads:
            description: Remove completed downloads flag.
            returned: always
            type: bool
            sample: true
        remove_failed_downloads:
            description: Remove failed downloads flag.
            returned: always
            type: bool
            sample: false
        enable:
            description: Enable flag.
            returned: always
            type: bool
            sample: true
        priority:
            description: Priority.
            returned: always
            type: int
            sample: 1
        config_contract:
            description: Config contract.
            returned: always
            type: str
            sample: "BroadcastheNetSettings"
        implementation:
            description: Implementation.
            returned: always
            type: str
            sample: "BroadcastheNet"
        protocol:
            description: Protocol.
            returned: always
            type: str
            sample: "torrent"
        tags:
            description: Tag list.
            type: list
            returned: always
            elements: int
            sample: [1,2]
        fields:
            description: field list.
            type: list
            returned: always
'''

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        name=dict(type='str'),
    )


def list_download_clients(result):
    try:
        return client.list_download_client()
    except Exception as e:
        module.fail_json('Error listing download clients: %s' % to_native(e.reason), **result)


def populate_download_clients(result):
    download_clients = []
    # Check if a resource is present already.
    for download_client in list_download_clients(result):
        if module.params['name']:
            if download_client['name'] == module.params['name']:
                download_clients = [download_client.dict(by_alias=False)]
        else:
            download_clients.append(download_client.dict(by_alias=False))
    return download_clients


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = sonarr.DownloadClientApi(module.api)
    result = dict(
        changed=False,
        download_clients=[],
    )

    # List resources.
    result.update(download_clients=populate_download_clients(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
