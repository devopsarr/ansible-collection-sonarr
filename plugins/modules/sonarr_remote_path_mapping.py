#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_remote_path_mapping

short_description: Manages Sonarr remote path mapping.

version_added: "0.0.4"

description: Manages Sonarr remote path mapping.

options:
    host:
        description: Download Client host.
        required: true
        type: str
    remote_path:
        description: Download Client remote path.
        required: true
        type: str
    local_path:
        description: Local path.
        required: true
        type: str
    state:
        description: Create or delete a remote_path_mapping.
        required: false
        default: 'present'
        choices: [ "present", "absent" ]
        type: str

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a remote path mapping
- name: Create a remote path mapping
  devopsarr.sonarr.remote_path_mapping:
    host: 'transmission-host'
    remote_path: '/download/complete/'
    local_path: '/series-download/'


# Delete a remote path mapping
- name: Delete a remote_path_mapping
  devopsarr.sonarr.remote_path_mapping:
    host: 'transmission-host'
    remote_path: '/download/complete/'
    local_path: '/series-download/'
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
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


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        host=dict(type='str', required=True),
        remote_path=dict(type='str', required=True),
        local_path=dict(type='str', required=True),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )

    result = dict(
        changed=False,
        id=0,
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    client = sonarr.RemotePathMappingApi(module.api)

    # List resources.
    try:
        remote_path_mappings = client.list_remote_path_mapping()
    except Exception as e:
        module.fail_json('Error listing remote path mappings: %s' % to_native(e.reason), **result)

    # Check if a resource is present already.
    for remote_path_mapping in remote_path_mappings:
        if remote_path_mapping['host'] == module.params['host'] and \
           remote_path_mapping['remote_path'] == module.params['remote_path'] and \
           remote_path_mapping['local_path'] == module.params['local_path']:
            result.update(remote_path_mapping.dict(by_alias=False))

    want = sonarr.RemotePathMappingResource(**{
        'host': module.params['host'],
        'remote_path': module.params['remote_path'],
        'local_path': module.params['local_path'],
    })

    # Create a new resource.
    if module.params['state'] == 'present' and result['id'] == 0:
        result['changed'] = True
        # Only without check mode.
        if not module.check_mode:
            try:
                response = client.create_remote_path_mapping(remote_path_mapping_resource=want)
            except Exception as e:
                module.fail_json('Error creating remote path mapping: %s' % to_native(e.reason), **result)
            result.update(response.dict(by_alias=False))

    # Delete the resource.
    elif module.params['state'] == 'absent' and result['id'] != 0:
        result['changed'] = True
        # Only without check mode.
        if not module.check_mode:
            try:
                response = client.delete_remote_path_mapping(result['id'])
            except Exception as e:
                module.fail_json('Error deleting remote path mapping: %s' % to_native(e.reason), **result)
            result['id'] = 0

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
