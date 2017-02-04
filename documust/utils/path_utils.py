"""Path related utilities"""

import fnmatch
import os
from six.moves import queue


def matches_in_path(path, flat, match):
    """Returns all matches to match in path, using BFS if flat is False"""

    matches = []
    dirs = queue.Queue()
    dirs.put(path)

    while not dirs.empty():
        current_path = dirs.get()

        directory_tree = next(os.walk(current_path))
        for filename in fnmatch.filter(directory_tree[2], match):  # All files that match
            matches.append(os.path.join(current_path, filename))

        if not flat:  # Search all folders
            for dirname in directory_tree[1]:  # All dirs
                dirs.put(os.path.join(current_path, dirname))

    return matches


def load_source(path):
    """Loads a module source code by path"""
    with open(path, 'r') as source:
        return source.read()
