#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_series

short_description: Manages Sonarr series.

version_added: "1.0.0"

description: Manages Sonarr series.

options:
    monitored:
        description: Monitored flag.
        type: bool
        default: false
    season_folder:
        description: Season folder flag.
        type: bool
        default: false
    use_scene_numbering:
        description: Use scene numbering flag.
        type: bool
        default: false
    quality_profile_id:
        description: Quality profile ID.
        type: int
    tvdb_id:
        description: TVDB ID.
        required: true
        type: int
    path:
        description: Series path.
        required: true
        type: str
    root_folder_path:
        description: Root folder path.
        type: str
    title:
        description: Series title.
        required: true
        type: str
    title_slug:
        description: Series title in kebab case.
        required: true
        type: str

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials
    - devopsarr.sonarr.sonarr_taggable
    - devopsarr.sonarr.sonarr_state

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a series
- name: Create a series
  devopsarr.sonarr.sonarr_series:
    title: "Breaking Bad"
    title_slug: "breaking-bad"
    tvdb_id: 81189
    monitored: false
    season_folder: true
    use_scene_numbering: false
    path: "/config/breaking-bad"
    root_folder_path: "/config"
    quality_profile_id: 1
    tags: [1,2]

# Delete a series
- name: Delete a series
  devopsarr.sonarr.sonarr_series:
    title: "Breaking Bad"
    title_slug: "breaking-bad"
    tvdb_id: 81189
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
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


def is_changed(status, want):
    if (want.title != status.title or
            want.title_slug != status.title_slug or
            want.monitored != status.monitored or
            want.season_folder != status.season_folder or
            want.use_scene_numbering != status.use_scene_numbering or
            want.quality_profile_id != status.quality_profile_id or
            want.tvdb_id != status.tvdb_id or
            want.path != status.path or
            want.root_folder_path != status.root_folder_path or
            want.tags != status.tags):
        return True

    return False


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        monitored=dict(type='bool', default=False),
        season_folder=dict(type='bool', default=False),
        use_scene_numbering=dict(type='bool', default=False),
        title=dict(type='str', required=True),
        title_slug=dict(type='str', required=True),
        path=dict(type='str', required=True),
        root_folder_path=dict(type='str'),
        quality_profile_id=dict(type='int'),
        tvdb_id=dict(type='int', required=True),
        tags=dict(type='list', elements='int', default=[]),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )

    result = dict(
        changed=False,
        id=0,
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    client = sonarr.SeriesApi(module.api)

    # List resources.
    try:
        seriess = client.list_series()
    except Exception as e:
        module.fail_json('Error listing seriess: %s' % to_native(e.reason), **result)

    state = sonarr.SeriesResource()
    # Check if a resource is present already.
    for series in seriess:
        if series['tvdb_id'] == module.params['tvdb_id']:
            result.update(series.dict(by_alias=False))
            state = series

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        if result['id'] != 0:
            result['changed'] = True
            if not module.check_mode:
                try:
                    response = client.delete_series(result['id'])
                except Exception as e:
                    module.fail_json('Error deleting series: %s' % to_native(e.reason), **result)
                result['id'] = 0
        module.exit_json(**result)

    want = sonarr.SeriesResource(**{
        'title': module.params['title'],
        'title_slug': module.params['title_slug'],
        'monitored': module.params['monitored'],
        'season_folder': module.params['season_folder'],
        'use_scene_numbering': module.params['use_scene_numbering'],
        'quality_profile_id': module.params['quality_profile_id'],
        'tvdb_id': module.params['tvdb_id'],
        'path': module.params['path'],
        'root_folder_path': module.params['root_folder_path'],
        'tags': module.params['tags'],
        'add_options': sonarr.AddSeriesOptions(**{
            'monitor': 'all',
            'search_for_missing_episodes': True,
            'search_for_cutoff_unmet_episodes': False,
        }),
    })

    # Create a new resource.
    if result['id'] == 0:
        result['changed'] = True
        # Only without check mode.
        if not module.check_mode:
            try:
                response = client.create_series(series_resource=want)
            except Exception as e:
                module.fail_json('Error creating series: %s' % to_native(e.reason), **result)
            result.update(response.dict(by_alias=False))
        module.exit_json(**result)

    # Update an existing resource.
    want.id = result['id']
    if is_changed(state, want):
        result['changed'] = True
        if not module.check_mode:
            try:
                response = client.update_series(series_resource=want, id=str(want.id))
            except Exception as e:
                module.fail_json('Error updating series: %s' % to_native(e.reason), **result)
        result.update(response.dict(by_alias=False))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
