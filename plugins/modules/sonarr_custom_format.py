#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_custom_format

short_description: Manages Sonarr custom format.

version_added: "1.0.0"

description: Manages Sonarr custom format.

options:
    name:
        description: Name.
        required: true
        type: str
    include_custom_format_when_renaming:
        description: Include custom format when renaming flag.
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

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a custom format
- name: Create a custom format
  devopsarr.sonarr.sonarr_custom_format:
    include_custom_format_when_renaming: false
    name: "Language"
    specifications:
    - name: "arabic"
      implementation: "LanguageSpecification"
      negate: false
      required: true
      fields:
      - name: "value"
        value: 26

# Delete a custom format
- name: Delete a custom format
  devopsarr.sonarr.sonarr_custom_format:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: custom formatID.
    type: int
    returned: always
    sample: 1
name:
    description: Name.
    returned: always
    type: str
    sample: "Example"
include_custom_format_when_renaming:
    description: Include custom format when renaming flag.
    returned: always
    type: bool
    sample: false
specifications:
    description: specification list.
    type: list
    returned: always
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
    # Check if the basic attributes are different
    if (
        want.name != status.name
        or want.include_custom_format_when_renaming != status.include_custom_format_when_renaming
        or len(want.specifications) != len(status.specifications)
    ):
        return True

    # Create a dictionary to store specifications by name for faster lookup
    status_specs = {spec.name: spec for spec in status.specifications}

    # Check if any specification is different
    for want_spec in want.specifications:
        status_spec = status_specs.get(want_spec.name)
        if (
            status_spec is None
            or want_spec.implementation != status_spec.implementation
            or want_spec.required != status_spec.required
            or want_spec.negate != status_spec.negate
        ):
            return True

        # Check if any field within the specification is different
        for want_field in want_spec.fields:
            status_field = next(
                (field for field in status_spec.fields if field.name == want_field.name),
                None,
            )
            if status_field is None or want_field.value != status_field.value:
                return True

    return False


def run_module():
    specification_helper = SpecificationHelper()

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        include_custom_format_when_renaming=dict(type='bool'),
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

    client = sonarr.CustomFormatApi(module.api)

    # list resources.
    try:
        formats = client.list_custom_format()
    except Exception as e:
        module.fail_json('Error listing custom formats: %s' % to_native(e.reason), **result)

    state = sonarr.CustomFormatResource()
    # Check if a resource is present already.
    for custom_format in formats:
        if custom_format['name'] == module.params['name']:
            result.update(custom_format.dict(by_alias=False))
            state = custom_format

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        if result['id'] != 0:
            result['changed'] = True
            if not module.check_mode:
                try:
                    response = client.delete_custom_format(result['id'])
                except Exception as e:
                    module.fail_json('Error deleting custom format: %s' % to_native(e.reason), **result)
                result['id'] = 0
        module.exit_json(**result)

    want = sonarr.CustomFormatResource(**{
        'name': module.params['name'],
        'include_custom_format_when_renaming': module.params['include_custom_format_when_renaming'],
        'specifications': specification_helper.populate_specifications(module.params['specifications'], 'custom_format'),
    })

    # Create a new resource.
    if result['id'] == 0:
        result['changed'] = True
        # Only without check mode.
        if not module.check_mode:
            try:
                response = client.create_custom_format(custom_format_resource=want)
            except Exception as e:
                module.fail_json('Error creating custom format: %s' % to_native(e.reason), **result)
            result.update(response.dict(by_alias=False))
        module.exit_json(**result)

    # Update an existing resource.
    want.id = result['id']
    if is_changed(state, want):
        result['changed'] = True
        if not module.check_mode:
            try:
                response = client.update_custom_format(custom_format_resource=want, id=str(want.id))
            except Exception as e:
                module.fail_json('Error updating custom format: %s' % to_native(e), **result)
        result.update(response.dict(by_alias=False))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
