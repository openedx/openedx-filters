"""
Filters of the Open edX platform.
"""
import sys
import warnings
from importlib.metadata import PackageNotFoundError, version

from openedx_filters.filters import *

try:
    __version__ = version("openedx-filters")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

if sys.version_info < (3, 12):  # pragma: no cover
    warnings.warn(
        "Python 3.11 support is deprecated and will be removed in a future release. "
        "Please upgrade to Python 3.12 or later.",
        DeprecationWarning,
        stacklevel=2,
    )
