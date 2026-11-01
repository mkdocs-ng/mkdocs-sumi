"""Sumi: a modern, local-first documentation theme for MkDocs."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version('mkdocs-sumi')
except PackageNotFoundError:  # Not installed, e.g. run from a source checkout.
    __version__ = '0.0.0'
