#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_media_management_info

short_description: Get information about Sonarr media management.

version_added: "0.5.0"

description: Get information about Sonarr media management.

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch media management
- name: fetch media management info
  devopsarr.sonarr.media_management_info:
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Media management ID.
    type: int
    returned: always
    sample: '1'
chmod_folder:
    description: Permission in linux format.
    returned: always
    type: str
    sample: '755'
rescan_after_refresh:
    description: Rescan after refresh.
    returned: always
    type: str
    sample: 'afterManual'
recycle_bin:
    description: Bin path.
    returned: always
    type: str
    sample: '/tmp'
file_date:
    description: File date modification.
    returned: always
    type: str
    sample: 'localAirDate'
extra_file_extensions:
    description: Comma separated list of extra files extension to be imported.
    returned: always
    type: str
    sample: 'srt,info'
episode_title_required:
    description: Episode title required.
    returned: always
    type: str
    sample: 'bulkSeasonReleases'
download_propers_and_repacks:
    description: Download propers and repack.
    returned: always
    type: str
    sample: 'preferAndUpgrade'
chown_group:
    description: Linux group.
    returned: always
    type: str
    sample: 'arrs'
minimum_free_space_when_importing:
    description: Minimum free space when importing.
    returned: always
    type: int
    sample: '100'
recycle_bin_cleanup_days:
    description: Recycle bin days.
    returned: always
    type: int
    sample: '7'
auto_unmonitor_previously_downloaded_episodes:
    description: Auto unmonitor previously downloaded episodes.
    returned: always
    type: bool
    sample: 'true'
skip_free_space_check_when_importing:
    description: Skip free space check when importing.
    returned: always
    type: bool
    sample: 'true'
set_permissions_linux:
    description: Set linux permission flag.
    returned: always
    type: bool
    sample: 'true'
import_extra_files:
    description: Import extra files flag.
    returned: always
    type: bool
    sample: 'true'
enable_media_info:
    description: Enable media info flag.
    returned: always
    type: bool
    sample: 'true'
delete_empty_folders:
    description: Delete empty folders.
    returned: always
    type: bool
    sample: 'true'
create_empty_series_folders:
    description: Create empty series folder.
    returned: always
    type: bool
    sample: 'true'
copy_using_hardlinks:
    description: Copy using hardlinks.
    returned: always
    type: bool
    sample: 'true'
'''

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule
from ansible.module_utils.common.text.converters import to_native


try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def run_module():
    result = dict(
        changed=False,
    )

    module = SonarrModule(
        argument_spec={},
        supports_check_mode=True,
    )

    client = sonarr.MediaManagementConfigApi(module.api)

    # Get resource.
    try:
        media_management = client.get_media_management_config()
    except Exception as e:
        module.fail_json('Error getting media managements: %s' % to_native(e.reason), **result)

    result.update(media_management.dict(by_alias=False))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
