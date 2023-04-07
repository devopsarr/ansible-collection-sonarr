#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_root_folder_info

short_description: Get information about Sonarr root folder.

version_added: "0.5.0"

description: Get information about Sonarr root folder.

options:
    path:
        description: Actual root folder.
        type: str

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all root folders.
- name: Gather information about all root folders
  devopsarr.sonarr.sonarr_root_folder_info:

# Gather information about a single root folder.
- name: Gather information about a single root folder
  devopsarr.sonarr.sonarr_root_folder_info:
    name: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
root_folders:
    description: A list of root folders.
    returned: always
    type: list
    elements: dict
    contains:
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
        path=dict(type='str'),
    )

    result = dict(
        changed=False,
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

    folders = []
    # Check if a resource is present already.
    for root_folder in root_folders:
        if module.params['path']:
            if root_folder['path'] == module.params['path']:
                folders = [root_folder.dict(by_alias=False)]
        else:
            folders.append(root_folder.dict(by_alias=False))

    result.update(root_folders=folders)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
