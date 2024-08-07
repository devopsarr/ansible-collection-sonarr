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
        choices: [ "torrent", "usenet" ]
        type: str
    usenet_delay:
        description: Usenet delay.
        type: int
    torrent_delay:
        description: Torrent delay.
        type: int
    minimum_custom_format_score:
        description: Minimum cutoff format score.
        type: int
        default: 0
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
    bypass_if_above_custom_format_score:
        description: Bypass if above custom format score flag.
        type: bool
    tags:
        description: Tag list.
        required: true
        type: list
        elements: int

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials
    - devopsarr.sonarr.sonarr_state

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a delay profile
- name: Create a delay profile
  devopsarr.sonarr.sonarr_delay_profile:
    preferred_protocol: torrent
    usenet_delay: 0
    torrent_delay: 0
    minimum_custom_format_score: 0
    order: 100
    enable_usenet: true
    enable_torrent: true
    bypass_if_above_custom_format_score: true
    bypass_if_highest_quality: false
    tags: [1,2]

# Delete a delay profile
- name: Delete a delay_profile
  devopsarr.sonarr.sonarr_delay_profile:
    preferred_protocol: torrent
    tags: [1,2]
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Delay Profile ID.
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
minimum_custom_format_score:
    description: Minimum cutoff format score.
    type: int
    returned: always
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
bypass_if_above_custom_format_score:
    description: Bypass if above custom format score flag.
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


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        preferred_protocol=dict(type='str', choices=['torrent', 'usenet']),
        usenet_delay=dict(type='int'),
        torrent_delay=dict(type='int'),
        minimum_custom_format_score=dict(type='int', default=0),
        order=dict(type='int'),
        enable_usenet=dict(type='bool'),
        enable_torrent=dict(type='bool'),
        bypass_if_highest_quality=dict(type='bool'),
        bypass_if_above_custom_format_score=dict(type='bool'),
        tags=dict(type='list', elements='int', required=True),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )


def create_delay_profile(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.create_delay_profile(delay_profile_resource=want)
        except sonarr.ApiException as e:
            module.fail_json('Error creating delay profile: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error creating delay profile: {}'.format(to_native(e)), **result)
        result.update(response.model_dump(by_alias=False))
    module.exit_json(**result)


def list_delay_profiles(result):
    try:
        return client.list_delay_profile()
    except sonarr.ApiException as e:
        module.fail_json('Error listing delay profiles: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing delay profiles: {}'.format(to_native(e)), **result)


def find_delay_profile(tags, result):
    for profile in list_delay_profiles(result):
        if profile.tags == tags:
            return profile
    return None


def update_delay_profile(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_delay_profile(delay_profile_resource=want, id=str(want.id))
        except sonarr.ApiException as e:
            module.fail_json('Error updating delay profile: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating delay profile: {}'.format(to_native(e)), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.model_dump(by_alias=False))


def delete_delay_profile(result):
    if result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                client.delete_delay_profile(result['id'])
            except sonarr.ApiException as e:
                module.fail_json('Error deleting delay profile: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
            except Exception as e:
                module.fail_json('Error deleting delay profile: {}'.format(to_native(e)), **result)
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
    client = sonarr.DelayProfileApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_delay_profile(module.params['tags'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        delete_delay_profile(result)

    # Set wanted resource.
    want = sonarr.DelayProfileResource(
        enable_usenet=module.params['enable_usenet'],
        enable_torrent=module.params['enable_torrent'],
        preferred_protocol=module.params['preferred_protocol'],
        usenet_delay=module.params['usenet_delay'],
        torrent_delay=module.params['torrent_delay'],
        minimum_custom_format_score=module.params['minimum_custom_format_score'],
        bypass_if_highest_quality=module.params['bypass_if_highest_quality'],
        bypass_if_above_custom_format_score=module.params['bypass_if_above_custom_format_score'],
        order=module.params['order'],
        tags=module.params['tags'],
    )

    # Create a new resource if needed.
    if result['id'] == 0:
        create_delay_profile(want, result)

    # Update an existing resource.
    want.id = result['id']
    if want != state:
        update_delay_profile(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
