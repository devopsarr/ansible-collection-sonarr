#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_indexer

short_description: Manages Sonarr indexer.

version_added: "0.5.0"

description: Manages Sonarr indexer.

options:
    name:
        description: Name.
        required: true
        type: str
    enable_automatic_search:
        description: Enable automatic search flag.
        type: bool
    enable_interactive_search:
        description: Enable interactive search flag.
        type: bool
    enable_rss:
        description: Enable RSS flag.
        type: bool
    priority:
        description: Priority.
        type: int
    download_client_id:
        description: Download client ID.
        type: int
        default: 0
    protocol:
        description: Protocol.
        choices: [ "torrent", "usenet" ]
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
# Create a indexer
- name: Create a indexer
  devopsarr.sonarr.sonarr_indexer:
    name: "Example"
    enable_automatic_search: false
    enable_interactive_search: false
    enable_rss: false
    priority: 10
    config_contract: "FanzubSettings"
    implementation: "Fanzub"
    protocol: "usenet"
    fields:
    - name: "baseUrl"
      value: "http://fanzub.com/rss/"
    - name: "animeStandardFormatSearch"
      value: true
    tags: [1,2]

# Delete a indexer
- name: Delete a indexer
  devopsarr.sonarr.sonarr_indexer:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: indexer ID.
    type: int
    returned: always
    sample: 1
name:
    description: Name.
    returned: always
    type: str
    sample: "Example"
enable_automatic_search:
    description: Enable automatic search flag.
    returned: always
    type: bool
    sample: true
enable_interactive_search:
    description: Enable interactive search flag.
    returned: always
    type: bool
    sample: false
enable_rss:
    description: Enable RSS flag.
    returned: always
    type: bool
    sample: true
priority:
    description: Priority.
    returned: always
    type: int
    sample: 1
download_client_id:
    description: Download client ID.
    returned: always
    type: int
    sample: 0
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
from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_field_utils import FieldHelper
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def is_changed(status, want):
    if (want.name != status.name or
            want.enable_automatic_search != status.enable_automatic_search or
            want.enable_interactive_search != status.enable_interactive_search or
            want.enable_rss != status.enable_rss or
            want.priority != status.priority or
            want.download_client_id != status.download_client_id or
            want.config_contract != status.config_contract or
            want.implementation != status.implementation or
            want.protocol != status.protocol or
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
        enable_automatic_search=dict(type='bool'),
        enable_interactive_search=dict(type='bool'),
        enable_rss=dict(type='bool'),
        priority=dict(type='int'),
        download_client_id=dict(type='int', default=0),
        config_contract=dict(type='str'),
        implementation=dict(type='str'),
        protocol=dict(type='str', choices=['usenet', 'torrent']),
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

    client = sonarr.IndexerApi(module.api)

    # List resources.
    try:
        indexers = client.list_indexer()
    except Exception as e:
        module.fail_json('Error listing indexers: %s' % to_native(e.reason), **result)

    state = sonarr.IndexerResource()
    # Check if a resource is present already.
    for indexer in indexers:
        if indexer['name'] == module.params['name']:
            result.update(indexer.dict(by_alias=False))
            state = indexer

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        if result['id'] != 0:
            result['changed'] = True
            if not module.check_mode:
                try:
                    response = client.delete_indexer(result['id'])
                except Exception as e:
                    module.fail_json('Error deleting indexer: %s' % to_native(e.reason), **result)
                result['id'] = 0
        module.exit_json(**result)

    want = sonarr.IndexerResource(**{
        'name': module.params['name'],
        'enable_automatic_search': module.params['enable_automatic_search'],
        'enable_interactive_search': module.params['enable_interactive_search'],
        'enable_rss': module.params['enable_rss'],
        'priority': module.params['priority'],
        'download_client_id': module.params['download_client_id'],
        'config_contract': module.params['config_contract'],
        'implementation': module.params['implementation'],
        'protocol': module.params['protocol'],
        'tags': module.params['tags'],
        'fields': field_helper.populate_fields(module.params['fields']),
    })

    # Create a new resource.
    if result['id'] == 0:
        result['changed'] = True
        # Only without check mode.
        if not module.check_mode:
            try:
                response = client.create_indexer(indexer_resource=want)
            except Exception as e:
                module.fail_json('Error creating indexer: %s' % to_native(e.reason), **result)
            result.update(response.dict(by_alias=False))
        module.exit_json(**result)

    # Update an existing resource.
    want.id = result['id']
    if is_changed(state, want) or module.params['update_secrets']:
        result['changed'] = True
        if not module.check_mode:
            try:
                response = client.update_indexer(indexer_resource=want, id=str(want.id))
            except Exception as e:
                module.fail_json('Error updating indexer: %s' % to_native(e.reason), **result)
        result.update(response.dict(by_alias=False))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
