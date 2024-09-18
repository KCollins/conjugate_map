"""init.py"""

from importlib import metadata

from conjugate_map.conj_calc import calc_mlat_rings
from conjugate_map.conj_calc import conjcalc
from conjugate_map.conj_calc import findconj

# Set version
__version__ = metadata.version('conjugate_map')
