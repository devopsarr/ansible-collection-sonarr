# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    # Plugin options for Sonarr objects with implementation
    DOCUMENTATION = r'''
options:
  config_contract:
    description: Config contract.
    type: str
  implementation:
    description: Implementation.
    type: str
  fields:
    description: Configuration field list.
    type: list
    elements: dict
    suboptions:
      name:
        description: Field name.
        type: str
      value:
        description: Field value.
        type: raw
'''
