# Copyright: (c) 2020, Fuochi <devopsarr@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

try:
    import sonarr
    HAS_SONARR_LIBRARY = True
except ImportError:
    HAS_SONARR_LIBRARY = False

from ansible_collections.devopsarr.sonarr.plugins.module_utils.sonarr_module import SonarrModule


class FieldException():
    def __init__(self, api, py):
        # type: (str, str) -> None
        self.api = api
        self.py = py

    def __getitem__(self, item):
        return getattr(self, item)


class FieldHelper():
    def __init__(self, fields):
        # type: (list[str]) -> None
        self.fields = fields
        self.exceptions = [
            FieldException(
                api='seedCriteria.seasonPackSeedTime',
                py='season_pack_seed_time',
            ),
            FieldException(
                api='seedCriteria.seedRatio',
                py='seed_ratio',
            ),
            FieldException(
                api='seedCriteria.seedTime',
                py='seed_time',
            ),
            FieldException(
                api='tags',
                py='field_tags',
            ),
            FieldException(
                api='profileIds',
                py='quality_profile_ids',
            ),
        ]

    def __getitem__(self, item):
        return getattr(self, item)

    def _to_camel_case(self, snake_str):
        # type: (str) -> str
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def _api_value(self, py_value):
        # type: (str) -> str
        for field in self.exceptions:
            if py_value == field['py']:
                return field['api']
        return self._to_camel_case(py_value)

    def populate_fields(self, module):
        # type: (SonarrModule) -> list[sonarr.Field]
        fields = []

        for field in self.fields:
            if field in module.params:
                fields.append(
                    sonarr.Field(**{
                        'name': self._api_value(field),
                        'value': module.params[field],
                    }),
                )

        return fields


class IndexerHelper():
    def __init__(self, status):
        # type: (sonarr.IndexerResource) -> None
        self.status = status
        self.indexer_fields = [
            'anime_standard_format_search',
            'allow_zero_size',
            'ranked_only',
            'api_key',
            'additional_parameters',
            'api_path',
            'base_url',
            'captcha_token',
            'cookie',
            'passkey',
            'username',
            'seed_ratio',
            'delay',
            'seed_time',
            'minimum_seeders',
            'season_pack_seed_time',
            'categories',
            'anime_categories',
        ]

    def is_changed(self, want):
        # type: (sonarr.IndexerResource) -> bool
        if (want.name != self.status.name or
                want.enable_automatic_search != self.status.enable_automatic_search or
                want.enable_interactive_search != self.status.enable_interactive_search or
                want.enable_rss != self.status.enable_rss or
                want.priority != self.status.priority or
                want.download_client_id != self.status.download_client_id or
                want.config_contract != self.status.config_contract or
                want.implementation != self.status.implementation or
                want.protocol != self.status.protocol or
                want.tags != self.status.tags):
            return True

        for status_field in self.status.fields:
            for want_field in want.fields:
                if want_field.name == status_field.name and want_field.value != status_field.value and status_field.value != "********":
                    return True
        return False


class DownloadClientHelper():
    def __init__(self, status):
        # type: (sonarr.DownloadClientResource) -> None
        self.status = status
        self.download_client_fields = [
            'add_paused',
            'use_ssl',
            'start_on_add',
            'sequential_order',
            'first_and_last',
            'add_stopped',
            'save_magnet_files',
            'read_only',
            'host',
            'api_key',
            'rpc_path',
            'url_base',
            'secret_token',
            'username',
            'password',
            'tv_category',
            'tv_imported_category',
            'tv_directory',
            'destination',
            'category',
            'nzb_folder',
            'strm_folder',
            'torrent_folder',
            'watch_folder',
            'magnet_file_extension',
            'port',
            'recent_tv_priority',
            'older_tv_priority',
            'recent_priority',
            'older_priority',
            'initial_state',
            'intial_state',
            'additional_tags',
            'field_tags',
            'post_import_tags',
        ]

    def is_changed(self, want):
        # type: (sonarr.DownloadClientResource) -> bool
        if (want.name != self.status.name or
                want.remove_completed_downloads != self.status.remove_completed_downloads or
                want.remove_failed_downloads != self.status.remove_failed_downloads or
                want.enable != self.status.enable or
                want.priority != self.status.priority or
                want.config_contract != self.status.config_contract or
                want.implementation != self.status.implementation or
                want.protocol != self.status.protocol or
                want.tags != self.status.tags):
            return True

        for status_field in self.status.fields:
            for want_field in want.fields:
                if want_field.name == status_field.name and want_field.value != status_field.value and status_field.value != "********":
                    return True
        return False


class ImportListHelper():
    def __init__(self, status):
        # type: (sonarr.ImportListResource) -> None
        self.status = status
        self.import_list_fields = [
            'access_token',
            'refresh_token',
            'api_key',
            'username',
            'auth_user',
            'rating',
            'base_url',
            'expires',
            'listname',
            'genres',
            'years',
            'trakt_additional_parameters',
            'limit',
            'trakt_list_type',
            'list_type',
            'language_profile_ids',
            'quality_profile_ids',
            'tag_ids',
        ]

    def is_changed(self, want):
        # type: (sonarr.ImportListResource) -> bool
        if (want.name != self.status.name or
                want.enable_automatic_add != self.status.enable_automatic_add or
                want.should_monitor != self.status.should_monitor or
                want.quality_profile_id != self.status.quality_profile_id or
                want.season_folder != self.status.season_folder or
                want.config_contract != self.status.config_contract or
                want.implementation != self.status.implementation or
                want.series_type != self.status.series_type or
                want.tags != self.status.tags):
            return True

        for status_field in self.status.fields:
            for want_field in want.fields:
                if want_field.name == status_field.name and want_field.value != status_field.value and status_field.value != "********":
                    return True
        return False
