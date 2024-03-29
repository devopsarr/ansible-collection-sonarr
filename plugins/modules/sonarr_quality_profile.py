#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_quality_profile

short_description: Manages Sonarr quality profile.

version_added: "0.5.0"

description: Manages Sonarr quality profile.

options:
    name:
        description: Name.
        required: true
        type: str
    upgrade_allowed:
        description: Upgrade allowed flag.
        type: bool
        default: False
    cutoff:
        description: Quality ID to which cutoff.
        type: int
    cutoff_format_score:
        description: Cutoff format score.
        type: int
        default: 0
    min_format_score:
        description: Min format score.
        type: int
        default: 0
    quality_groups:
        description: Quality groups ordered list. Define only the allowed groups.
        type: list
        elements: dict
        default: []
        suboptions:
            name:
                description: Quality group name.
                type: str
            id:
                description: Quality group ID.
                type: int
            qualities:
                description: Quality list.
                type: list
                elements: dict
                suboptions:
                    name:
                        description: Quality name.
                        type: str
                    resolution:
                        description: Quality resolution.
                        type: str
                    source:
                        description: Quality source.
                        type: str
                    id:
                        description: Quality ID.
                        type: int
    formats:
        description: Format items list. Define only the used custom formats.
        type: list
        elements: dict
        default: []
        suboptions:
            name:
                description: Format name.
                type: str
            id:
                description: Format ID.
                type: int
            score:
                description: Format score.
                type: int

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials
    - devopsarr.sonarr.sonarr_state

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# Create a quality profile
- name: Create a quality profile
  devopsarr.sonarr.sonarr_quality_profile:
    name: "Example"
    upgrade_allowed: true
    cutoff: 1
    min_format_score: 0
    cutoff_format_score: 0
    quality_groups:
      - qualities:
        - id: 1
          name: "SDTV"
          source: "television"
          resolution: 480
      - name: "WEB 720p"
        id: 1001
        qualities:
          - id: 14
            name: "WEBRip-720p"
            source: "webRip"
            resolution: 720
          - id: 5
            name: "WEBDL-720p"
            source: "web"
            resolution: 720
    formats: []

# Delete a quality profile
- name: Delete a quality_profile
  devopsarr.sonarr.sonarr_quality_profile:
    name: Example
    state: absent
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Quality Profile ID.
    type: int
    returned: always
    sample: 1
name:
    description: Name.
    returned: always
    type: str
    sample: Example
upgrade_allowed:
    description: Upgrade allowed flag.
    returned: always
    type: bool
    sample: false
cutoff:
    description: Quality ID to which cutoff.
    returned: always
    type: int
    sample: 1
cutoff_format_score:
    description: Cutoff format score.
    returned: always
    type: int
    sample: 0
min_format_score:
    description: Min format score.
    returned: always
    type: int
    sample: 0
items:
    description: Quality groups
    returned: always
    type: list
    elements: dict
    sample: []
format_items:
    description: Format items list.
    returned: always
    type: list
    elements: dict
    sample: []
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
        name=dict(type='str', required=True),
        cutoff=dict(type='int'),
        min_format_score=dict(type='int', default=0),
        cutoff_format_score=dict(type='int', default=0),
        upgrade_allowed=dict(type='bool', default=False),
        quality_groups=dict(type='list', elements='dict', default=[]),
        formats=dict(type='list', elements='dict', default=[]),
        state=dict(default='present', type='str', choices=['present', 'absent']),
    )

    result = dict(
        changed=False,
        id=0,
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    client = sonarr.QualityProfileApi(module.api)

    # List resources.
    try:
        quality_profiles = client.list_quality_profile()
    except Exception as e:
        module.fail_json('Error listing quality profiles: %s' % to_native(e.reason), **result)

    # Check if a resource is present already.
    for profile in quality_profiles:
        if profile['name'] == module.params['name']:
            result.update(profile.dict(by_alias=False))
            state = profile

    # Delete the resource if needed.
    if module.params['state'] == 'absent':
        if result['id'] != 0:
            result['changed'] = True
            if not module.check_mode:
                try:
                    response = client.delete_quality_profile(result['id'])
                except Exception as e:
                    module.fail_json('Error deleting quality profile: %s' % to_native(e.reason), **result)
                result['id'] = 0
        module.exit_json(**result)

    # Populate quality groups.
    quality_groups = []
    allowed_qualities = []
    for item in module.params['quality_groups']:
        if len(item['qualities']) == 1:
            quality_groups.append(sonarr.QualityProfileQualityItemResource(**{
                'quality': sonarr.Quality(**{
                    'id': item['qualities'][0]['id'],
                    'name': item['qualities'][0]['name'],
                    'source': item['qualities'][0]['source'],
                    'resolution': item['qualities'][0]['resolution'],
                }),
                'items': [],
                'allowed': True,
            }))
            allowed_qualities.append(item['qualities'][0]['id'])
        else:
            qualities = []
            for quality in item['qualities']:
                qualities.append(sonarr.QualityProfileQualityItemResource(**{
                    'quality': sonarr.Quality(**{
                        'id': quality['id'],
                        'name': quality['name'],
                        'source': quality['source'],
                        'resolution': quality['resolution'],
                    }),
                    'allowed': True,
                    'items': []
                }))
                allowed_qualities.append(quality['id'])

            quality_groups.append(sonarr.QualityProfileQualityItemResource(**{
                'allowed': True,
                'name': item['name'],
                'id': item['id'],
                'items': qualities,
            }))

    # Add disallowed qualities
    temp_client = sonarr.QualityDefinitionApi(module.api)
    # GET resources.
    try:
        all_qualities = temp_client.list_quality_definition()
    except Exception as e:
        module.fail_json('Error listing qualities: %s' % to_native(e.reason), **result)

    for q in all_qualities[::-1]:
        if q['quality']['id'] not in allowed_qualities:
            quality_groups.insert(0, sonarr.QualityProfileQualityItemResource(**{
                'quality': sonarr.Quality(**{
                    'id': q['quality']['id'],
                    'name': q['quality']['name'],
                    'source': q['quality']['source'],
                    'resolution': q['quality']['resolution'],
                }),
                'items': [],
                'allowed': False,
            }))

    # Populate formats.
    formats = []
    used_formats = []
    for item in module.params['formats']:
        formats.append(sonarr.ProfileFormatItemResource(**{
            'name': item['name'],
            'format': item['id'],
            'score': item['score'],
        }))
        used_formats.append(item['id'])

    # Add unused formats
    temp_client = sonarr.CustomFormatApi(module.api)
    # GET resources.
    try:
        all_formats = temp_client.list_custom_format()
    except Exception as e:
        module.fail_json('Error listing formats: %s' % to_native(e.reason), **result)

    for f in all_formats:
        if f['id'] not in used_formats:
            formats.append(sonarr.ProfileFormatItemResource(**{
                'name': f['name'],
                'format': f['id'],
                'score': 0,
            }))

    want = sonarr.QualityProfileResource(**{
        'name': module.params['name'],
        'cutoff': module.params['cutoff'],
        'upgrade_allowed': module.params['upgrade_allowed'],
        'cutoff_format_score': module.params['cutoff_format_score'],
        'min_format_score': module.params['min_format_score'],
        'items': quality_groups,
        'format_items': formats,
    })

    # Create a new resource.
    if result['id'] == 0:
        result['changed'] = True
        # Only without check mode.
        if not module.check_mode:
            try:
                response = client.create_quality_profile(quality_profile_resource=want)
            except Exception as e:
                module.fail_json('Error creating quality profile: %s' % to_native(e.reason), **result)
            result.update(response.dict(by_alias=False))
        module.exit_json(**result)

    # Update an existing resource.
    want.id = result['id']
    if want != state:
        result['changed'] = True
        if not module.check_mode:
            try:
                response = client.update_quality_profile(quality_profile_resource=want, id=str(want.id))
            except Exception as e:
                module.fail_json('Error updating quality profile: %s' % to_native(e.reason), **result)
        result.update(response.dict(by_alias=False))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
