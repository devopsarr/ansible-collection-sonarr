#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sonarr_quality_info

short_description: Get information about Sonarr quality.

version_added: "0.6.0"

description: Get information about Sonarr quality.

options:
    name:
        description: Name.
        type: str

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
---
# fetch all qualities
- name: fetch all qualities
  devopsarr.sonarr.sonarr_quality_info:

# fetch a single quality
- name: fetch a single quality
  devopsarr.sonarr.sonarr_quality_info:
    name: SDTV
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
qualities:
    description: A list of quality.
    returned: always
    type: list
    elements: dict
    contains:
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


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str'),
    )

    result = dict(
        changed=False,
        qualities=[],
    )

    module = SonarrModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    client = sonarr.QualityDefinitionApi(module.api)

    # Get resource.
    try:
        quality_list = client.list_quality_definition()
    except Exception as e:
        module.fail_json('Error getting qualities: %s' % to_native(e.reason), **result)

    qualities = []
    # Check if a resource is present already.
    for quality in quality_list:
        if module.params['name']:
            if quality['quality']['name'] == module.params['name']:
                qualities = [quality.dict(by_alias=False)]
        else:
            qualities.append(quality.dict(by_alias=False))

    result.update(qualities=qualities)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
