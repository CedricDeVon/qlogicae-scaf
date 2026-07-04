from pathlib import Path

from library import (
    file_io_manager,
    filesystem_manager,
    value_cache_manager,
    yaml_file_io_manager,
    json_file_io_manager,
    text_file_io_manager,
)
from library.target_cache_value import TargetCacheValue


class WorkspaceFilesystemManager:
    def __init__(self) -> None:
        self._scope_selections: set[str] = {"private", "public"}

    @property
    def scope_selections(self) -> set[str]:
        return self._scope_selections

    def setup(self) -> bool:
        for workspace_scope_name in self.scope_selections:
            for configuration_file in Path(
                f"{
                    value_cache_manager.singleton.get_one_value(
                        ['current-root-full-path'],
                        output_type=TargetCacheValue.FOLDER_PATH,
                    )
                }/workspace/{workspace_scope_name}/configuration"
            ).iterdir():
                if not configuration_file.is_file():
                    continue

                with open(
                    configuration_file.resolve(),
                    encoding=file_io_manager.singleton.file_encoding,
                ) as current_file:
                    raw_data = self.read_file(current_file)

                    value_cache_manager.singleton.set_one_value(
                        [
                            f"workspace/{workspace_scope_name}/configuration/{configuration_file.name}-raw"
                        ],
                        ({} if raw_data is None else raw_data) or {},
                        output_type=TargetCacheValue.DEFINED,
                    )
                    value_cache_manager.singleton.set_one_value(
                        [
                            f"workspace/{workspace_scope_name}/configuration/{configuration_file.name}-full-path"
                        ],
                        configuration_file.resolve(),
                        output_type=TargetCacheValue.FILE_PATH,
                    )

    def shutdown(self) -> bool:
        return True

    def read_file(self, file: Any) -> Any:
        if yaml_file_io_manager.singleton.is_valid(file):
            return yaml_file_io_manager.singleton.read_file(file)

        elif json_file_io_manager.singleton.is_valid(file):
            return json_file_io_manager.singleton.read_file(file)

        else:
            return text_file_io_manager.singleton.read_file(file)

    def throw_if_required_files_not_found(self) -> bool:
        if not filesystem_manager.singleton.is_file_path_valid(
            f"{
                value_cache_manager.singleton.get_one_value(
                    ['current-root-full-path'],
                    output_type=TargetCacheValue.FOLDER_PATH,
                )
            }/workspace/public/configuration"
        ):
            raise Exception("workspace/public/configuration/workspace.yaml' must exist")

        if not filesystem_manager.singleton.is_file_path_valid(
            f"{
                value_cache_manager.singleton.get_one_value(
                    ['current-root-full-path'],
                    output_type=TargetCacheValue.FOLDER_PATH,
                )
            }/workspace/private/configuration"
        ):
            raise Exception("workspace/public/configuration/workspace.yaml' must exist")

        return False


singleton = WorkspaceFilesystemManager()
