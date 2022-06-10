# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    # Plugin options for Sonarr credentials
    DOCUMENTATION = r'''
options:
  sonarr_url:
    description: Full Sonarr URL with protocol and port (e.g. `https://test.sonarr.tv:8989`)
    type: str
    required: true
  sonarr_api_key:
    description: API key for Sonarr authentication.
    type: str
    required: true
notes:
  - for authentication, you can set service_account_file using the c(SONARR_URL) env variable.
  - for authentication, you can set service_account_contents using the c(SONARR_API_KEY) env variable.
'''
