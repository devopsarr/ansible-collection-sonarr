#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_tag_info

short_description: Get information about Sonarr tag.

version_added: "0.5.0"

description: Get information about Sonarr tag.

options:
    label:
        description: Actual tag.
        type: str

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
# Gather information about all tags.
- name: Gather information about all tags
  devopsarr.sonarr.tag_info:

# Gather information about a single tag.
- name: Gather information about all tags
  devopsarr.sonarr.tag_info:
    label: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
tags:
    description: A list of tags.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: Tag ID.
            type: int
            returned: always
            sample: '1'
        label:
            description: The output message that the test module generates.
            type: str
            returned: 'on create/update'
            sample: 'hd'
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
        label=dict(type='str'),
    )

    result = dict(
        changed=False,
        tags=[]
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    client = sonarr.TagApi(module.api)

    # List resources.
    try:
        response = client.list_tag()
    except Exception as e:
        module.fail_json('Error listing tags: %s' % to_native(e.reason), **result)

    tags = []
    for tag in response:
        if module.params['label']:
            if tag['label'] == module.params['label']:
                tags = [tag.dict(by_alias=False)]
        else:
            tags.append(tag.dict(by_alias=False))

    result.update(tags=tags)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
