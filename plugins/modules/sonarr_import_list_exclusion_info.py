#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_import_list_exclusion_info

short_description: Manages Sonarr import list exclusion.

version_added: "0.7.0"

description: Manages Sonarr import list exclusion.

options:
    tvdb_id:
        description: TVDB ID.
        type: int

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Gather information about all import list exclusion
- name: Gather information about all import list exclusion
  devopsarr.sonarr.sonarr_import_list_exclusion_info:

# Gather information about a single list exclusion
- name: Gather information about a single list exclusion
  devopsarr.sonarr.sonarr_import_list_exclusion_info:
    tvdb_id: 123
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
import_list_exclusions:
    description: A list of remote path mappings.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: import list exclusion ID.
            type: int
            returned: always
            sample: 1
        tvdb_id:
            description: TVDB ID.
            type: int
            returned: 'always'
            sample: 12345
        title:
            description: Title.
            type: str
            returned: 'always'
            sample: 'Breaking Bad'
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
        tvdb_id=dict(type='int'),
    )


def list_import_list_exclusion(result):
    try:
        return client.list_import_list_exclusion()
    except sonarr.ApiException as e:
        module.fail_json('Error listing import list exclusions: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing import list exclusions: {}'.format(to_native(e)), **result)


def populate_import_list_exclusions(result):
    exclusions = []
    # Check if a resource is present already.
    for import_list_exclusion in list_import_list_exclusion(result):
        if module.params['tvdb_id']:
            if import_list_exclusion.tvdb_id == module.params['tvdb_id']:
                exclusions = [import_list_exclusion.model_dump(by_alias=False)]
        else:
            exclusions.append(import_list_exclusion.model_dump(by_alias=False))
    return exclusions


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = sonarr.ImportListExclusionApi(module.api)
    result = dict(
        changed=False,
        import_list_exclusions=[],
    )

    # List resources.
    result.update(import_list_exclusions=populate_import_list_exclusions(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
