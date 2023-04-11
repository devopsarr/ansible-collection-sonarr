#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_indexer_config

short_description: Manages Sonarr indexer config.

version_added: "0.5.0"

description: Manages Sonarr indexer config.

options:
    maximum_size:
        description: Maximum size.
        required: true
        type: int
    minimum_age:
        description: Minimum age.
        required: true
        type: int
    retention:
        description: Retention.
        required: true
        type: int
    rss_sync_interval:
        description: RSS sync interval.
        required: true
        type: int

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update indexer config
- name: Update indexer config
  devopsarr.sonarr.sonarr_indexer_config:
    maximum_size: 0
    minimum_age: 0
    retention: 0
    rss_sync_interval: 50
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Indexer config ID.
    type: int
    returned: always
    sample: '1'
maximum_size:
    description: Maximum size.
    returned: always
    type: int
    sample: '0'
minimum_age:
    description: Minimum age.
    returned: always
    type: int
    sample: '0'
retention:
    description: Retention.
    returned: always
    type: int
    sample: '0'
rss_sync_interval:
    description: RSS sync interval.
    returned: always
    type: int
    sample: '100'
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
        maximum_size=dict(type='int', required=True),
        minimum_age=dict(type='int', required=True),
        retention=dict(type='int', required=True),
        rss_sync_interval=dict(type='int', required=True),
    )

    result = dict(
        changed=False,
        id=0,
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    client = sonarr.IndexerConfigApi(module.api)

    # Get resource.
    try:
        indexer_config = client.get_indexer_config()
    except Exception as e:
        module.fail_json('Error getting indexer config: %s' % to_native(e.reason), **result)

    result.update(indexer_config.dict(by_alias=False))

    want = sonarr.IndexerConfigResource(**{
        'maximum_size': module.params['maximum_size'],
        'minimum_age': module.params['minimum_age'],
        'retention': module.params['retention'],
        'rss_sync_interval': module.params['rss_sync_interval'],
        'id': 1,
    })

    # Update an existing resource.
    if want != indexer_config:
        result['changed'] = True
        if not module.check_mode:
            try:
                response = client.update_indexer_config(indexer_config_resource=want, id=str(want.id))
            except Exception as e:
                module.fail_json('Error updating indexer config: %s' % to_native(e.reason), **result)
        result.update(response.dict(by_alias=False))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
