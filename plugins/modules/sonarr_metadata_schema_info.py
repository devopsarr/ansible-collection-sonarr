#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_metadata_schema_info

short_description: Get information about Sonarr metadata schema.

version_added: "1.0.0"

description: Get information about Sonarr metadata schema.

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
# Gather information about all metadatas schema.
- name: Gather information about all metadatas schema
  devopsarr.sonarr.sonarr_metadata_schema_info:

# Gather information about a single metadata schema.
- name: Gather information about a single metadata schema
  devopsarr.sonarr.sonarr_metadata_schema_info:
    name: BroadcastheNet
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
metadatas:
    description: A list of metadatas schema.
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


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        name=dict(type='str'),
    )


def list_metadata_schema(result):
    try:
        return client.list_metadata_schema()
    except sonarr.ApiException as e:
        module.fail_json('Error listing metadata schemas: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing metadata schemas: {}'.format(to_native(e)), **result)


def populate_metadata_schema(result):
    metadatas = []
    # Check if a resource is present already.
    for metadata in list_metadata_schema(result):
        if module.params['name']:
            if metadata.implementation == module.params['name']:
                metadatas = [metadata.model_dump(by_alias=False)]
        else:
            metadatas.append(metadata.model_dump(by_alias=False))
    return metadatas


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = sonarr.MetadataApi(module.api)
    result = dict(
        changed=False,
        metadatas=[],
    )

    # List resources.
    result.update(metadatas=populate_metadata_schema(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
