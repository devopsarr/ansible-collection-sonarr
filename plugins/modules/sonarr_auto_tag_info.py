#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_auto_tag_info

short_description: Get information about Sonarr auto tag.

version_added: "1.0.0"

description: Get information about Sonarr auto tag.

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
# Gather information about all auto tags
- name: Gather information about all auto tags
  devopsarr.sonarr.sonarr_auto_tag_info:

# Gather information about a single auto tag
- name: Gather information about a single auto tag
  devopsarr.sonarr.sonarr_auto_tag_info:
    name: Example
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
auto_tags:
    description: A list of auto tag.
    returned: always
    type: list
    elements: dict
    contains:
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
            description: Include auto tag when renaming flag.
            returned: always
            type: bool
            sample: false
        tags:
            description: Tag list.
            type: list
            returned: always
            elements: int
            sample: [1,2]
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
        auto_tags=[],
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

    auto_tags = []
    # Check if a resource is present already.
    for auto_tag in tags:
        if module.params['name']:
            if auto_tag['name'] == module.params['name']:
                auto_tags = [auto_tag.dict(by_alias=False)]
        else:
            auto_tags.append(auto_tag.dict(by_alias=False))

    result.update(auto_tags=auto_tags)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
