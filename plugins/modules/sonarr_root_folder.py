#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_root_folder

short_description: Manages Sonarr root folder.

version_added: "0.0.2"

description: Manages Sonarr root folder.

options:
    path:
        description: Actual root folder.
        required: true
        type: str
    state:
        description: Create or delete a root_folder.
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
# Create a root folder
- name: Create a root folder
  devopsarr.sonarr.root_folder:
    path: '/series'

# Delete a root folder
- name: Delete a root_folder
  devopsarr.sonarr.root_folder:
    path: '/series'
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: root folder ID.
    type: int
    returned: always
    sample: '1'
path:
    description: The root folder path.
    type: str
    returned: 'on create/update'
    sample: '/series'
accessible:
    description: Access flag.
    type: str
    returned: 'on create/update'
    sample: 'true'
unmapped_folders:
    description: List of unmapped folders
    type: dict
    returned: always
    sample: '[]'
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
        # TODO: add validation for root folders
        path=dict(type='str', required=True),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )

    result = dict(
        changed=False,
        id=0,
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    client = sonarr.RootFolderApi(module.api)

    # List resources.
    try:
        root_folders = client.list_root_folder()
    except Exception as e:
        module.fail_json('Error listing root folders: %s' % to_native(e.reason), **result)

    # Check if a resource is present already.
    for root_folder in root_folders:
        if root_folder['path'] == module.params['path']:
            result.update(root_folder.dict(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        if result['id'] != 0:
            result['changed'] = True
            # Only without check mode.
            if not module.check_mode:
                try:
                    response = client.delete_root_folder(result['id'])
                except Exception as e:
                    module.fail_json('Error deleting root folder: %s' % to_native(e.reason), **result)
                result['id'] = 0
        module.exit_json(**result)

    # Create a new resource.
    if result['id'] == 0:
        result['changed'] = True
        # Only without check mode.
        if not module.check_mode:
            try:
                response = client.create_root_folder(root_folder_resource={'path': module.params['path']})
            except Exception as e:
                module.fail_json('Error creating root folder: %s' % to_native(e.reason), **result)
            result.update(response.dict(by_alias=False))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
