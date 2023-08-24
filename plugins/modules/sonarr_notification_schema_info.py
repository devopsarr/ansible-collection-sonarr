#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_notification_schema_info

short_description: Get information about Sonarr notification schema.

version_added: "1.0.0"

description: Get information about Sonarr notification schema.

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
# Gather information about all notifications schema.
- name: Gather information about all notifications schema
  devopsarr.sonarr.sonarr_notification_schema_info:

# Gather information about a single notification schema.
- name: Gather information about a single notification schema
  devopsarr.sonarr.sonarr_notification_schema_info:
    name: BroadcastheNet
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
notifications:
    description: A list of notifications schema.
    returned: always
    type: list
    elements: dict
    contains:
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
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str'),
    )

    result = dict(
        changed=False,
        notifications=[],
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    client = sonarr.NotificationApi(module.api)

    # List resources.
    try:
        notification_list = client.list_notification_schema()
    except Exception as e:
        module.fail_json('Error listing notification schemas: %s' % to_native(e.reason), **result)

    notifications = []
    # Check if a resource is present already.
    for notification in notification_list:
        if module.params['name']:
            if notification['implementation'] == module.params['name']:
                notifications = [notification.dict(by_alias=False)]
        else:
            notifications.append(notification.dict(by_alias=False))

    result.update(notifications=notifications)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
