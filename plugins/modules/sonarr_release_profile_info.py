#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_release_profile_info

short_description: Get information about Sonarr release profile.

version_added: "0.0.3"

description: Get information about Sonarr release profile.

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
# Gather information about all release profiles.
- name: Gather information about all release profiles
  devopsarr.sonarr.sonarr_release_profile_info:

# Gather information about a single release profile.
- name: Gather information about a single release profile
  devopsarr.sonarr.sonarr_release_profile_info:
    name: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
release_profiles:
    description: A list of release profiles.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: Release Profile ID.
            type: int
            returned: always
            sample: 1
        ignored:
            description: Ignored terms. At least one of `required` and `ignored` must be set.
            type: list
            elements: str
            returned: always
            sample: ["proper", "repack"]
        required:
            description: Required terms. At least one of `required` and `ignored` must be set.
            type: list
            elements: str
            returned: always
            sample: ["proper", "repack"]
        indexer_id:
            description: Indexer ID. Set `0` for all."
            type: int
            returned: always
            sample: 1
        enabled:
            description: Enabled.
            type: bool
            returned: always
            sample: True
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
        name=dict(type='str'),
    )

    result = dict(
        changed=False,
        release_profiles=[],
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    client = sonarr.ReleaseProfileApi(module.api)

    # List resources.
    try:
        release_profiles = client.list_release_profile()
    except Exception as e:
        module.fail_json('Error listing release profiles: %s' % to_native(e.reason), **result)

    profiles = []
    # Check if a resource is present already.
    for profile in release_profiles:
        if module.params['name']:
            if profile['name'] == module.params['name']:
                profiles = [profile.dict(by_alias=False)]
        else:
            profiles.append(profile.dict(by_alias=False))

    result.update(release_profiles=profiles)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
