#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_naming_info

short_description: Get information about Sonarr naming.

version_added: "0.5.0"

description: Get information about Sonarr naming.

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch naming
- name: fetch naming
  devopsarr.sonarr.sonarr_naming_info:
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Naming ID.
    type: int
    returned: always
    sample: '1'
standard_episode_format:
    description: Standard episode format.
    returned: always
    type: str
    sample: '{Series Title} - S{season:00}E{episode:00} - {Episode Title} {Quality Full}'
daily_episode_format:
    description: Daily episode format.
    returned: always
    type: str
    sample: '{Series Title} - {Air-Date} - {Episode Title} {Quality Full}'
anime_episode_format:
    description: Anime episode format.
    returned: always
    type: str
    sample: '{Series Title} - S{season:00}E{episode:00} - {Episode Title} {Quality Full}'
series_folder_format:
    description: Series folder format.
    returned: always
    type: str
    sample: '{Series Title}'
season_folder_format:
    description: Series folder format.
    returned: always
    type: str
    sample: 'Season {season}'
specials_folder_format:
    description: Series folder format.
    returned: always
    type: str
    sample: 'S0'
multi_episode_style:
    description: Multi episode style. 0 - 'Extend' 1 - 'Duplicate' 2 - 'Repeat' 3 - 'Scene' 4 - 'Range' 5 - 'Prefixed Range'.
    returned: always
    type: int
    sample: 2
colon_replacement_format:
    description: >
        Colon replacement format.
        0 - 'Delete' 1 - 'Replace with Dash' 2 - 'Replace with Space Dash' 3 - 'Replace with Space Dash Space' 4 - 'Smart Replace'.
    returned: always
    type: int
    sample: 2
rename_episodes:
    description: Rename episodes.
    returned: always
    type: bool
    sample: true
replace_illegal_characters:
    description: Replace illegal characters.
    returned: always
    type: bool
    sample: true
'''

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule
from ansible.module_utils.common.text.converters import to_native

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def get_naming_config(result):
    try:
        return client.get_naming_config()
    except sonarr.ApiException as e:
        module.fail_json('Error getting naming: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting naming: {}'.format(to_native(e)), **result)


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec={},
        supports_check_mode=True,
    )
    # Init client and result.
    client = sonarr.NamingConfigApi(module.api)
    result = dict(
        changed=False,
    )

    # Get resource.
    result.update(get_naming_config(result).model_dump(by_alias=False))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
