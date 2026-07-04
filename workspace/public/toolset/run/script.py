import os
import argparse

from library import (
    system_manager,
    workspace_manager,
    macros_manager,
    file_log_manager,
    value_cache_manager,
)
from library.target_cache_value import TargetCacheValue
from library.execute_command_return import ExecuteCommandReturn


def handler_manager_callback():
    cli_parser = argparse.ArgumentParser(
        description="'script' command",
        epilog="...",
    )
    cli_parser.add_argument(
        "-t",
        "--target",
        help="target",
        dest="target",
        choices=(
            value_cache_manager.singleton.get_one_value(
                ["script-selections"],
                output_type=TargetCacheValue.DEFINED,
            )
            or {}
        ),
    )
    cli_arguments = cli_parser.parse_args()

    if not value_cache_manager.singleton.get_one_value(
        [
            f"workspace/public/configuration/workspace.yaml-raw",
            "data",
            "script",
            "is-enabled",
        ],
        output_type=TargetCacheValue.ANY,
    ):
        file_log_manager.singleton.log_warning(
            "'run.script' - check 'data.script.is-enabled' property within your 'workspace.yaml' file - disabled"
        )

        return False

    handle_targets(cli_arguments.target)

    return True


def handle_targets(target_name):
    target_type = value_cache_manager.singleton.get_one_value(
        [
            "workspace/public/configuration/workspace.yaml-raw",
            "data",
            "script",
            "targets",
            target_name,
            "type",
        ],
        output_type=TargetCacheValue.ANY,
    )

    if target_type == "individual":
        handle_target_option(target_name)

    elif target_type == "collection":
        for collection_script_name in (
            value_cache_manager.singleton.get_one_value(
                [
                    "workspace/public/configuration/workspace.yaml-raw",
                    "data",
                    "script",
                    "targets",
                    target_name,
                    "commands",
                ],
                output_type=TargetCacheValue.ANY,
            )
            or []
        ):
            collection_target_type = value_cache_manager.singleton.get_one_value(
                [
                    "workspace/public/configuration/workspace.yaml-raw",
                    "data",
                    "script",
                    "targets",
                    collection_script_name,
                    "type",
                ],
                output_type=TargetCacheValue.ANY,
            )

            if collection_target_type == "individual":
                handle_target_option(collection_script_name)

            elif collection_target_type == "collection":
                handle_targets(collection_script_name)
    else:
        workspace_manager.singleton.handle_cli_argument_set_invalid(cli_arguments)


def handle_target_option(target_name):
    file_log_manager.singleton.log_info(
        f"'run.script' - '{target_name}' execution - start"
    )

    system_manager.singleton.change_cli_filesystem_path(
        macros_manager.singleton.parse_one(
            value_cache_manager.singleton.get_one_value(
                [
                    "workspace/public/configuration/workspace.yaml-raw",
                    "data",
                    "script",
                    "targets",
                    target_name,
                    "enter-full-path",
                ],
                output_type=TargetCacheValue.ANY,
            )
            or "${{ current-root-full-path }}",
            (
                value_cache_manager.singleton.get_one_value(
                    ["workspace-macros"],
                    output_type=TargetCacheValue.DEFINED,
                )
                or {}
            ),
        )
    )

    for current_command in (
        value_cache_manager.singleton.get_one_value(
            [
                "workspace/public/configuration/workspace.yaml-raw",
                "data",
                "script",
                "targets",
                target_name,
                "commands",
            ],
            output_type=TargetCacheValue.DEFINED,
        )
        or []
    ):
        file_log_manager.singleton.log_info(
            system_manager.singleton.execute_command(
                macros_manager.singleton.parse_one(
                    current_command,
                    (
                        value_cache_manager.singleton.get_one_value(
                            ["workspace-macros"],
                            output_type=TargetCacheValue.DEFINED,
                        )
                        or {}
                    ),
                ),
                ExecuteCommandReturn.MINIMAL_RETURN,
            )
        )

    system_manager.singleton.change_cli_filesystem_path(
        macros_manager.singleton.parse_one(
            value_cache_manager.singleton.get_one_value(
                [
                    "workspace/public/configuration/workspace.yaml-raw",
                    "data",
                    "script",
                    "targets",
                    target_name,
                    "exit-full-path",
                ],
                output_type=TargetCacheValue.ANY,
            )
            or "${{ current-root-full-path }}",
            (
                value_cache_manager.singleton.get_one_value(
                    ["workspace-macros"],
                    output_type=TargetCacheValue.DEFINED,
                )
                or {}
            ),
        )
    )

    file_log_manager.singleton.log_info(
        f"'run.script' - '{target_name}' execution - complete"
    )

    return True


workspace_manager.singleton.handle(handler_manager_callback)
