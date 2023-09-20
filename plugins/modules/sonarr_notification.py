#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_notification

short_description: Manages Sonarr notification.

version_added: "1.0.0"

description: Manages Sonarr notification.

options:
    name:
        description: Name.
        required: true
        type: str
    on_grab:
        description: On grab flag.
        type: bool
        default: false
    on_download:
        description: On download flag.
        type: bool
        default: false
    on_rename:
        description: On rename flag.
        type: bool
        default: false
    on_series_add:
        description: On series add flag.
        type: bool
        default: false
    on_series_delete:
        description: On series delete flag.
        type: bool
        default: false
    on_episode_file_delete:
        description: On episode file delete flag.
        type: bool
        default: false
    on_episode_file_delete_for_upgrade:
        description: On episode file delete for upgrade flag.
        type: bool
        default: false
    on_health_issue:
        description: On health issue flag.
        type: bool
        default: false
    on_health_restored:
        description: On health restored flag.
        type: bool
        default: false
    on_application_update:
        description: On application update flag.
        type: bool
        default: false
    on_manual_interaction_required:
        description: On manual interaction required flag.
        type: bool
        default: false
    on_upgrade:
        description: On upgrade flag.
        type: bool
        default: false
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
# Create a notification
- name: Create a notification
  devopsarr.sonarr.sonarr_notification:
    name: "Example"
    on_grab: true
    config_contract: "WebhookSettings"
    implementation: "Webhook"
    fields:
    - name: "username"
      value: "User"
    - name: "password"
      value: "test"
    - name: "url"
      value: "webhook.lcl"
    - name: "method"
      value: 1
    tags: [1,2]

# Delete a notification
- name: Delete a notification
  devopsarr.sonarr.sonarr_notification:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: notification ID.
    type: int
    returned: always
    sample: 1
name:
    description: Name.
    returned: always
    type: str
    sample: "Example"
on_grab:
    description: On grab flag.
    returned: always
    type: bool
    sample: true
on_download:
    description: On download flag.
    returned: always
    type: bool
    sample: false
on_rename:
    description: On rename flag.
    returned: always
    type: bool
    sample: true
on_series_add:
    description: On series add flag.
    returned: always
    type: bool
    sample: true
on_series_delete:
    description: On series delete flag.
    returned: always
    type: bool
    sample: true
on_episode_file_delete:
    description: On episode file delete flag.
    returned: always
    type: bool
    sample: true
on_episode_file_delete_for_upgrade:
    description: On episode file delete for upgrade flag.
    returned: always
    type: bool
    sample: true
on_health_issue:
    description: On health issue flag.
    returned: always
    type: bool
    sample: true
on_health_restored:
    description: On health restored flag.
    returned: always
    type: bool
    sample: true
on_application_update:
    description: On application update flag.
    returned: always
    type: bool
    sample: true
on_manual_interaction_required:
    description: On manual interaction required flag.
    returned: always
    type: bool
    sample: true
on_upgrade:
    description: On upgrade flag.
    returned: always
    type: bool
    sample: true
config_contract:
    description: Config contract.
    returned: always
    type: str
    sample: "WebhookSettings"
implementation:
    description: Implementation.
    returned: always
    type: str
    sample: "Webhook"
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
            want.on_grab != status.on_grab or
            want.on_download != status.on_download or
            want.on_rename != status.on_rename or
            want.on_series_add != status.on_series_add or
            want.on_series_delete != status.on_series_delete or
            want.on_episode_file_delete != status.on_episode_file_delete or
            want.on_episode_file_delete_for_upgrade != status.on_episode_file_delete_for_upgrade or
            want.on_health_issue != status.on_health_issue or
            want.on_health_restored != status.on_health_restored or
            want.on_manual_interaction_required != status.on_manual_interaction_required or
            want.on_upgrade != status.on_upgrade or
            want.on_application_update != status.on_application_update or
            want.config_contract != status.config_contract or
            want.implementation != status.implementation or
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
        on_grab=dict(type='bool', default=False),
        on_download=dict(type='bool', default=False),
        on_rename=dict(type='bool', default=False),
        on_series_add=dict(type='bool', default=False),
        on_series_delete=dict(type='bool', default=False),
        on_episode_file_delete=dict(type='bool', default=False),
        on_episode_file_delete_for_upgrade=dict(type='bool', default=False),
        on_health_issue=dict(type='bool', default=False),
        on_health_restored=dict(type='bool', default=False),
        on_application_update=dict(type='bool', default=False),
        on_manual_interaction_required=dict(type='bool', default=False),
        on_upgrade=dict(type='bool', default=False),
        config_contract=dict(type='str'),
        implementation=dict(type='str'),
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

    client = sonarr.NotificationApi(module.api)

    # List resources.
    try:
        notifications = client.list_notification()
    except Exception as e:
        module.fail_json('Error listing notifications: %s' % to_native(e.reason), **result)

    state = sonarr.NotificationResource()
    # Check if a resource is present already.
    for notification in notifications:
        if notification['name'] == module.params['name']:
            result.update(notification.dict(by_alias=False))
            state = notification

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        if result['id'] != 0:
            result['changed'] = True
            if not module.check_mode:
                try:
                    response = client.delete_notification(result['id'])
                except Exception as e:
                    module.fail_json('Error deleting notification: %s' % to_native(e.reason), **result)
                result['id'] = 0
        module.exit_json(**result)

    want = sonarr.NotificationResource(**{
        'name': module.params['name'],
        'on_grab': module.params['on_grab'],
        'on_download': module.params['on_download'],
        'on_rename': module.params['on_rename'],
        'on_series_add': module.params['on_series_add'],
        'on_series_delete': module.params['on_series_delete'],
        'on_episode_file_delete': module.params['on_episode_file_delete'],
        'on_episode_file_delete_for_upgrade': module.params['on_episode_file_delete_for_upgrade'],
        'on_health_issue': module.params['on_health_issue'],
        'on_health_restored': module.params['on_health_restored'],
        'on_application_update': module.params['on_application_update'],
        'on_manual_interaction_required': module.params['on_manual_interaction_required'],
        'on_upgrade': module.params['on_upgrade'],
        'config_contract': module.params['config_contract'],
        'implementation': module.params['implementation'],
        'tags': module.params['tags'],
        'fields': field_helper.populate_fields(module.params['fields']),
    })

    # Create a new resource.
    if result['id'] == 0:
        result['changed'] = True
        # Only without check mode.
        if not module.check_mode:
            try:
                response = client.create_notification(notification_resource=want)
            except Exception as e:
                module.fail_json('Error creating notification: %s' % to_native(e.reason), **result)
            result.update(response.dict(by_alias=False))
        module.exit_json(**result)

    # Update an existing resource.
    want.id = result['id']
    if is_changed(state, want) or module.params['update_secrets']:
        result['changed'] = True
        if not module.check_mode:
            try:
                response = client.update_notification(notification_resource=want, id=str(want.id))
            except Exception as e:
                module.fail_json('Error updating notification: %s' % to_native(e.reason), **result)
        result.update(response.dict(by_alias=False))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
