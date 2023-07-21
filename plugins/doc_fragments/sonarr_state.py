# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    # Plugin options for Sonarr deletable objects
    DOCUMENTATION = r'''
options:
  state:
    description: Create or delete resource.
    required: false
    default: 'present'
    choices: [ "present", "absent" ]
    type: str
'''
