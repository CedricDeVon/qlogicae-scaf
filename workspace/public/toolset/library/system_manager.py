import os
import shlex
import subprocess
from pathlib import Path

from library.execute_command_return import ExecuteCommandReturn


class SystemManager:
    def change_cli_filesystem_path(
        self,
        value: str,
    ) -> bool:
        path = Path(value).expanduser().resolve()

        if not path.exists():
            raise Exception(
                f"directory '{path}' does not exist.",
            )

        if not path.is_dir():
            raise Exception(
                f"'{path}' is not a directory.",
            )

        os.chdir(path)

        return True

    def execute_command(
        self,
        command: str,
        output_type: ExecuteCommandReturn = ExecuteCommandReturn.MINIMAL_RETURN,
    ) -> bool:
        if not command:
            raise ValueError("command cannot be empty")

        if isinstance(command, str):
            command = shlex.split(command)

        elif not isinstance(command, Sequence):
            raise TypeError("command must be a string or a sequence")

        match output_type:
            case ExecuteCommandReturn.MINIMAL_RETURN:
                return subprocess.run(
                    command,
                    check=True,
                    text=True,
                    encoding="utf-8",
                )

            case ExecuteCommandReturn.FULL_RETURN:
                return subprocess.check_output(
                    command,
                    text=True,
                    encoding="utf-8",
                ).strip()

        return True


singleton = SystemManager()
