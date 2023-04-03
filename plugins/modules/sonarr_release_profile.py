#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_release_profile

short_description: Manages Sonarr release profile.

version_added: "0.0.3"

description: Manages Sonarr release profile.

options:
    name:
        description: Name.
        required: true
        type: str
    ignored:
        description: Ignored terms. At least one of `required` and `ignored` must be set.
        type: list
        elements: str
    required:
        description: Required terms. At least one of `required` and `ignored` must be set.
        type: list
        elements: str
    indexer_id:
        description: Indexer ID. Set `0` for all.
        type: int
        default: 0
    enabled:
        description: Enabled.
        type: bool
    tags:
        description: Tag list.
        type: list
        elements: int
        default: []
    state:
        description: Create or delete a release profile.
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
# Create a release profile
- name: Create a release profile
  devopsarr.sonarr.release_profile:
    enabled: true
    name: "Example"
    required: ["proper"]
    ignored: ["repack"]
    indexer_id: 1
    tags: [1,2]

# Delete a release profile
- name: Delete a release_profile
  devopsarr.sonarr.release_profile:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
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
        name=dict(type='str', required=True),
        ignored=dict(type='list', elements='str'),
        required=dict(type='list', elements='str'),
        indexer_id=dict(type='int', default=0),
        enabled=dict(type='bool'),
        tags=dict(type='list', elements='int', default=[]),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )

    result = dict(
        changed=False,
        id=0,
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

    # Check if a resource is present already.
    for profile in release_profiles:
        if profile['name'] == module.params['name']:
            result.update(profile.dict(by_alias=False))
            state = profile

    want = sonarr.ReleaseProfileResource(**{
        'name': module.params['name'],
        'enabled': module.params['enabled'],
        'required': module.params['required'],
        'ignored': module.params['ignored'],
        'indexer_id': module.params['indexer_id'],
        'tags': module.params['tags'],
    })

    # Create a new resource.
    if module.params['state'] == 'present' and result['id'] == 0:
        result['changed'] = True
        # Only without check mode.
        if not module.check_mode:
            try:
                response = client.create_release_profile(release_profile_resource=want)
            except Exception as e:
                module.fail_json('Error creating release profile: %s' % to_native(e.reason), **result)
            result.update(response.dict(by_alias=False))

    # Update an existing resource.
    elif module.params['state'] == 'present':
        want.id = result['id']
        if want != state:
            result['changed'] = True
            if not module.check_mode:
                try:
                    response = client.update_release_profile(release_profile_resource=want, id=str(want.id))
                except Exception as e:
                    module.fail_json('Error updating release profile: %s' % to_native(e.reason), **result)
            result.update(response.dict(by_alias=False))

    # Delete the resource.
    elif module.params['state'] == 'absent' and result['id'] != 0:
        result['changed'] = True
        if not module.check_mode:
            try:
                response = client.delete_release_profile(result['id'])
            except Exception as e:
                module.fail_json('Error deleting release profile: %s' % to_native(e.reason), **result)
            result['id'] = 0

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
