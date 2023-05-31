# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r'''
options:
  name:
    description: Name.
    required: true
    type: str
  remove_completed_downloads:
    description: Remove completed downloads flag.
    type: bool
  remove_failed_downloads:
    description: Remove failed downloads flag.
    type: bool
  enable:
    description: Enable flag.
    type: bool
  priority:
    description: Priority.
    type: int
  tags:
    description: Tag list.
    type: list
    elements: int
    default: []
  state:
    description: Create or delete a indexer.
    required: false
    default: 'present'
    choices: [ "present", "absent" ]
    type: str
'''
