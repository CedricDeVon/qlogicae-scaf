from collections.abc import Callable

from library import (
    log_manager,
    workspace_log_manager,
    workspace_system_manager,
    workspace_macros_manager,
    workspace_filesystem_manager,
    workspace_value_cache_manager,
)
from library.target_cache_value import TargetCacheValue


class WorkspaceManager:
    def handle(self, callback: Callable[[void], void]) -> bool:
        self.setup()

        callback()

        self.shutdown()

        return True

    def setup(self) -> bool:
        workspace_system_manager.singleton.setup()
        workspace_filesystem_manager.singleton.setup()
        workspace_value_cache_manager.singleton.setup_pre_macros()
        workspace_macros_manager.singleton.setup()
        workspace_value_cache_manager.singleton.setup_post_macros()
        workspace_log_manager.singleton.setup()

        return True

    def shutdown(self) -> bool:
        workspace_log_manager.singleton.shutdown()
        workspace_value_cache_manager.singleton.shutdown()
        workspace_macros_manager.singleton.setup()
        workspace_filesystem_manager.singleton.shutdown()
        workspace_system_manager.singleton.shutdown()

        return True

    def handle_cli_argument_set_invalid(self, cli_arguments: Any) -> bool:
        log_manager.singleton.log_info(
            f"'{cli_arguments}' is not an existing cli option set"
        )

        return True


singleton = WorkspaceManager()
