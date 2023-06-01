#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_import_list_exclusion

short_description: Manages Sonarr import list exclusion.

version_added: "0.7.0"

description: Manages Sonarr import list exclusion.

options:
    tvdb_id:
        description: TVDB ID.
        required: true
        type: int
    title:
        description: Title.
        required: true
        type: str
    state:
        description: Create or delete a import_list_exclusion.
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
# Create a import list exclusion
- name: Create a import list exclusion
  devopsarr.sonarr.sonarr_import_list_exclusion:
    tvdb_id: 123
    title: 'example'


# Delete a import list exclusion
- name: Delete a import_list_exclusion
  devopsarr.sonarr.sonarr_import_list_exclusion:
    tvdb_id: 123
    title: 'example'
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: import list exclusion ID.
    type: int
    returned: always
    sample: 1
tvdb_id:
    description: TVDB ID.
    type: int
    returned: 'always'
    sample: 12345
title:
    description: Title.
    type: str
    returned: 'always'
    sample: 'Breaking Bad'
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
        tvdb_id=dict(type='int', required=True),
        title=dict(type='str', required=True),
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

    client = sonarr.ImportListExclusionApi(module.api)

    # List resources.
    try:
        import_list_exclusions = client.list_import_list_exclusion()
    except Exception as e:
        module.fail_json('Error listing import list exclusions: %s' % to_native(e.reason), **result)

    # Check if a resource is present already.
    for import_list_exclusion in import_list_exclusions:
        if import_list_exclusion['tvdb_id'] == module.params['tvdb_id'] and \
           import_list_exclusion['title'] == module.params['title']:
            result.update(import_list_exclusion.dict(by_alias=False))

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        if result['id'] != 0:
            result['changed'] = True
            # Only without check mode.
            if not module.check_mode:
                try:
                    response = client.delete_import_list_exclusion(result['id'])
                except Exception as e:
                    module.fail_json('Error deleting import list exclusion: %s' % to_native(e.reason), **result)
                result['id'] = 0
        module.exit_json(**result)

    want = sonarr.ImportListExclusionResource(**{
        'tvdb_id': module.params['tvdb_id'],
        'title': module.params['title'],
    })

    # Create a new resource.
    if result['id'] == 0:
        result['changed'] = True
        # Only without check mode.
        if not module.check_mode:
            try:
                response = client.create_import_list_exclusion(import_list_exclusion_resource=want)
            except Exception as e:
                module.fail_json('Error creating import list exclusion: %s' % to_native(e.reason), **result)
            result.update(response.dict(by_alias=False))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
