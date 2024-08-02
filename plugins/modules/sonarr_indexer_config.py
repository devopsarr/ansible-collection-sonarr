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


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        maximum_size=dict(type='int', required=True),
        minimum_age=dict(type='int', required=True),
        retention=dict(type='int', required=True),
        rss_sync_interval=dict(type='int', required=True),
    )


def read_indexer_config(result):
    try:
        return client.get_indexer_config()
    except sonarr.ApiException as e:
        module.fail_json('Error getting indexer config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting indexer config: {}'.format(to_native(e)), **result)


def update_indexer_config(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_indexer_config(indexer_config_resource=want, id="1")
        except sonarr.ApiException as e:
            module.fail_json('Error updating indexer config: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating indexer config: {}'.format(to_native(e)), **result)
    # No need to exit module since it will exit by default either way
    result.update(response.model_dump(by_alias=False))


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )

    # Init client and result.
    client = sonarr.IndexerConfigApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Get resource.
    state = read_indexer_config(result)
    if state:
        result.update(state.model_dump(by_alias=False))

    want = sonarr.IndexerConfigResource(
        maximum_size=module.params['maximum_size'],
        minimum_age=module.params['minimum_age'],
        retention=module.params['retention'],
        rss_sync_interval=module.params['rss_sync_interval'],
        id=1,
    )

    # Update an existing resource.
    if want != state:
        update_indexer_config(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
