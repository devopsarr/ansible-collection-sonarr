#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_download_client_flood

short_description: Manages Sonarr download client Flood.

version_added: "0.6.0"

description: Manages Sonarr download client Flood.

options:
    update_secrets:
        description: Flag to force update of secret fields.
        type: bool
        default: false
    use_ssl:
        description: Use SSL.
        type: bool
    start_on_add:
        description: Start on add.
        type: bool
    host:
        description: Host.
        type: str
    url_base:
        description: URL base.
        type: str
    username:
        description: Username.
        type: str
    password:
        description: Password.
        type: str
    destination:
        description: Destination.
        type: str
    port:
        description: Port.
        type: int
    additional_tags:
        description: Additional Tags.
        type: list
        elements: int
    field_tags:
        description: Field Tags.
        type: list
        elements: str
    post_import_tags:
        description: Post import Tags.
        type: list
        elements: str

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials
    - devopsarr.sonarr.sonarr_download_client

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a download client
- name: Create a download client
  devopsarr.sonarr.sonarr_download_client_flood:
    remove_completed_downloads: false
    remove_failed_downloads: false
    enable: false
    priority: 1
    name: "Flood"
    host: "localhost"
    url_base: "/flood"
    port: 3000
    use_ssl: false
    start_on_add: true
    field_tags: ["sonarr"]
    username: "user"
    password: "password"
    tags: [1,2]

# Delete a download client
- name: Delete a download client
  devopsarr.sonarr.sonarr_download_client_flood:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
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
from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_field_utils import FieldHelper, DownloadClientHelper
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        remove_completed_downloads=dict(type='bool'),
        remove_failed_downloads=dict(type='bool'),
        enable=dict(type='bool'),
        priority=dict(type='int'),
        tags=dict(type='list', elements='int', default=[]),
        state=dict(default='present', type='str', choices=['present', 'absent']),
        # Needed to manage obfuscate response from api "********"
        update_secrets=dict(type='bool', default=False),
        # Field values
        start_on_add=dict(type='bool'),
        use_ssl=dict(type='bool'),
        host=dict(type='str'),
        url_base=dict(type='str'),
        username=dict(type='str'),
        password=dict(type='str', no_log=True),
        destination=dict(type='str'),
        port=dict(type='int'),
        additional_tags=dict(type='list', elements='int'),
        field_tags=dict(type='list', elements='str'),
        post_import_tags=dict(type='list', elements='str'),
    )

    result = dict(
        changed=False,
        id=0,
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    client = sonarr.DownloadClientApi(module.api)

    # List resources.
    try:
        clients = client.list_download_client()
    except Exception as e:
        module.fail_json('Error listing download clients: %s' % to_native(e.reason), **result)

    state = sonarr.DownloadClientResource()
    # Check if a resource is present already.
    for download_client in clients:
        if download_client['name'] == module.params['name']:
            result.update(download_client.dict(by_alias=False))
            state = download_client

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        if result['id'] != 0:
            result['changed'] = True
            if not module.check_mode:
                try:
                    response = client.delete_download_client(result['id'])
                except Exception as e:
                    module.fail_json('Error deleting download client: %s' % to_native(e.reason), **result)
                result['id'] = 0
        module.exit_json(**result)

    client_helper = DownloadClientHelper(state)
    field_helper = FieldHelper(fields=client_helper.download_client_fields)
    want = sonarr.DownloadClientResource(**{
        'name': module.params['name'],
        'remove_completed_downloads': module.params['remove_completed_downloads'],
        'remove_failed_downloads': module.params['remove_failed_downloads'],
        'enable': module.params['enable'],
        'priority': module.params['priority'],
        'config_contract': 'FloodSettings',
        'implementation': 'Flood',
        'protocol': 'torrent',
        'tags': module.params['tags'],
        'fields': field_helper.populate_fields(module),
    })

    # Create a new resource.
    if result['id'] == 0:
        result['changed'] = True
        # Only without check mode.
        if not module.check_mode:
            try:
                response = client.create_download_client(download_client_resource=want)
            except Exception as e:
                module.fail_json('Error creating download client: %s' % to_native(e.reason), **result)
            result.update(response.dict(by_alias=False))
        module.exit_json(**result)

    # Update an existing resource.
    want.id = result['id']
    if client_helper.is_changed(want) or module.params['update_secrets']:
        result['changed'] = True
        if not module.check_mode:
            try:
                response = client.update_download_client(download_client_resource=want, id=str(want.id))
            except Exception as e:
                module.fail_json('Error updating download client: %s' % to_native(e), **result)
        result.update(response.dict(by_alias=False))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
