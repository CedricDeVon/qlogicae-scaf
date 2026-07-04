import shutil
from pathlib import Path


class FileSystem:
    def get_root_workspace_folder(self):
        return Path(__file__).resolve().parent.parent.parent.parent.parent

    def get_cli_folder(self):
        return Path.cwd()

    def throw_if_filesystem_path_invalid(self, value):
        path = Path(value)

        if not path.exists():
            raise Exception(f"Path '{path}' is invalid")

        return False

    def throw_if_file_path_invalid(self, value):
        path = Path(value)

        if not path.is_file():
            raise Exception(f"File '{path}' is invalid")

        return False

    def throw_if_folder_path_invalid(self, value):
        path = Path(value)

        if not path.is_dir():
            raise Exception(f"'{path}' is invalid")

        return False

    def is_filesystem_path_valid(self, value):
        path = Path(value)

        if not path.exists():
            return False

        return True

    def is_file_path_valid(self, value):
        path = Path(value)

        if not path.is_file():
            return False

        return True

    def is_folder_path_valid(self, value):
        path = Path(value)

        if not path.is_dir():
            return False

        return True

    def clean_filesystem_path(self, path):
        directory = Path(path).resolve()

        protected_paths = {
            Path("/"),
            Path.home(),
        }

        if directory in protected_paths:
            raise Exception(f"'{path}' is protected")

        if not directory.exists():
            return True

        if not directory.is_dir():
            raise Exception(f"'{path}' is not a folder")

        for item in directory.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()

            elif item.is_dir():
                shutil.rmtree(item)

        return True

    def copy_filesystem_path(self, first_path, second_path):
        shutil.copytree(first_path, second_path, dirs_exist_ok=True)

        return True

    def move_filesystem_path(self, first_path, second_path):
        source = Path(first_path)
        destination = Path(second_path)

        destination.mkdir(parents=True, exist_ok=True)

        for path in source.iterdir():
            shutil.move(path, destination / path.name)

        return True


singleton = FileSystem()
