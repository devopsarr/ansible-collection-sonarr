#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_metadata_info

short_description: Get information about Sonarr metadata.

version_added: "1.0.0"

description: Get information about Sonarr metadata.

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
# Gather information about all metadatas.
- name: Gather information about all metadatas
  devopsarr.sonarr.sonarr_metadata_info:

# Gather information about a single metadata.
- name: Gather information about a single metadata
  devopsarr.sonarr.sonarr_metadata_info:
    name: test
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
metadatas:
    description: A list of metadatas.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: metadata ID.
            type: int
            returned: always
            sample: 1
        name:
            description: Name.
            returned: always
            type: str
            sample: "Example"
        enable:
            description: On grab flag.
            returned: always
            type: bool
            sample: true
        config_contract:
            description: Config contract.
            returned: always
            type: str
            sample: "WebhookSettings"
        implementation:
            description: Implementation.
            returned: always
            type: str
            sample: "Webhook"
        tags:
            description: Tag list.
            type: list
            returned: always
            elements: int
            sample: [1,2]
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


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str'),
    )

    result = dict(
        changed=False,
        metadatas=[],
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    client = sonarr.MetadataApi(module.api)

    # List resources.
    try:
        metadata_list = client.list_metadata()
    except Exception as e:
        module.fail_json('Error listing metadatas: %s' % to_native(e.reason), **result)

    metadatas = []
    # Check if a resource is present already.
    for metadata in metadata_list:
        if module.params['name']:
            if metadata['name'] == module.params['name']:
                metadatas = [metadata.dict(by_alias=False)]
        else:
            metadatas.append(metadata.dict(by_alias=False))

    result.update(metadatas=metadatas)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
