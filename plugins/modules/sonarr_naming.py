#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_naming

short_description: Manages Sonarr naming.

version_added: "0.0.6"

description: Manages Sonarr naming.

options:
    standard_episode_format:
        description: Standard episode format.
        required: true
        type: str
    daily_episode_format:
        description: Daily episode format.
        required: true
        type: str
    anime_episode_format:
        description: Anime episode format.
        required: true
        type: str
    series_folder_format:
        description: Series folder format.
        required: true
        type: str
    season_folder_format:
        description: Series folder format.
        required: true
        type: str
    specials_folder_format:
        description: Series folder format.
        required: true
        type: str
    custom_colon_replacement_format:
        description: Custom colon folder format.
        required: false
        default: ""
        type: str
    multi_episode_style:
        description: Multi episode style. 0 - 'Extend' 1 - 'Duplicate' 2 - 'Repeat' 3 - 'Scene' 4 - 'Range' 5 - 'Prefixed Range'.
        required: true
        type: int
        choices: [0, 1, 2, 3, 4, 5]
    colon_replacement_format:
        description: >
            Colon replacement format.
            0 - 'Delete' 1 - 'Replace with Dash' 2 - 'Replace with Space Dash' 3 - 'Replace with Space Dash Space' 4 - 'Smart Replace', 5 - 'Custom Replace'.
        required: true
        type: int
        choices: [0, 1, 2, 3, 4, 5]
    rename_episodes:
        description: Rename episodes.
        required: true
        type: bool
    replace_illegal_characters:
        description: Replace illegal characters.
        required: true
        type: bool

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update naming
- name: Update naming
  devopsarr.sonarr.sonarr_naming:
    rename_episodes: true
    replace_illegal_characters: true
    multi_episode_style: 0
    colon_replacement_format: 0
    daily_episode_format: '{Series Title} - {Air-Date} - {Episode Title} {Quality Full}'
    anime_episode_format: '{Series Title} - S{season:00}E{episode:00} - {Episode Title} {Quality Full}'
    series_folder_format: '{Series Title}'
    season_folder_format: 'Season {season}'
    specials_folder_format: 'S0'
    standard_episode_format: '{Series Title} - S{season:00}E{episode:00} - {Episode Title} {Quality Full}'
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
custom_colon_replacement_format:
    description: Custom colon replacement format.
    returned: always
    type: str
    sample: ':'
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


def init_module_args():
    # define available arguments/parameters a user can pass to the module
    return dict(
        standard_episode_format=dict(type='str', required=True),
        daily_episode_format=dict(type='str', required=True),
        anime_episode_format=dict(type='str', required=True),
        series_folder_format=dict(type='str', required=True),
        season_folder_format=dict(type='str', required=True),
        specials_folder_format=dict(type='str', required=True),
        multi_episode_style=dict(type='int', required=True, choices=[0, 1, 2, 3, 4, 5]),
        colon_replacement_format=dict(type='int', required=True, choices=[0, 1, 2, 3, 4, 5]),
        custom_colon_replacement_format=dict(type='str', required=False, default=""),
        rename_episodes=dict(type='bool', required=True),
        replace_illegal_characters=dict(type='bool', required=True),
    )


def read_naming(result):
    try:
        return client.get_naming_config()
    except sonarr.ApiException as e:
        module.fail_json('Error getting naming: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error getting naming: {}'.format(to_native(e)), **result)


def update_naming(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_naming_config(naming_config_resource=want, id="1")
        except sonarr.ApiException as e:
            module.fail_json('Error updating naming: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating naming: {}'.format(to_native(e)), **result)
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
    client = sonarr.NamingConfigApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Get resource.
    state = read_naming(result)
    if state:
        result.update(state.model_dump(by_alias=False))

    want = sonarr.NamingConfigResource(
        standard_episode_format=module.params['standard_episode_format'],
        daily_episode_format=module.params['daily_episode_format'],
        anime_episode_format=module.params['anime_episode_format'],
        series_folder_format=module.params['series_folder_format'],
        season_folder_format=module.params['season_folder_format'],
        specials_folder_format=module.params['specials_folder_format'],
        multi_episode_style=module.params['multi_episode_style'],
        colon_replacement_format=module.params['colon_replacement_format'],
        custom_colon_replacement_format=module.params['custom_colon_replacement_format'],
        rename_episodes=module.params['rename_episodes'],
        replace_illegal_characters=module.params['replace_illegal_characters'],
        id=1,
    )

    # Update an existing resource.
    if want != state:
        update_naming(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
