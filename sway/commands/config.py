from __future__ import annotations

import argparse
from typing import Any

from sway.utils.yaml import get_config, set_config


class RepoEnvConfig:
    def __init__(self, env: str, branch: str):
        self.env = env
        self.branch = branch

    def __repr__(self) -> str:
        return f"{self.env} - {self.branch}"


class RepoConfig:
    def __init__(
        self,
        repo_id: str,
        repo: str,
        path: str | None = None,
        envs: list[RepoEnvConfig] | None = None,
    ):
        self.id = repo_id
        self.repo = repo
        self.path = path
        self.envs = envs

    def __repr__(self) -> str:
        return f"{self.id} | {self.repo} | {self.path} | {self.envs}"


class SwayConfig:
    def __init__(self, repos: list[RepoConfig]):
        self.repos = repos

    def __repr__(self) -> str:
        return f"{self.repos}"


def get_config_object() -> SwayConfig:
    data = get_config()

    repos = []
    for repo in data["repos"]:
        repos.append(
            RepoConfig(
                # make it optional, create id from repo when not given
                repo_id=repo["id"],
                repo=repo["repo"],
                # default path would be parent dir
                path=repo.get("path", "./../"),
                envs=[
                    RepoEnvConfig(env=env["env"], branch=env["branch"])
                    for env in repo.get("envs", [])
                ]
                or None,
            ),
        )

    return SwayConfig(repos=repos)


def config_init(args: argparse.Namespace) -> int:
    q = "Would you like to define your repos interactively? (yes/no) "
    a = input(q)
    if a not in ("yes", "y"):
        print(
            "Refer the README.md in the `sway` repository for config file instructions.",
        )
        return 0

    repos: list[dict[str, Any]] = []
    while True:
        print("\nAdding Repository:")
        repo = input("repo: [Example: git@github.com:saurbhc/sway] ")
        repo_id = input("id: [Example: sway] ")
        repo_path = input("path: [Example: /home/ubuntu/dev/sway] ")

        q = f"\nWould you like to define --environment/-e for {repo_id}? (yes/no) "
        a = input(q)
        if a not in ("yes", "y"):
            repos.append(
                {
                    "id": repo_id,
                    "repo": repo,
                    "path": repo_path,
                },
            )
            break

        envs = []
        while True:
            print(f"\n- Adding Environment for Repository {repo_id}:")
            env = input("- env: [Example: dev] ")
            branch = input("- branch: [Example: develop] ")
            envs.append(
                {
                    "env": env,
                    "branch": branch,
                },
            )

            q = f"\nWould you like to define more --environment/-e for {repo_id}? (yes/no) "
            a = input(q)
            if a not in ("yes", "y"):
                break

        repos.append(
            {
                "id": repo_id,
                "repo": repo,
                "path": repo_path,
                "envs": envs,
            },
        )

        q = "Would you like to define more repos interactively? (yes/no) "
        a = input(q)
        if a not in ("yes", "y"):
            break

    set_config(data={"repos": repos})

    return 0


def config_validate() -> int:
    config = get_config_object()
    # TODO: add validation, see #2

    return 0
