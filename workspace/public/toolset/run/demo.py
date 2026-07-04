from library import (
    workspace_manager,
    value_cache_manager,
)


def handle_manager_callback():
    value_cache_manager.singleton.display_all_items()


workspace_manager.singleton.handle(handle_manager_callback)
