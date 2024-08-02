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
---
# Gather information about all tags.
- name: Gather information about all tags
  devopsarr.sonarr.sonarr_tag_info:

# Gather information about a single tag.
- name: Gather information about a single tag
  devopsarr.sonarr.sonarr_tag_info:
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


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        label=dict(type='str'),
    )


def list_tags(result):
    try:
        return client.list_tag()
    except sonarr.ApiException as e:
        module.fail_json('Error listing tags: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing tags: {}'.format(to_native(e)), **result)


def populate_tags(result):
    tags = []
    for tag in list_tags(result):
        if module.params['label']:
            if tag.label == module.params['label']:
                tags = [tag.model_dump(by_alias=False)]
        else:
            tags.append(tag.model_dump(by_alias=False))
    return tags


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = sonarr.TagApi(module.api)
    result = dict(
        changed=False,
        tags=[],
    )

    # List resources.
    result.update(tags=populate_tags(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
