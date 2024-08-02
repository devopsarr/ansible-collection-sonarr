#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_quality

short_description: Manages Sonarr quality.

version_added: "0.6.0"

description: Manages Sonarr quality.

options:
    name:
        description: Name.
        required: true
        type: str
    title:
        description: Title.
        type: str
    min_size:
        description: Minimum size.
        type: float
    max_size:
        description: Maximum size.
        type: float
    preferred_size:
        description: Preferred size.
        type: float


extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# update quality
- name: Update quality
  devopsarr.sonarr.sonarr_quality:
    name: HDTV-2160p
    title: HDTV-2160p
    max_size: 200.0
    min_size: 35.0
    preferred_size: 95.0
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
id:
    description: Quality ID.
    type: int
    returned: always
    sample: '1'
title:
    description: Title.
    returned: always
    type: str
    sample: 'WEBRip-480p'
min_size:
    description: Minimum size.
    returned: always
    type: float
    sample: '1.0'
max_size:
    description: Maximum size.
    returned: always
    type: float
    sample: '130.0'
preferred_size:
    description: Preferred size.
    returned: always
    type: float
    sample: '95.0'
quality:
    description: Series folder format.
    returned: always
    type: dict
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
        name=dict(type='str', required=True),
        title=dict(type='str'),
        min_size=dict(type='float'),
        max_size=dict(type='float'),
        preferred_size=dict(type='float'),
    )


def list_qualities(result):
    try:
        return client.list_quality_definition()
    except sonarr.ApiException as e:
        module.fail_json('Error listing qualities: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
    except Exception as e:
        module.fail_json('Error listing qualities: {}'.format(to_native(e)), **result)


def find_quality(name, result):
    for quality in list_qualities(result):
        if quality.quality.name == name:
            return quality
    return None


def update_quality(want, result):
    result['changed'] = True
    # Only without check mode.
    if not module.check_mode:
        try:
            response = client.update_quality_definition(quality_definition_resource=want, id=str(want.id))
        except sonarr.ApiException as e:
            module.fail_json('Error updating quality: {}\n body: {}'.format(to_native(e.reason), to_native(e.body)), **result)
        except Exception as e:
            module.fail_json('Error updating quality: {}'.format(to_native(e)), **result)
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
    client = sonarr.QualityDefinitionApi(module.api)
    result = dict(
        changed=False,
        id=0,
    )

    # Check if a resource is present already.
    state = find_quality(module.params['name'], result)
    if state:
        result.update(state.model_dump(by_alias=False))

    # No delete is needed
    want = sonarr.QualityDefinitionResource(
        title=module.params['title'],
        min_size=module.params['min_size'],
        max_size=module.params['max_size'],
        preferred_size=module.params['preferred_size'],
    )

    # Update an existing resource if needed.
    want.id = result['id']
    want.weight = result['weight']
    want.quality = sonarr.Quality(**result['quality'])
    if want != state:
        update_quality(want, result)

    # Exit whith no changes.
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
