from __future__ import absolute_import, division, print_function
from tjango.utils.version import get_version
# version is a human-readable version number.

# version_info is a four-tuple for programmatic comparison. The first
# three numbers are the components of the version number.  The fourth
# is zero for an official release, positive for a development branch,
# or negative for a release candidate or beta (after the base version
# number has been incremented)
VERSION = (0, 1, 1, 'beta', 1)

__version__ = get_version(VERSION)