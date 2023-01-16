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
# Create a root folder
- name: Create a root folder
  devopsarr.sonarr.root_folder:
    path: '/series'

# Delete a root folder
- name: Delete a root_folder
  devopsarr.sonarr.root_folder:
    path: 'series'
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

    root_folders = client.list_root_folder()

    for root_folder in root_folders:
        if root_folder['path'] == module.params['path']:
            result.update(root_folder)

    # TODO: add error handling
    if module.params['state'] == 'present' and result['id'] == 0:
        result['changed'] = True
        if not module.check_mode:
            response = client.create_root_folder(root_folder_resource={'path': module.params['path']})
            result.update(response)
    elif module.params['state'] == 'absent' and result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            response = client.delete_root_folder(result['id'])
            result['id'] = 0
    elif module.check_mode:
        module.exit_json(**result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
