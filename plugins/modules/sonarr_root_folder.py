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

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials
    - devopsarr.sonarr.sonarr_state

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a root folder
- name: Create a root folder
  devopsarr.sonarr.sonarr_root_folder:
    path: '/series'

# Delete a root folder
- name: Delete a root_folder
  devopsarr.sonarr.sonarr_root_folder:
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


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        path=dict(type='str', required=True),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )


def create_root_folder(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_root_folder(root_folder_resource=want)
        except Exception as e:
            module.fail_json('Error creating root folder: %s' % to_native(e.reason), **result)
        result.update(response.dict(by_alias=False))
    module.exit_json(**result)


def list_root_folders(result):
    try:
        return client.list_root_folder()
    except Exception as e:
        module.fail_json('Error listing root folders: %s' % to_native(e.reason), **result)


def find_root_folder(path, result):
    for folder in list_root_folders(result):
        if folder['path'] == path:
            return folder
    return None


def delete_root_folder(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_root_folder(result['id'])
            except Exception as e:
                module.fail_json('Error deleting root folder: %s' % to_native(e.reason), **result)
            result['id'] = 0
    module.exit_json(**result)


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )

    # Init client and result.
    client = sonarr.RootFolderApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_root_folder(module.params['path'], result)
    if state:
        result.update(state.dict(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_root_folder(result)

    # Create a new resource.
    if result['id'] == 0:
        create_root_folder({'path': module.params['path']}, result)

    # No need for update
    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
