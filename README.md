# conjugate_map
[![PyPI version](https://badge.fury.io/py/conjugate-map.svg)](https://badge.fury.io/py/conjugate-map) [![DOI](https://zenodo.org/badge/651410906.svg)](https://zenodo.org/doi/10.5281/zenodo.10056623) [![Documentation Status](https://readthedocs.org/projects/conjugate-map/badge/?version=latest)](https://conjugate-map.readthedocs.io/en/latest/?badge=latest)


Files and scripts relating to geomagnetic conjugate map. 
Run in Binder here: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KCollins/conjugate_map/HEAD?labpath=notebooks%2FMWE.ipynb)

There are two example notebooks available:
 - `MWE.ipynb`: Minimal working example demonstrating conjugate calculations.
 - `ConjugateMap.ipynb`: More in-depth examples using COMNAP, Madrigal and other databases to produce animated maps with plotly express.

The following functions are imported from `conj_calc.py`:
 - `conjugate_map.findconj()` : function to compute conjugate points for a given location at a given time and date. 
 - `conjugate_map.conjcalc()` : function to take in a dataframe and add columns for all stages of calculating conjugate points.
 - `conjugate_map.calc_mlat_rings()` : function to calculate magnetic graticules for a given latitude and datetime.
 
 You can read the documentation for each function by running, e.g., `help(calc_mlat_rings)`.

## Installation
To install from pypi: 
`pip install conjugate-map`

To install from source: 
Clone git repo and run `python -m pip install .` from top level of directory.
