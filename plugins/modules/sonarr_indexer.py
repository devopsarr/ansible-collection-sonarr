#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_indexer

short_description: Manages Sonarr indexer.

version_added: "0.5.0"

description: Manages Sonarr indexer.

options:
    name:
        description: Name.
        required: true
        type: str
    enable_automatic_search:
        description: Enable automatic search flag.
        type: bool
    enable_interactive_search:
        description: Enable interactive search flag.
        type: bool
    enable_rss:
        description: Enable RSS flag.
        type: bool
    priority:
        description: Priority.
        type: int
    download_client_id:
        description: Download client ID.
        type: int
        default: 0
    config_contract:
        description: Config contract.
        type: str
    implementation:
        description: Implementation.
        type: str
    protocol:
        description: Protocol.
        choices: [ "torrent", "usenet" ]
        type: str
    update_secrets:
        description: Flag to force update of secret fields.
        type: bool
        default: false
    anime_standard_format_search:
        description: Anime standard format search.
        type: bool
    allow_zero_size:
        description: Allow zero size.
        type: bool
    ranked_only:
        description: Ranked only.
        type: bool
    api_key:
        description: API key.
        type: str
    additional_parameters:
        description: Additional parameters.
        type: str
    api_path:
        description: API path.
        type: str
    base_url:
        description: Base URL.
        type: str
    captcha_token:
        description: Captcha token.
        type: str
    cookie:
        description: Cookie.
        type: str
    passkey:
        description: Passkey.
        type: str
    username:
        description: Username.
        type: str
    seed_ratio:
        description: Seed ratio.
        type: float
    delay:
        description: Delay.
        type: int
    seed_time:
        description: Seed time.
        type: int
    minimum_seeders:
        description: Minimum seeders.
        type: int
    season_pack_seed_time:
        description: Season pack seed time.
        type: int
    categories:
        description: Categories.
        type: list
        elements: int
    anime_categories:
        description: Anime categories.
        type: list
        elements: int
    tags:
        description: Tag list.
        type: list
        elements: int
        default: []
    state:
        description: Create or delete a indexer.
        required: false
        default: 'present'
        choices: [ "present", "absent" ]
        type: str

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a indexer
- name: Create a indexer
  devopsarr.sonarr.indexer:
    name: "Example"
    enable_automatic_search: false
    enable_interactive_search: false
    enable_rss: false
    priority: 10
    config_contract: "FanzubSettings"
    implementation: "Fanzub"
    protocol: "usenet"
    anime_standard_format_search: true
    base_url: "http://fanzub.com/rss/"
    tags: [1,2]

# Delete a indexer
- name: Delete a indexer
  devopsarr.sonarr.indexer:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
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
from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_field_utils import FieldHelper
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def changed(want, status):
    # type: (sonarr.IndexerResource,sonarr.IndexerResource) -> bool
    if (want.name != status.name or
            want.enable_automatic_search != status.enable_automatic_search or
            want.enable_interactive_search != status.enable_interactive_search or
            want.enable_rss != status.enable_rss or
            want.priority != status.priority or
            want.download_client_id != status.download_client_id or
            want.config_contract != status.config_contract or
            want.implementation != status.implementation or
            want.protocol != status.protocol or
            want.tags != status.tags):
        return True

    for status_field in status.fields:
        for want_field in want.fields:
            if want_field.name == status_field.name and want_field.value != status_field.value and status_field.value != "********":
                return True
    return False


indexer_fields = [
    'anime_standard_format_search',
    'allow_zero_size',
    'ranked_only',
    'api_key',
    'additional_parameters',
    'api_path',
    'base_url',
    'captcha_token',
    'cookie',
    'passkey',
    'username',
    'seed_ratio',
    'delay',
    'seed_time',
    'minimum_seeders',
    'season_pack_seed_time',
    'categories',
    'anime_categories',
]


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        enable_automatic_search=dict(type='bool'),
        enable_interactive_search=dict(type='bool'),
        enable_rss=dict(type='bool'),
        priority=dict(type='int'),
        download_client_id=dict(type='int', default=0),
        config_contract=dict(type='str'),
        implementation=dict(type='str'),
        protocol=dict(type='str', choices=['usenet', 'torrent']),
        tags=dict(type='list', elements='int', default=[]),
        state=dict(default='present', type='str', choices=['present', 'absent']),
        # Needed to manage obfuscate response from api "********"
        update_secrets=dict(type='bool', default=False),
        # Field values
        anime_standard_format_search=dict(type='bool'),
        allow_zero_size=dict(type='bool'),
        ranked_only=dict(type='bool'),
        api_key=dict(type='str', no_log=True),
        additional_parameters=dict(type='str'),
        api_path=dict(type='str'),
        base_url=dict(type='str'),
        captcha_token=dict(type='str', no_log=True),
        cookie=dict(type='str'),
        passkey=dict(type='str', no_log=True),
        username=dict(type='str'),
        seed_ratio=dict(type='float'),
        delay=dict(type='int'),
        seed_time=dict(type='int'),
        minimum_seeders=dict(type='int'),
        season_pack_seed_time=dict(type='int'),
        categories=dict(type='list', elements='int'),
        anime_categories=dict(type='list', elements='int'),
    )

    result = dict(
        changed=False,
        id=0,
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    client = sonarr.IndexerApi(module.api)

    # List resources.
    try:
        indexers = client.list_indexer()
    except Exception as e:
        module.fail_json('Error listing indexers: %s' % to_native(e.reason), **result)

    # Check if a resource is present already.
    for indexer in indexers:
        if indexer['name'] == module.params['name']:
            result.update(indexer.dict(by_alias=False))
            state = indexer

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        if result['id'] != 0:
            result['changed'] = True
            if not module.check_mode:
                try:
                    response = client.delete_indexer(result['id'])
                except Exception as e:
                    module.fail_json('Error deleting indexer: %s' % to_native(e.reason), **result)
                result['id'] = 0
        module.exit_json(**result)

    field_helper = FieldHelper(fields=indexer_fields)
    want = sonarr.IndexerResource(**{
        'name': module.params['name'],
        'enable_automatic_search': module.params['enable_automatic_search'],
        'enable_interactive_search': module.params['enable_interactive_search'],
        'enable_rss': module.params['enable_rss'],
        'priority': module.params['priority'],
        'download_client_id': module.params['download_client_id'],
        'config_contract': module.params['config_contract'],
        'implementation': module.params['implementation'],
        'protocol': module.params['protocol'],
        'tags': module.params['tags'],
        'fields': field_helper.populate_fields(module),
    })

    # Create a new resource.
    if result['id'] == 0:
        result['changed'] = True
        # Only without check mode.
        if not module.check_mode:
            try:
                response = client.create_indexer(indexer_resource=want)
            except Exception as e:
                module.fail_json('Error creating indexer: %s' % to_native(e.reason), **result)
            result.update(response.dict(by_alias=False))
        module.exit_json(**result)

    # Update an existing resource.
    want.id = result['id']
    if changed(want, state) or module.params['update_secrets']:
        result['changed'] = True
        if not module.check_mode:
            try:
                response = client.update_indexer(indexer_resource=want, id=str(want.id))
            except Exception as e:
                module.fail_json('Error updating indexer: %s' % to_native(e.reason), **result)
        result.update(response.dict(by_alias=False))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
