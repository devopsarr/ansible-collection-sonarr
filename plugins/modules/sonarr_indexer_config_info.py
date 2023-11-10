#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_indexer_config_info

short_description: Get information about Sonarr indexer config.

version_added: "0.5.0"

description: Get information about Sonarr indexer config.

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch indexer config
- name: fetch indexer config
  devopsarr.sonarr.sonarr_indexer_config_info:
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


def get_indexer_config(result):
    try:
        return client.get_indexer_config()
    except Exception as e:
        module.fail_json('Error getting indexer config: %s' % to_native(e.reason), **result)


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec={},
        supports_check_mode=True,
    )
    # Init client and result.
    client = sonarr.IndexerConfigApi(module.api)
    result = dict(
        changed=False,
    )

    # Get resource.
    result.update(get_indexer_config(result).dict(by_alias=False))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
