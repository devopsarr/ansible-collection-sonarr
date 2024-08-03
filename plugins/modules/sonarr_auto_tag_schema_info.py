#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_auto_tag_schema_info

short_description: Get information about Sonarr auto tag schema.

version_added: "1.0.0"

description: Get information about Sonarr auto tag schema.

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
# Gather information about all auto tags schema.
- name: Gather information about all auto tags schema
  devopsarr.sonarr.sonarr_auto_tag_schema_info:

# Gather information about a single auto tag schema.
- name: Gather information about a single auto tag schema
  devopsarr.sonarr.sonarr_auto_tag_schema_info:
    name: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
auto_tags:
    description: A list of auto tag.
    returned: always
    type: list
    elements: dict
    contains:
        config_contract:
            description: Config contract.
            returned: always
            type: str
            sample: "BroadcastheNetSettings"
        implementation:
            description: Implementation.
            returned: always
            type: str
            sample: "BroadcastheNet"
        fields:
            description: field list.
            type: list
            returned: always
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


def list_auto_tag_schema(result):
    try:
        return client.list_auto_tagging_schema()
    except sonarr.ApiException as e:
        module.fail_json('Error listing auto tags: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing auto tags: {}'.format(to_native(e)), **result)


def populate_auto_tag_schema(result):
    auto_tags = []
    # Check if a resource is present already.
    for auto_tag in list_auto_tag_schema(result):
        if module.params['name']:
            if auto_tag.implementation == module.params['name']:
                auto_tags = [auto_tag.model_dump(by_alias=False)]
        else:
            auto_tags.append(auto_tag.model_dump(by_alias=False))
    return auto_tags


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = sonarr.AutoTaggingApi(module.api)
    result = dict(
        changed=False,
        auto_tags=[],
    )

    # List resources.
    result.update(auto_tags=populate_auto_tag_schema(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
