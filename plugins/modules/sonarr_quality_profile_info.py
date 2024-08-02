#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_quality_profile_info

short_description: Get information about Sonarr quality profile.

version_added: "0.5.0"

description: Get information about Sonarr quality profile.

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
# Gather information about all quality profiles.
- name: Gather information about all quality profiles
  devopsarr.sonarr.sonarr_quality_profile_info:

# Gather information about a single quality profile.
- name: Gather information about a single quality profile
  devopsarr.sonarr.sonarr_quality_profile_info:
    name: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
quality_profiles:
    description: A list of quality profiles.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: Quality Profile ID.
            type: int
            returned: always
            sample: 1
        name:
            description: Name.
            returned: always
            type: str
            sample: Example
        upgrade_allowed:
            description: Upgrade allowed flag.
            returned: always
            type: bool
            sample: false
        cutoff:
            description: Quality ID to which cutoff.
            returned: always
            type: int
            sample: 1
        cutoff_format_score:
            description: Cutoff format score.
            returned: always
            type: int
            sample: 0
        min_format_score:
            description: Min format score.
            returned: always
            type: int
            sample: 0
        quality_groups:
            description: Quality groups
            returned: always
            type: list
            elements: dict
            sample: []
        formats:
            description: Format items list.
            returned: always
            type: list
            elements: dict
            sample: []
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


def list_quality_profile(result):
    try:
        return client.list_quality_profile()
    except sonarr.ApiException as e:
        module.fail_json('Error listing quality profiles: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing quality profiles: {}'.format(to_native(e)), **result)


def populate_quality_profiles(result):
    profiles = []
    # Check if a resource is present already.
    for profile in list_quality_profile(result):
        if module.params['name']:
            if profile.name == module.params['name']:
                profiles = [profile.model_dump(by_alias=False)]
        else:
            profiles.append(profile.model_dump(by_alias=False))
    return profiles


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = sonarr.QualityProfileApi(module.api)
    result = dict(
        changed=False,
        quality_profiles=[],
    )

    # List resources.
    result.update(quality_profiles=populate_quality_profiles(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
