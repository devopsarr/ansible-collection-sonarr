#!/usr/bin/python

# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

DOCUMENTATION = r'''
---
module: sonarr_system_info

short_description: Sonarr system info module

version_added: "1.0.0"

description: Provide Sonarr system info

extends_documentation_fragment:
    - devopsarr.sonarr.sonarr_credentials

author:
    - Fuochi (@Fuochi)
'''

EXAMPLES = r'''
# It will fetch the system info
- name: Test with a message
  devopsarr.sonarr.sonarr_system_info:
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
app_name:
    description: It should be Sonarr.
    type: str
    returned: always
    sample: 'Sonarr'
version:
    description: Binary version.
    type: str
    returned: always
    sample: '3.0.8.1507'
build_time:
    description: Build time.
    type: str
    returned: always
    sample: '2022-04-23T21:40:53Z'
is_debug:
    description: Debug flag.
    type: bool
    returned: always
    sample: 'false'
is_production:
    description: Production flag.
    type: bool
    returned: always
    sample: 'false'
is_admin:
    description: Admin flag.
    type: bool
    returned: always
    sample: 'false'
is_user_interactive:
    description: User interactive flag.
    type: bool
    returned: always
    sample: 'false'
startup_path:
    description: Startup path.
    type: str
    returned: always
    sample: '/app/sonarr/bin'
app_data:
    description: Configuration path.
    type: str
    returned: always
    sample: '/config'
os_name:
    description: Host OS.
    type: str
    returned: always
    sample: 'ubuntu'
os_version:
    description: Host OS version.
    type: str
    returned: always
    sample: '20.04'
is_mono_runtime:
    description: Mono runtime flag.
    type: bool
    returned: always
    sample: 'true'
is_mono:
    description: Mono flag.
    type: bool
    returned: always
    sample: 'true'
is_linux:
    description: Linux flag.
    type: bool
    returned: always
    sample: 'false'
is_osx:
    description: OSX flag.
    type: bool
    returned: always
    sample: 'false'
is_windows:
    description: Windows flag.
    type: str
    returned: always
    sample: 'false'
mode:
    description: Mode.
    type: str
    returned: always
    sample: 'console'
branch:
    description: Sonarr branch.
    type: str
    returned: always
    sample: 'master'
authentication:
    description: Authentication type.
    type: str
    returned: always
    sample: 'none'
sqlite_version:
    description: SQLite version.
    type: str
    returned: always
    sample: '3.31.1'
url_base:
    description: URI prefix for installation.
    type: str
    returned: always
    sample: '/sonarr'
runtime_version:
    description: Runtime version.
    type: str
    returned: always
    sample: '6.12.0.122'
runtime_name:
    description: Runtime name.
    type: str
    returned: always
    sample: 'mono'
start_time:
    description: Start time.
    type: str
    returned: always
    sample: '2022-06-09T08:21:23.970798Z'
package_version:
    description: Package version.
    type: str
    returned: always
    sample: '3.0.8.1507-ls148'
package_author:
    description: Package author.
    type: str
    returned: always
    sample: '[linuxserver.io](https://linuxserver.io)'
package_update_mechanism:
    description: Package update mechanism.
    type: str
    returned: always
    sample: 'docker'
'''

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule

__metaclass__ = type


def run_module():
    result = dict(
        changed=False,
    )

    # init SonarrModule
    module = SonarrModule(
        supports_check_mode=True
    )

    # get the response from api
    response = module.api.system_status.get()
    # map the response to result
    result.update(**response)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
