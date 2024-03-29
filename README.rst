=======
pyemcee
=======

.. image:: https://img.shields.io/pypi/v/pyemcee.svg?style=flat
    :target: https://pypi.python.org/pypi/pyemcee/
    :alt: PyPI Version
    
.. image:: https://app.travis-ci.com/mcfit/pyemcee.svg?branch=master
    :target: https://app.travis-ci.com/github/mcfit/pyemcee
    :alt: Build Status
    
.. image:: https://ci.appveyor.com/api/projects/status/oqnksaooj338xn4d?svg=true
    :target: https://ci.appveyor.com/project/danehkar/pyemcee
    :alt: Build Status
    
.. image:: https://coveralls.io/repos/github/mcfit/pyemcee/badge.svg?
    :target: https://coveralls.io/github/mcfit/pyemcee?branch=master
    :alt: Coverage Status
    
.. image:: https://img.shields.io/badge/license-GPL-blue.svg
    :target: https://github.com/mcfit/pyemcee/blob/master/LICENSE
    :alt: GitHub license
    
.. image:: https://img.shields.io/conda/vn/conda-forge/pyemcee.svg
    :target: https://anaconda.org/conda-forge/pyemcee
    :alt: Anaconda Cloud
    
.. image:: https://readthedocs.org/projects/pyemcee/badge/?version=latest
    :target: https://pyemcee.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
    
.. image:: https://img.shields.io/badge/python-2.7%2C%203.5-blue.svg
    :alt: Support Python versions 2.7, 3.4 and 3.5
    
.. image:: https://img.shields.io/badge/DOI-10.5281/zenodo.4495911-blue.svg
    :target: https://doi.org/10.5281/zenodo.4495911
    :alt: Zenodo
    
.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/mcfit/pyemcee/HEAD?labpath=Notebook.ipynb

Description
===========

**pyemcee** is a Python implementation of the *affine-invariant Markov chain Monte Carlo (MCMC) ensemble sampler*, based on `sl_emcee <https://github.com/mcfit/sl_emcee>`_ by `M. A. Nowak <http://space.mit.edu/home/mnowak/isis_vs_xspec/>`_, an S-Lang/`ISIS <http://space.mit.edu/cxc/isis/>`_ implementation of the MCMC Hammer proposed by `Goodman & Weare (2010) <http://dx.doi.org/10.2140/camcos.2010.5.65>`_, and also implemented in Python (`emcee <https://github.com/dfm/emcee>`_) by `Foreman-Mackey et al. (2013) <https://ui.adsabs.harvard.edu/abs/2013PASP..125..306F/abstract>`_. 


Installation
============

To install the last version, all you should need to do is

.. code-block::

    $ python setup.py install

To install the stable version, you can use the preferred installer program (pip):

.. code-block::

    $ pip install pyemcee

or you can install it from the cross-platform package manager *conda*:

.. code-block::

    $ conda install -c conda-forge pyemcee

This package requires the following packages:

    - `NumPy <https://numpy.org/>`_
    - `SciPy <https://scipy.org/scipylib/>`_
    - `Matplotlib <https://matplotlib.org/>`_

How to Use
==========

The Documentation of the functions provides in detail in the *API Documentation* (`mcfit.github.io/pyemcee/doc <https://mcfit.github.io/pyemcee/doc>`_). This Python library creates the MCMC sampling  for given upper and lower uncertainties, and propagates uncertainties of parameters into the function.

See *Jupyter Notebook*: `Notebook.ipynb <https://github.com/mcfit/pyemcee/blob/master/Notebook.ipynb>`_

Run *Jupyter Notebook* on `Binder <https://mybinder.org/v2/gh/mcfit/pyemcee/HEAD?labpath=Notebook.ipynb>`_:

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/mcfit/pyemcee/HEAD?labpath=Notebook.ipynb

First, you need to load the **pyemcee** library as follows:

.. code-block:: python

    import pyemcee
    import numpy as np

You need to define your function. For example:

.. code-block:: python

    def myfunc21(input1):
       result1 = np.sum(input1)
       result2 = input1[1] ** input1[0]
       return [result1, result2]

Then, specify the upper and lower uncertainties of the prior parameters:

.. code-block:: python

    input1 = np.array([1., 2.])
    input1_err = np.array([0.2, 0.5])
    input1_err_p = input1_err
    input1_err_m = -input1_err
    output1 = myfunc21(input1)
    output1_num = len(output1)

Choose the appropriate uncertainty distribution. For example, for a uniform distribution, use_gaussian=0, and a Gaussian distribution use_gaussian=1. Then, specify the number of walkers and the number of iterations, e.g. walk_num=30 and iteration_num=100. You can then create the MCMC sample and propagate the uncertainties of the input parameters into your defined functions as follows:

.. code-block:: python

    use_gaussian=0 # uniform distribution from min value to max value
    walk_num=30 # number of walkers
    iteration_num=100 # number of samplers
    mcmc_sim = pyemcee.hammer(myfunc21, input1, input1_err_m, 
                              input1_err_p, output1, walk_num, 
                              iteration_num, use_gaussian)

To determine the upper and lower errors of the function outputs, you need to run with the chosen appropriate confidence level. For example, a 1.645-sigma standard deviation can be specified with clevel=0.90. For a 1-sigma standard deviation, we have clevel=0.682:

.. code-block:: python

    clevel=0.68268949 # 1-sigma
    output1_error = pyemcee.find_errors(output1, mcmc_sim, clevel, do_plot=1)
    
which shows the following distribution histograms:

.. image:: https://raw.githubusercontent.com/mcfit/pyemcee/master/examples/images/histogram0.png
    :width: 100

.. image:: https://raw.githubusercontent.com/mcfit/pyemcee/master/examples/images/histogram1.png
    :width: 100

To prevent plotting, you should set do_plot=None. To print the results:

.. code-block:: python

    for i in range(0, output1_num):
       print(output1[i], output1_error[i,:])

which provide the upper and lower limits on each parameter:

.. code-block::

    3.0 [-0.35801017 0.35998471]
    2.0 [-0.37573196 0.36297235]

For other standard deviation, you should use different confidence levels:

.. code-block:: python

    clevel=0.38292492 # 0.5-sigma
    clevel=0.68268949 # 1.0-sigma
    clevel=0.86638560 # 1.5-sigma
    clevel=0.90       # 1.645-sigma
    clevel=0.95       # 1.960-sigma
    clevel=0.95449974 # 2.0-sigma
    clevel=0.98758067 # 2.5-sigma
    clevel=0.99       # 2.575-sigma
    clevel=0.99730020 # 3.0-sigma
    clevel=0.99953474 # 3.5-sigma
    clevel=0.99993666 # 4.0-sigma
    clevel=0.99999320 # 4.5-sigma
    clevel=0.99999943 # 5.0-sigma
    clevel=0.99999996 # 5.5-sigma
    clevel=0.999999998# 6.0-sigma

Documentation
=============

For more information on how to use the API functions from the pyemcee library, please read the `API Documentation  <https://mcfit.github.io/pyemcee/doc>`_ published on `mcfit.github.io/pyemcee <https://mcfit.github.io/pyemcee>`_.


Learn More
==========

==================  =============================================
**Documentation**   https://pyemcee.readthedocs.io/
**Repository**      https://github.com/mcfit/pyemcee
**Issues & Ideas**  https://github.com/mcfit/pyemcee/issues
**Conda-Forge**     https://anaconda.org/conda-forge/pyemcee
**PyPI**            https://pypi.org/project/pyemcee/
**Archive**         `10.5281/zenodo.4495911 <https://doi.org/10.5281/zenodo.4495911>`_
==================  =============================================
