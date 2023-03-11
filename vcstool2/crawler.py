import os
from typing import List

from vcstool2.clients import GitClient


def find_repositories(paths: list, nested: bool = False) -> List[GitClient]:
    """
    Recursively search for Git repositories in a directory and its subdirectories.
    :param paths: List of directory paths to search.
    :param nested: Whether to search nested directories.
    :return: List of GitClient objects representing Git repositories found.
    """
    repos = []
    visited = []
    for path in paths:
        _find_repositories(path, repos, visited, nested=nested)
    return repos


def _find_repositories(path, repos, visited, nested=False):
    """
    :param path: Directory path to search.
    :param repos: List of GitClient objects representing Git repositories found.
    :param visited: List of visited directory paths to avoid duplicates.
    :param nested: Whether to search nested directories. Default is False.
    """
    abs_path = os.path.abspath(path)
    if abs_path in visited:
        return
    visited.append(abs_path)

    if GitClient.is_repository(path):
        repos.append(GitClient(path))
        if not nested:
            return

    try:
        listdir = os.listdir(path)
    except OSError:
        listdir = []
    for name in sorted(listdir):
        subpath = os.path.join(path, name)
        if not os.path.isdir(subpath):
            continue
        _find_repositories(subpath, repos, visited, nested=nested)
