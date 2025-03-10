#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_download_client

short_description: Manages Sonarr download client.

version_added: "0.6.0"

description: Manages Sonarr download client.

options:
    name:
        description: Name.
        required: true
        type: str
    remove_completed_downloads:
        description: Remove completed downloads flag.
        type: bool
    remove_failed_downloads:
        description: Remove failed downloads flag.
        type: bool
    enable:
        description: Enable flag.
        type: bool
    priority:
        description: Priority.
        type: int
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
# Create a download client
- name: Create a download client
  devopsarr.sonarr.sonarr_download_client:
    remove_completed_downloads: false
    remove_failed_downloads: false
    enable: false
    priority: 1
    name: "Hadouken"
    fields:
    - name: "host"
      value: "hadouken.lcl"
    - name: "urlBase"
      value: "/hadouken/"
    - name: "port"
      value: 9091
    - name: "category"
      value: "sonarr-tv"
    - name: "username"
      value: "username"
    - name: "password"
      value: "password"
    - name: "useSsl"
      value: true
    protocol: "torrent"
    config_contract: "HadoukenSettings"
    implementation: "Hadouken"
    tags: [1,2]

# Delete a download client
- name: Delete a download client
  devopsarr.sonarr.sonarr_download_client:
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
from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_field_utils import FieldHelper
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def is_changed(status, want):
    if (want.name != status.name or
            want.remove_completed_downloads != status.remove_completed_downloads or
            want.remove_failed_downloads != status.remove_failed_downloads or
            want.enable != status.enable or
            want.priority != status.priority or
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


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        name=dict(type='str', required=True),
        remove_completed_downloads=dict(type='bool'),
        remove_failed_downloads=dict(type='bool'),
        enable=dict(type='bool'),
        priority=dict(type='int'),
        config_contract=dict(type='str'),
        implementation=dict(type='str'),
        protocol=dict(type='str', choices=['usenet', 'torrent']),
        tags=dict(type='list', elements='int', default=[]),
        fields=dict(type='list', elements='dict', options=field_helper.field_args),
        state=dict(default='present', type='str', choices=['present', 'absent']),
        # Needed to manage obfuscate response from api "********"
        update_secrets=dict(type='bool', default=False),
    )


def create_download_client(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_download_client(download_client_resource=want)
        except sonarr.ApiException as e:
            module.fail_json('Error creating download client: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating download client: {}'.format(to_native(e)), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_download_clients(result):
    try:
        return client.list_download_client()
    except sonarr.ApiException as e:
        module.fail_json('Error listing download clients: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing download clients: {}'.format(to_native(e)), **result)


def find_download_client(name, result):
    for download_client in list_download_clients(result):
        if download_client.name == name:
            return download_client
    return None


def update_download_client(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_download_client(download_client_resource=want, id=want.id)
        except sonarr.ApiException as e:
            module.fail_json('Error updating download client: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating download client: {}'.format(to_native(e)), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.model_dump(by_alias=False))


def delete_download_client(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_download_client(result['id'])
            except sonarr.ApiException as e:
                module.fail_json('Error deleting download client: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting download client: {}'.format(to_native(e)), **result)
            result['id'] = 0
    module.exit_json(**result)


def run_module():
    global client
    global module
    global field_helper

    # Init helper.
    field_helper = FieldHelper()

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )

    # Init client and result.
    client = sonarr.DownloadClientApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_download_client(module.params['name'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_download_client(result)

    # Set wanted resource.
    want = sonarr.DownloadClientResource(
        name=module.params['name'],
        remove_completed_downloads=module.params['remove_completed_downloads'],
        remove_failed_downloads=module.params['remove_failed_downloads'],
        enable=module.params['enable'],
        priority=module.params['priority'],
        config_contract=module.params['config_contract'],
        implementation=module.params['implementation'],
        protocol=module.params['protocol'],
        tags=module.params['tags'],
        fields=field_helper.populate_fields(module.params['fields']),
    )

    # Create a new resource, if needed.
    if result['id'] == 0:
        create_download_client(want, result)

    # Update an existing resource.
    want.id = result['id']
    if is_changed(state, want) or module.params['update_secrets']:
        update_download_client(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
