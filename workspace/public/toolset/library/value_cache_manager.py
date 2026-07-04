from typing import Any
from collections.abc import Mapping

from library import filesystem_manager, value_cache_storage_manager
from library.target_cache_value import TargetCacheValue


class ValueCacheManager:
    def is_key_found(self, keys: list[str]) -> bool:
        return value_cache_storage_manager.singleton.is_key_found(keys)

    def get_one_value(
        self,
        keys: list[str],
        output_type: TargetCacheValue = TargetCacheValue.DEFINED,
    ) -> Any:
        value = value_cache_storage_manager.singleton.get_one_value(keys)
        self.throw_if_value_is_explicitly_invalid(value, output_type)

        return value

    def set_one_value(
        self,
        keys: list[str],
        value: Any,
        output_type: TargetCacheValue = TargetCacheValue.DEFINED,
    ) -> bool:
        self.throw_if_value_is_explicitly_invalid(value, output_type)

        return value_cache_storage_manager.singleton.set_one_value(keys, value)

    def remove_one_value(self, keys: list[str]) -> bool:
        self.throw_if_key_not_found(keys)

        return value_cache_storage_manager.singleton.remove_one_value(keys)

    def clear_all_values(self) -> bool:
        return value_cache_storage_manager.singleton.clear_all_values()

    def display_all_items(self) -> bool:
        return value_cache_storage_manager.singleton.display_all_items()

    def throw_if_value_is_explicitly_invalid(
        self,
        value: Any,
        output_type: TargetCacheValue = TargetCacheValue.DEFINED,
    ) -> bool:
        match output_type:
            case TargetCacheValue.FILESYSTEM_PATH:
                return filesystem_manager.singleton.throw_if_filesystem_path_invalid(
                    value
                )

            case TargetCacheValue.FILE_PATH:
                return filesystem_manager.singleton.throw_if_file_path_invalid(value)

            case TargetCacheValue.FOLDER_PATH:
                return filesystem_manager.singleton.throw_if_folder_path_invalid(value)

            case TargetCacheValue.DEFINED:
                return self.throw_if_undefined(value)

            case _:
                return False

        return False

    def throw_if_key_not_found(self, keys: list[str]) -> bool:
        if not value_cache_storage_manager.singleton.is_key_found(keys):
            raise Exception(f"key path '{keys}' does not exist")

        return False

    def throw_if_undefined(self, value: Any) -> bool:
        if value is None:
            raise Exception("value is not defined")

        return False


singleton = ValueCacheManager()
