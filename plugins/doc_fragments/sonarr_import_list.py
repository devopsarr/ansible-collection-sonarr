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
  season_folder:
    description: Season folder flag.
    type: bool
  enable_automatic_add:
    description: Enable autometic add flag.
    type: bool
  quality_profile_id:
    description: Quality profile ID.
    type: int
  should_monitor:
    description: Should monitor.
    type: str
  root_folder_path:
    description: Root folder path.
    type: str
  series_type:
    description: Series type.
    type: str
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
