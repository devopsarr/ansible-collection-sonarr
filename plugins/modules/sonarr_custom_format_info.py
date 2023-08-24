#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_custom_format_info

short_description: Get information about Sonarr custom format.

version_added: "1.0.0"

description: Get information about Sonarr custom format.

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
# Gather information about all custom formats
- name: Gather information about all custom formats
  devopsarr.sonarr.sonarr_custom_format_info:

# Gather information about a single custom format
- name: Gather information about a single custom format
  devopsarr.sonarr.sonarr_custom_format_info:
    name: Example
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
custom_formats:
    description: A list of custom format.
    returned: always
    type: list
    elements: dict
    contains:
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


def run_module():
    specification_helper = SpecificationHelper()

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str'),
    )

    result = dict(
        changed=False,
        custom_formats=[],
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

    custom_formats = []
    # Check if a resource is present already.
    for custom_format in formats:
        if module.params['name']:
            if custom_format['name'] == module.params['name']:
                custom_formats = [custom_format.dict(by_alias=False)]
        else:
            custom_formats.append(custom_format.dict(by_alias=False))

    result.update(custom_formats=custom_formats)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
