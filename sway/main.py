from __future__ import annotations

import argparse

from sway.commands.branch import branch_cmd
from sway.commands.build import build_poetry
from sway.commands.config import config_init, config_validate, get_config_object
from sway.utils.config import VERSION


def main() -> int:
    parser = argparse.ArgumentParser(prog="sway")

    # https://stackoverflow.com/a/8521644/812183
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    # subparsers
    subparsers = parser.add_subparsers(dest="command")
    config_parser = subparsers.add_parser(
        "config",
        help=".sway-config.yaml options",
    )
    branch_parser = subparsers.add_parser(
        "branch",
        help="branch-management options",
    )
    build_parser = subparsers.add_parser(
        "build",
        help="build-management options",
    )

    # config subparsers
    config_subparsers = config_parser.add_subparsers(dest="action")
    config_init_parser = config_subparsers.add_parser(
        "init",
        help="generate .sway-config.yaml config interatively",
    )
    config_validate_parser = config_subparsers.add_parser(
        "validate",
        help="validate .sway-config.yaml config",
    )

    # branch subparser commands
    branch_parser.add_argument(
        "--repo",
        "-r",
        type=str,
        nargs="*",
        action="append",
        metavar=("repo_id", "repo_branch"),
        help="use '--repo/-r {repo-id} {repo-branch}'",
    )
    branch_parser.add_argument(
        "--environment",
        "-e",
        required=True,
        help="env setup provided in .sway-config.yaml",
    )

    # build subparsers
    build_subparsers = build_parser.add_subparsers(dest="tool")
    build_poetry_subparser = build_subparsers.add_parser(
        "poetry",
        help="build via poetry",
    )

    # build poetry subparser commands
    build_poetry_subparser.add_argument(
        "--copy",
        help="copy .whl file to <path>, use '--copy <path>'",
    )
    build_poetry_subparser.add_argument(
        "--repo",
        "-r",
        type=str,
        nargs="*",
        action="append",
        metavar=("repo_id",),
        help="use '--repo/-r {repo-id}'",
    )

    args = parser.parse_args()

    if args.command == "config" and args.action == "init":
        return config_init(args=args)

    if args.command == "config" and args.action == "validate":
        return config_validate()

    config = get_config_object()

    if args.command == "branch":
        return branch_cmd(args=args, config=config)

    if args.command == "build" and args.tool == "poetry":
        return build_poetry(args=args, config=config)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
