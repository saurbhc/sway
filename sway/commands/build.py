from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess

from sway.commands.config import SwayConfig


def build_poetry(args: argparse.Namespace, config: SwayConfig) -> int:
    # parse args
    _copy = args.copy

    for repo in config.repos:
        repo_id = repo.id
        repo_path = repo.path

        assert repo_path

        os.chdir(repo_path)

        current_branch = subprocess.run(
            ("git", "rev-parse", "--abbrev-ref", "HEAD"),
            check=True,
            capture_output=True,
            text=True,
        ).stdout.rstrip("\n")

        print(f"[{repo_id}] building {current_branch}")

        cmd = ("poetry", "build")
        p = subprocess.run(
            cmd,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
        )
        if p.returncode != 0:
            print(p.stdout.decode().strip())
            return 1

        if _copy:
            # find whl path
            pattern = re.compile("- Building wheel\\n  - Built (.*)")
            match = pattern.search(p.stdout.decode())
            assert match
            whl_file = match.groups()[0]

            src = repo_path + f"/dist/{whl_file}"
            print(f"[{repo_id}] copying {src} -> {_copy}")
            shutil.copy(src=src, dst=_copy)

    return 0
