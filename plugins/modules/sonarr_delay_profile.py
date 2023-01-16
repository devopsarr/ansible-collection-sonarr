#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_delay_profile

short_description: Manages Sonarr delay profile.

version_added: "0.0.3"

description: Manages Sonarr delay profile.

options:
    preferred_protocol:
        description: Preferred protocol.
        required: true
        choices: [ "torrent", "usenet" ]
        type: str
    usenet_delay:
        description: Usenet delay.
        type: int
    torrent_delay:
        description: Torrent delay.
        type: int
    order:
        description: Order.
        type: int
    enable_usenet:
        description: Enable Usenet.
        type: bool
    enable_torrent:
        description: Enable Torrent.
        type: bool
    bypass_if_highest_quality:
        description: Bypass if highest quality flag.
        type: bool
    tags:
        description: Tag list.
        required: true
        type: list
        elements: int
    state:
        description: Create or delete a delay profile.
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
---
# Create a delay profile
- name: Create a delay profile
  devopsarr.sonarr.delay_profile:
    preferred_protocol: torrent
    usenet_delay: 0
    torrent_delay: 0
    order: 100
    enable_usenet: true
    enable_torrent: true
    bypass_if_highest_quality: false
    tags: [1,2]

# Delete a delay profile
- name: Delete a delay_profile
  devopsarr.sonarr.delay_profile:
    preferred_protocol: torrent
    tags: [1,2]
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Tag ID.
    type: int
    returned: always
    sample: 1
preferred_protocol:
    description: Preferred protocol.
    returned: always
    type: str
    sample: 'torrent'
usenet_delay:
    description: Usenet delay.
    returned: always
    type: int
    sample: 0
torrent_delay:
    description: Torrent delay.
    returned: always
    type: int
    sample: 0
order:
    description: Order.
    returned: always
    type: int
    sample: 10
enable_usenet:
    description: Enable Usenet.
    returned: always
    type: bool
    sample: true
enable_torrent:
    description: Enable Torrent.
    returned: always
    type: bool
    sample: true
bypass_if_highest_quality:
    description: Bypass if highest quality flag.
    returned: always
    type: bool
    sample: true
tags:
    description: Tag list.
    type: list
    returned: always
    elements: int
    sample: [1,2]
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
        preferred_protocol=dict(type='str', required=True, choices=['torrent', 'usenet']),
        usenet_delay=dict(type='int'),
        torrent_delay=dict(type='int'),
        order=dict(type='int'),
        enable_usenet=dict(type='bool'),
        enable_torrent=dict(type='bool'),
        bypass_if_highest_quality=dict(type='bool'),
        tags=dict(type='list', elements='int', required=True),
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

    client = sonarr.DelayProfileApi(module.api)

    delay_profiles = client.list_delay_profile()

    for profile in delay_profiles:
        if profile['tags'] == module.params['tags']:
            result.update(profile)
            state = profile

    want = sonarr.DelayProfileResource(**{
        'enable_usenet': module.params['enable_usenet'],
        'enable_torrent': module.params['enable_torrent'],
        'preferred_protocol': module.params['preferred_protocol'],
        'usenet_delay': module.params['usenet_delay'],
        'torrent_delay': module.params['torrent_delay'],
        'bypass_if_highest_quality': module.params['bypass_if_highest_quality'],
        'order': module.params['order'],
        'tags': module.params['tags'],
    })

    if module.params['state'] == 'present' and result['id'] == 0:
        result['changed'] = True

        if not module.check_mode:
            response = client.create_delay_profile(delay_profile_resource=want)
            result.update(response)
    elif module.params['state'] == 'present':
        want.id = result['id']
        if want != state:
            result['changed'] = True
            if not module.check_mode:
                response = client.update_delay_profile(delay_profile_resource=want, id=str(want.id))

                result.update(response)

    elif module.params['state'] == 'absent' and result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            response = client.delete_delay_profile(result['id'])
            result['id'] = 0

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()