#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_series_info

short_description: Get information about Sonarr series.

version_added: "1.0.0"

description: Get information about Sonarr series.

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
# Gather information about all series.
- name: Gather information about all series
  devopsarr.sonarr.sonarr_series_info:

# Gather information about a single series.
- name: Gather information about a single series
  devopsarr.sonarr.sonarr_series_info:
    tvdb_id: 12345678
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
series_list:
    description: A list of series.
    returned: always
    type: list
    elements: dict
    contains:
        id:
            description: series ID.
            type: int
            returned: always
            sample: 1
        monitored:
            description: Monitored flag.
            type: bool
            returned: always
            sample: false
        season_folder:
            description: Season folder flag.
            type: bool
            returned: always
            sample: false
        use_scene_numbering:
            description: Use scene numbering flag.
            type: bool
            returned: always
            sample: false
        quality_profile_id:
            description: Quality profile ID.
            type: int
            returned: always
            sample: 1
        tvdb_id:
            description: TVDB ID.
            type: int
            returned: always
            sample: 12345678
        path:
            description: Series path.
            type: str
            returned: always
            sample: "/series/series_title"
        root_folder_path:
            description: Root folder path.
            type: str
            returned: always
            sample: "/series"
        title:
            description: Series title.
            type: str
            returned: always
            sample: "Series Title"
        title_slug:
            description: Series title in kebab case.
            type: str
            returned: always
            sample: "series-title"
        tags:
            description: Tag list.
            type: list
            returned: always
            elements: int
            sample: [1,2]
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


def list_series(result):
    try:
        return client.list_series()
    except sonarr.ApiException as e:
        module.fail_json('Error listing series: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing series: {}'.format(to_native(e)), **result)


def populate_series(result):
    series = []
    # Check if a resource is present already.
    for single_series in list_series(result):
        if module.params['tvdb_id']:
            if single_series.tvdb_id == module.params['tvdb_id']:
                series = [single_series.model_dump(by_alias=False)]
        else:
            series.append(single_series.model_dump(by_alias=False))
    return series


def run_module():
    global client
    global module

    # Define available arguments/parameters a user can pass to the module
    module = SonarrModule(
        argument_spec=init_module_args(),
        supports_check_mode=True,
    )
    # Init client and result.
    client = sonarr.SeriesApi(module.api)
    result = dict(
        changed=False,
        series_list=[],
    )

    # List resources.
    result.update(series_list=populate_series(result))

    # Exit with data.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
