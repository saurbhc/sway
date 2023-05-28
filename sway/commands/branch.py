from __future__ import annotations

import argparse
import os
import subprocess

from sway.commands.config import SwayConfig


def branch_repo(
    args: argparse.Namespace,
    config: SwayConfig,
    repo: list[list[str]],
) -> dict[str, dict[str, str | None]]:
    branch_repos = {}

    repo_ids = {r.id: r for r in config.repos}
    for _repo in repo:
        # validate
        if len(_repo) != 2:
            err = f"usage: '--repo/-rrepo-id repo-branch'. got {_repo}"
            raise ValueError(err)

        # parse
        repo_id, repo_branch = _repo

        # repo exists in config
        if repo_id not in repo_ids:
            raise ValueError("repo-id must exist in .sway-config.yaml")

        branch_repos[repo_id] = {
            "path": repo_ids[repo_id].path,
            "branch": repo_branch,
        }

    return branch_repos


def branch_cmd(args: argparse.Namespace, config: SwayConfig) -> int:
    # parse args
    repo = args.repo or []
    env = args.environment

    if repo:
        branch_repos = branch_repo(args=args, config=config, repo=repo)
    else:
        branch_repos = {
            r.id: {"path": r.path, "branch": r_env.branch}
            for r in config.repos
            for r_env in r.envs or ()
            if r_env.env == env
        }

    # todo if branch_repos is empty - raise ValueError ?
    if not branch_repos:
        print(f"no repos found with {env=}")

    for repo_id, repo_config in branch_repos.items():
        repo_path = repo_config["path"]
        repo_branch = repo_config["branch"]

        assert repo_path
        assert repo_branch

        os.chdir(repo_path)

        current_branch = subprocess.run(
            ("git", "rev-parse", "--abbrev-ref", "HEAD"),
            check=True,
            capture_output=True,
            text=True,
        ).stdout.rstrip("\n")

        if current_branch == repo_branch:
            print(f"[{repo_id}] {current_branch}")
            continue

        print(f"[{repo_id}] {current_branch} -> {repo_branch}")

        cmd = ("git", "checkout", repo_branch)
        p = subprocess.run(
            cmd,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
        )
        if p.returncode != 0:
            print(p.stdout.decode().strip())

    return 0
