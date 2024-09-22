"""init.py"""

from importlib import metadata

from conjugate_map.conj_calc import calc_mlat_rings  # noqa F401
from conjugate_map.conj_calc import conjcalc  # noqa F401
from conjugate_map.conj_calc import findconj  # noqa F401

# Set version
__version__ = metadata.version('conjugate_map')
