#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_auto_tag

short_description: Manages Sonarr auto tag.

version_added: "1.0.0"

description: Manages Sonarr auto tag.

options:
    name:
        description: Name.
        required: true
        type: str
    remove_tags_automatically:
        description: Remove tags automatically flag.
        type: bool
    specifications:
        description: Specification list.
        type: list
        elements: dict
        suboptions:
            negate:
                description: Negate flag.
                type: bool
            required:
                description: Required flag.
                type: bool
            name:
                description: Specification name.
                type: str
            implementation:
                description: Implementation.
                type: str
            fields:
                description: Configuration field list.
                type: list
                elements: dict
                suboptions:
                    name:
                        description: Field name.
                        type: str
                    value:
                        description: Field value.
                        type: raw

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials
    - devopsarr.sonarr.sonarr_state
    - devopsarr.sonarr.sonarr_taggable

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a auto tag
- name: Create a auto tag
  devopsarr.sonarr.sonarr_auto_tag:
    remove_tags_automatically: false
    name: "Type"
    tags: [1]
    specifications:
    - name: "anime"
      implementation: "SeriesTypeSpecification"
      negate: false
      required: true
      fields:
      - name: "value"
        value: 2

# Delete a auto tag
- name: Delete a auto tag
  devopsarr.sonarr.sonarr_auto_tag:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: auto tagID.
    type: int
    returned: always
    sample: 1
name:
    description: Name.
    returned: always
    type: str
    sample: "Example"
remove_tags_automatically:
    description: Remove tags automatically flag.
    returned: always
    type: bool
    sample: false
specifications:
    description: specification list.
    type: list
    returned: always
tags:
    description: Tag list.
    type: list
    returned: always
    elements: int
    sample: [1,2]
'''

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule
from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_specification_utils import SpecificationHelper
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def is_changed(status, want):
    if (want.name != status.name or
            want.tags != status.tags or
            want.remove_tags_automatically != status.remove_tags_automatically):
        return True

    for status_spec in status.specifications:
        for want_spec in want.specifications:
            if want_spec.name == status_spec.name and (
                    want_spec.implementation != status_spec.implementation or
                    want_spec.required != status_spec.required or
                    want_spec.negate != status_spec.negate):
                return True

            for status_field in status_spec.fields:
                for want_field in want_spec.fields:
                    if want_field.name == status_field.name and want_field.value != status_field.value:
                        return True
    return False


def run_module():
    specification_helper = SpecificationHelper()

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        remove_tags_automatically=dict(type='bool'),
        tags=dict(type='list', elements='int', default=[]),
        specifications=dict(type='list', elements='dict', options=specification_helper.specification_args),
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

    client = sonarr.AutoTaggingApi(module.api)

    # list resources.
    try:
        tags = client.list_auto_tagging()
    except Exception as e:
        module.fail_json('Error listing auto tags: %s' % to_native(e.reason), **result)

    state = sonarr.AutoTaggingResource()
    # Check if a resource is present already.
    for auto_tag in tags:
        if auto_tag['name'] == module.params['name']:
            result.update(auto_tag.dict(by_alias=False))
            state = auto_tag

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        if result['id'] != 0:
            result['changed'] = True
            if not module.check_mode:
                try:
                    response = client.delete_auto_tagging(result['id'])
                except Exception as e:
                    module.fail_json('Error deleting auto tag: %s' % to_native(e.reason), **result)
                result['id'] = 0
        module.exit_json(**result)

    want = sonarr.AutoTaggingResource(**{
        'name': module.params['name'],
        'remove_tags_automatically': module.params['remove_tags_automatically'],
        'tags': module.params['tags'],
        'specifications': specification_helper.populate_specifications(module.params['specifications'], 'auto_tag'),
    })

    # Create a new resource.
    if result['id'] == 0:
        result['changed'] = True
        # Only without check mode.
        if not module.check_mode:
            try:
                response = client.create_auto_tagging(auto_tagging_resource=want)
            except Exception as e:
                module.fail_json('Error creating auto tag: %s' % to_native(e.reason), **result)
            result.update(response.dict(by_alias=False))
        module.exit_json(**result)

    # Update an existing resource.
    want.id = result['id']
    if is_changed(state, want):
        result['changed'] = True
        if not module.check_mode:
            try:
                response = client.update_auto_tagging(auto_tagging_resource=want, id=str(want.id))
            except Exception as e:
                module.fail_json('Error updating auto tag: %s' % to_native(e), **result)
        result.update(response.dict(by_alias=False))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
