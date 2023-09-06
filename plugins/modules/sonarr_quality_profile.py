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
        description: Quality name at which to cut off.
        type: str
    cutoff_format_score:
        description: Cutoff format score.
        type: int
        default: 0
    min_format_score:
        description: Min format score.
        type: int
        default: 0
    quality_groups:
        description: Quality groups
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
                description: Quality name list.
                type: list
                elements: str
    formats:
        description: Format items with score.
        type: dict
        default: {}

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
    cutoff: "WEB 720p"
    min_format_score: 0
    cutoff_format_score: 0
    quality_groups:
      - qualities:
          - "SDTV"
      - name: "WEB 720p"
        qualities:
          - "WEBRip-720p"
          - "WEBDL-720p"
    formats: {}

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
    sample: []
'''

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule
from ansible.module_utils.common.text.converters import to_native
from collections import OrderedDict

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        cutoff=dict(type='str'),
        min_format_score=dict(type='int', default=0),
        cutoff_format_score=dict(type='int', default=0),
        upgrade_allowed=dict(type='bool', default=False),
        quality_groups=dict(type='list', elements='dict', default=[]),
        formats=dict(type='dict', default={}),
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

    # Get schema
    schema_client = sonarr.QualityProfileSchemaApi(module.api)
    try:
        want = schema_client.get_qualityprofile_schema()
    except Exception as e:
        module.fail_json('Error getting quality profile schema: %s' % to_native(e.reason), **result)

    # Break apart quality groups and create a dict.
    quality_groups_dict = OrderedDict()
    
    for item in want.items:
        if item.quality is None:
            for quality in item.items:
                quality.allowed = False
                quality_groups_dict[quality.quality.name] = quality
        else:
            item.allowed = False
            quality_groups_dict[item.quality.name] = item

    # Populate quality groups.
    ident = 1000
    cutoff_id = None
    for item in module.params['quality_groups']:
        name = item['qualities'][0]
        if len(item['qualities']) == 1:
            quality_groups_dict[name].allowed = True
            if name == module.params['cutoff']:
                cutoff_id = quality_groups_dict[name].quality.id
        else:
            qualities = [quality_groups_dict[name].copy()]
            quality_groups_dict[name].allowed = True
            for quality in item['qualities'][1:]:
                qualities.append(quality_groups_dict.pop(quality))
                qualities[-1].allowed = True

            quality_groups_dict[name] = quality_groups_dict[name].copy(update={
                'allowed': True,
                'name': item['name'],
                'id': ident,
                'quality': None,
                'items': qualities,
            })

            if item['name'] == module.params['cutoff']:
                cutoff_id = ident
            ident += 1
    want.items = list(quality_groups_dict.values())


    # Populate formats.
    formats_dict = {item['name']: item for item in want.format_items}
    for key, value in module.params['formats'].items():
        formats_dict[key].score = value
    want.format_items = list(formats_dict.values())

    want = want.copy(update={
        'name': module.params['name'],
        'cutoff': cutoff_id,
        'upgrade_allowed': module.params['upgrade_allowed'],
        'cutoff_format_score': module.params['cutoff_format_score'],
        'min_format_score': module.params['min_format_score'],
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

