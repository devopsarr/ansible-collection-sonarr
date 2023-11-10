#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_import_list_schema_info

short_description: Get information about Sonarr import list schema.

version_added: "1.0.0"

description: Get information about Sonarr import list schema.

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
# Gather information about all import lists schema.
- name: Gather information about all import lists schema
  devopsarr.sonarr.sonarr_import_list_schema_info:

# Gather information about a single import list schema.
- name: Gather information about a single import list schema
  devopsarr.sonarr.sonarr_import_list_schema_info:
    name: PlexImport
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
import_lists:
    description: A list of import list.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: import listID.
            type: int
            returned: always
            sample: 1
        name:
            description: Name.
            returned: always
            type: str
            sample: "Example"
        enable_automatic_add:
            description: Enable automatic add flag.
            returned: always
            type: bool
            sample: false
        season_folder:
            description: Season folder flag.
            returned: always
            type: bool
            sample: false
        quality_profile_id:
            description: Quality profile ID.
            returned: always
            type: int
            sample: 1
        should_monitor:
            description: Should monitor.
            returned: always
            type: str
            sample: "unknown"
        root_folder_path:
            description: Root folder path.
            returned: always
            type: str
            sample: "/path"
        series_type:
            description: Series type.
            returned: always
            type: str
            sample: "standard"
        config_contract:
            description: Config contract.
            returned: always
            type: str
            sample: "CustomSettings"
        implementation:
            description: Implementation.
            returned: always
            type: str
            sample: "CustomImport"
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


def list_import_list_schema(result):
    try:
        return client.list_import_list_schema()
    except Exception as e:
        module.fail_json('Error listing import list schemas: %s' % to_native(e.reason), **result)


def populate_import_list_schema(result):
    import_lists = []
    # Check if a resource is present already.
    for import_list in list_import_list_schema(result):
        if module.params['name']:
            if import_list['implementation'] == module.params['name']:
                import_lists = [import_list.dict(by_alias=False)]
        else:
            import_lists.append(import_list.dict(by_alias=False))
    return import_lists


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = sonarr.ImportListApi(module.api)
    result = dict(
        changed=False,
        import_lists=[],
    )

    # List resources.
    result.update(import_lists=populate_import_list_schema(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
