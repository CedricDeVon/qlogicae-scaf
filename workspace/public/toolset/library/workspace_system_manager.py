from library import (
    system_manager,
    filesystem_manager,
    value_cache_manager,
)
from library.target_cache_value import TargetCacheValue


class WorkspaceSystemManager:
    def setup(self) -> bool:
        value_cache_manager.singleton.set_one_value(
            ["current-root-full-path"],
            filesystem_manager.singleton.get_root_workspace_folder(),
            output_type=TargetCacheValue.FOLDER_PATH,
        )
        value_cache_manager.singleton.set_one_value(
            ["original-console-full-path"],
            filesystem_manager.singleton.get_cli_folder(),
            output_type=TargetCacheValue.FOLDER_PATH,
        )
        value_cache_manager.singleton.set_one_value(
            ["previous-console-full-path"],
            value_cache_manager.singleton.get_one_value(
                ["original-console-full-path"],
                output_type=TargetCacheValue.FOLDER_PATH,
            ),
            output_type=TargetCacheValue.FOLDER_PATH,
        )
        value_cache_manager.singleton.set_one_value(
            ["current-console-full-path"],
            value_cache_manager.singleton.get_one_value(
                ["current-root-full-path"],
                output_type=TargetCacheValue.FOLDER_PATH,
            ),
            output_type=TargetCacheValue.FOLDER_PATH,
        )
        system_manager.singleton.change_cli_filesystem_path(
            value_cache_manager.singleton.get_one_value(
                ["current-root-full-path"],
                output_type=TargetCacheValue.FOLDER_PATH,
            )
        )

        return True

    def shutdown(self) -> bool:
        return True


singleton = WorkspaceSystemManager()
