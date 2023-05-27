from __future__ import annotations

import argparse

from sway.commands.branch import branch_cmd
from sway.commands.config import get_config_object, config_init, config_validate


def main() -> int:
    parser = argparse.ArgumentParser(prog="sway")

    # subparsers
    subparsers = parser.add_subparsers(dest="command")
    config_parser = subparsers.add_parser(
        "config",
        help=".pymonorepo-config.yaml options",
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
        help="use repo-id with provided branch, use --repo/-r {repo-id} {repo-branch}",
    )
    branch_parser.add_argument(
        "--environment",
        "-E",
        help="Project env setup in .sway-config.yaml",
    )

    args = parser.parse_args()

    if args.command == "config" and args.action == "init":
        return config_init(args=args)

    if args.command == "config" and args.action == "validate":
        return config_validate(args=args)

    config = get_config_object()

    if args.command == "branch":
        return branch_cmd(args=args, config=config)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())

