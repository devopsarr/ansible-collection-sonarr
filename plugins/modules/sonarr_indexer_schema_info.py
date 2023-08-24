#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_indexer_schema_info

short_description: Get information about Sonarr indexer schema.

version_added: "1.0.0"

description: Get information about Sonarr indexer schema.

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
# Gather information about all indexers schema.
- name: Gather information about all indexers schema
  devopsarr.sonarr.sonarr_indexer_schema_info:

# Gather information about a single indexer schema.
- name: Gather information about a single indexer schema
  devopsarr.sonarr.sonarr_indexer_schema_info:
    name: BroadcastheNet
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
indexers:
    description: A list of indexers schema.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: indexer ID.
            type: int
            returned: always
            sample: 1
        name:
            description: Name.
            returned: always
            type: str
            sample: "Example"
        enable_automatic_search:
            description: Enable automatic search flag.
            returned: always
            type: bool
            sample: true
        enable_interactive_search:
            description: Enable interactive search flag.
            returned: always
            type: bool
            sample: false
        enable_rss:
            description: Enable RSS flag.
            returned: always
            type: bool
            sample: true
        priority:
            description: Priority.
            returned: always
            type: int
            sample: 1
        download_client_id:
            description: Download client ID.
            returned: always
            type: int
            sample: 0
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
        protocol:
            description: Protocol.
            returned: always
            type: str
            sample: "torrent"
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
        indexers=[],
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    client = sonarr.IndexerApi(module.api)

    # List resources.
    try:
        indexer_list = client.list_indexer_schema()
    except Exception as e:
        module.fail_json('Error listing indexer schemas: %s' % to_native(e.reason), **result)

    indexers = []
    # Check if a resource is present already.
    for indexer in indexer_list:
        if module.params['name']:
            if indexer['name'] == module.params['name']:
                indexers = [indexer.dict(by_alias=False)]
        else:
            indexers.append(indexer.dict(by_alias=False))

    result.update(indexers=indexers)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
