#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_remote_path_mapping_info

short_description: Get information about Sonarr remote path mapping.

version_added: "0.5.0"

description: Get information about Sonarr remote path mapping.

options:
    id:
        description: Remote path mapping id.
        type: int

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all remote path mappings.
- name: Gather information about all remote path mappings
  devopsarr.sonarr.sonarr_remote_path_mapping_info:

# Gather information about a single remote path mapping.
- name: Gather information about a single remote path mapping
  devopsarr.sonarr.sonarr_remote_path_mapping_info:
    id: 1
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
remote_path_mappings:
    description: A list of remote path mappings.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: remote path mapping ID.
            type: int
            returned: always
            sample: '1'
        host:
            description: Download Client host.
            type: str
            returned: 'always'
            sample: 'transmission-host'
        remote_path:
            description: Download Client remote path.
            type: str
            returned: 'always'
            sample: '/download/complete/'
        local_path:
            description: Local remote path.
            type: str
            returned: 'always'
            sample: '/series-download/'
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
        id=dict(type='int'),
    )


def list_remote_path_mapping(result):
    try:
        return client.list_remote_path_mapping()
    except Exception as e:
        module.fail_json('Error listing remote path mappings: %s' % to_native(e.reason), **result)


def populate_remote_path_mappings(result):
    mappings = []
    # Check if a resource is present already.
    for remote_path_mapping in list_remote_path_mapping(result):
        if module.params['id']:
            if remote_path_mapping['id'] == module.params['id']:
                mappings = [remote_path_mapping.dict(by_alias=False)]
        else:
            mappings.append(remote_path_mapping.dict(by_alias=False))
    return mappings


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = sonarr.RemotePathMappingApi(module.api)
    result = dict(
        changed=False,
        remote_path_mappings=[],
    )

    # List resources.
    result.update(remote_path_mappings=populate_remote_path_mappings(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
