"""
Filters of the Open edX platform.
"""
import sys
import warnings

from openedx_filters.filters import *

__version__ = "3.3.0"

if sys.version_info < (3, 12):
    warnings.warn(
        "Python 3.11 support is deprecated and will be removed in a future release. "
        "Please upgrade to Python 3.12 or later.",
        DeprecationWarning,
        stacklevel=2,
    )
