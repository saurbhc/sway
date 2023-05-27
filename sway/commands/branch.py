from __future__ import annotations

import argparse

from sway.commands.config import SwayConfig


def branch_cmd(args: argparse.Namespace, config: SwayConfig) -> int:
    # parse args
    repo = args.repo or []

    for _repo in repo:
        if len(_repo) != 2:
            raise ValueError(
                f"'--repo/-r' must be used with 'repo-id repo-branch'. got {_repo}"
            )

        repo_id, repo_branch = _repo
        print(repo_id, repo_branch)

