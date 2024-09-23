Usage
=====

.. _installation:

Installation
------------
To install from pypi: ``pip install conjugate-map``

To install from source: Clone git repo and run
``python -m pip install .`` from top level of directory.


Example Notebooks
-----------------

There are two example notebooks available: - ``MWE.ipynb``: Minimal
working example demonstrating conjugate calculations. -
``ConjugateMap.ipynb``: More in-depth examples using COMNAP, Madrigal
and other databases to produce animated maps with plotly express.

The following functions are imported from ``conj_calc.py``: -
``conjugate_map.findconj()`` : function to compute conjugate points for
a given location at a given time and date. -
``conjugate_map.conjcalc()`` : function to take in a dataframe and add
columns for all stages of calculating conjugate points. -
``conjugate_map.calc_mlat_rings()`` : function to calculate magnetic
graticules for a given latitude and datetime.

You can read the documentation for each function by running, e.g.,
``help(calc_mlat_rings)``.


How to Cite
-----------
Collins, K., & Burrell, A. (2023). conjugate-map (Version 1) [Computer
software]. https://doi.org/10.5281/zenodo.10056623
