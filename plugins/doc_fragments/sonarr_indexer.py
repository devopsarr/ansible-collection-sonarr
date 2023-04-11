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
  enable_automatic_search:
    description: Enable automatic search flag.
    type: bool
  enable_interactive_search:
    description: Enable interactive search flag.
    type: bool
  enable_rss:
    description: Enable RSS flag.
    type: bool
  priority:
    description: Priority.
    type: int
  download_client_id:
    description: Download client ID.
    type: int
    default: 0
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
