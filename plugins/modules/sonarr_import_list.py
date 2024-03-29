#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_import_list

short_description: Manages Sonarr import list.

version_added: "1.0.0"

description: Manages Sonarr import list.

options:
    name:
        description: Name.
        required: true
        type: str
    season_folder:
        description: Season folder flag.
        type: bool
    enable_automatic_add:
        description: Enable autometic add flag.
        type: bool
    quality_profile_id:
        description: Quality profile ID.
        type: int
    should_monitor:
        description: Should monitor.
        type: str
    root_folder_path:
        description: Root folder path.
        type: str
    series_type:
        description: Series type.
        type: str
    update_secrets:
        description: Flag to force update of secret fields.
        type: bool
        default: false

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials
    - devopsarr.sonarr.sonarr_implementation
    - devopsarr.sonarr.sonarr_taggable
    - devopsarr.sonarr.sonarr_state

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a import list
- name: Create a import list
  devopsarr.sonarr.sonarr_import_list:
    enable_automatic_add: false
    should_monitor: "unknown"
    quality_profile_id: 1
    root_folder_path: "/config"
    season_folder: false
    fields:
    - name: "apiKey"
      value: "Key"
    - name: "baseUrl"
      value: "localhost"
    - name: "languageProfileIds"
      value: [1]
    name: "SonarrImport"
    series_type: "standard"
    config_contract: "SonarrSettings"
    implementation: "SonarrImport"
    tags: []

# Delete a import list
- name: Delete a import list
  devopsarr.sonarr.sonarr_import_list:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
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
from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_field_utils import FieldHelper
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def is_changed(status, want):
    if (want.name != status.name or
            want.enable_automatic_add != status.enable_automatic_add or
            want.should_monitor != status.should_monitor or
            want.quality_profile_id != status.quality_profile_id or
            want.season_folder != status.season_folder or
            want.config_contract != status.config_contract or
            want.implementation != status.implementation or
            want.series_type != status.series_type or
            want.tags != status.tags):
        return True

    for status_field in status.fields:
        for want_field in want.fields:
            if want_field.name == status_field.name and want_field.value != status_field.value and status_field.value != "********":
                return True
    return False


def run_module():
    field_helper = FieldHelper()

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        enable_automatic_add=dict(type='bool'),
        season_folder=dict(type='bool'),
        quality_profile_id=dict(type='int'),
        config_contract=dict(type='str'),
        implementation=dict(type='str'),
        should_monitor=dict(type='str'),
        root_folder_path=dict(type='str'),
        series_type=dict(type='str'),
        tags=dict(type='list', elements='int', default=[]),
        fields=dict(type='list', elements='dict', options=field_helper.field_args),
        state=dict(default='present', type='str', choices=['present', 'absent']),
        # Needed to manage obfuscate response from api "********"
        update_secrets=dict(type='bool', default=False),
    )

    result = dict(
        changed=False,
        id=0,
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    list = sonarr.ImportListApi(module.api)

    # List resources.
    try:
        lists = list.list_import_list()
    except Exception as e:
        module.fail_json('Error listing import lists: %s' % to_native(e.reason), **result)

    state = sonarr.ImportListResource()
    # Check if a resource is present already.
    for import_list in lists:
        if import_list['name'] == module.params['name']:
            result.update(import_list.dict(by_alias=False))
            state = import_list

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        if result['id'] != 0:
            result['changed'] = True
            if not module.check_mode:
                try:
                    response = list.delete_import_list(result['id'])
                except Exception as e:
                    module.fail_json('Error deleting import list: %s' % to_native(e.reason), **result)
                result['id'] = 0
        module.exit_json(**result)

    want = sonarr.ImportListResource(**{
        'name': module.params['name'],
        'season_folder': module.params['season_folder'],
        'quality_profile_id': module.params['quality_profile_id'],
        'should_monitor': module.params['should_monitor'],
        'root_folder_path': module.params['root_folder_path'],
        'config_contract': module.params['config_contract'],
        'implementation': module.params['implementation'],
        'series_type': module.params['series_type'],
        'enable_automatic_add': module.params['enable_automatic_add'],
        'tags': module.params['tags'],
        'fields': field_helper.populate_fields(module.params['fields']),
    })

    # Create a new resource.
    if result['id'] == 0:
        result['changed'] = True
        # Only without check mode.
        if not module.check_mode:
            try:
                response = list.create_import_list(import_list_resource=want)
            except Exception as e:
                module.fail_json('Error creating import list: %s' % to_native(e.reason), **result)
            result.update(response.dict(by_alias=False))
        module.exit_json(**result)

    # Update an existing resource.
    want.id = result['id']
    if is_changed(state, want) or module.params['update_secrets']:
        result['changed'] = True
        if not module.check_mode:
            try:
                response = list.update_import_list(import_list_resource=want, id=str(want.id))
            except Exception as e:
                module.fail_json('Error updating import list: %s' % to_native(e), **result)
        result.update(response.dict(by_alias=False))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
