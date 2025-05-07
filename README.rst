conjugate_map
=============

|PyPI version| |DOI| |Documentation Status| |Coverage Status| |Test Status|

Files and scripts relating to geomagnetic conjugate map. Run in Binder
here: |Binder|

There are two example notebooks available:

- ``MWE.ipynb``: Minimal working example demonstrating conjugate calculations.

- ``ConjugateMap.ipynb``: More in-depth examples using COMNAP, Madrigal and other databases to produce animated maps with plotly express.

The following functions are imported from ``conj_calc.py``:

- ``conjugate_map.findconj()`` : function to compute conjugate points for a given location at a given time and date.

- ``conjugate_map.conjcalc()`` : function to take in a dataframe and add columns for all stages of calculating conjugate points.

- ``conjugate_map.calc_mlat_rings()`` : function to calculate magnetic graticules for a given latitude and datetime.

You can read the documentation for each function by running, e.g.,
``help(calc_mlat_rings)``.

Installation
------------

To install from pypi: ``pip install conjugate-map``

To install from source: Clone git repo and run
``python -m pip install .`` from top level of directory.

Testing
-------

To test locally, run ``python -m unittest`` from top level of directory.

.. |PyPI version| image:: https://badge.fury.io/py/conjugate-map.svg
   :target: https://badge.fury.io/py/conjugate-map
.. |DOI| image:: https://zenodo.org/badge/651410906.svg
   :target: https://zenodo.org/doi/10.5281/zenodo.10056623
.. |Documentation Status| image:: https://readthedocs.org/projects/conjugate-map/badge/?version=latest
   :target: https://conjugate-map.readthedocs.io/en/latest/?badge=latest
.. |Coverage Status| image:: https://coveralls.io/repos/github/KCollins/conjugate_map/badge.svg?branch=main
   :target: https://coveralls.io/github/KCollins/conjugate_map/?branch=main
.. |Test Status| image:: https://github.com/KCollins/conjugate_map/actions/workflows/main.yml/badge.svg?branch=main
   :target: https://github.com/KCollins/conjugate_map/actions/workflows/main.yml
.. |Binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/KCollins/conjugate_map/HEAD?labpath=notebooks%2FMWE.ipynb
