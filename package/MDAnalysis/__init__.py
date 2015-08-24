# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8
#
# MDAnalysis --- http://www.MDAnalysis.org
# Copyright (c) 2006-2015 Naveen Michaud-Agrawal, Elizabeth J. Denning, Oliver Beckstein
# and contributors (see AUTHORS for the full list)
#
# Released under the GNU Public Licence, v2 or any higher version
#
# Please cite your use of MDAnalysis in published work:
# N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and O. Beckstein.
# MDAnalysis: A Toolkit for the Analysis of Molecular Dynamics Simulations.
# J. Comput. Chem. 32 (2011), 2319--2327, doi:10.1002/jcc.21787
#


"""
:mod:`MDAnalysis` --- analysis of molecular simulations in python
=================================================================

MDAnalysis (http://www.mdanalysis.org) is a python toolkit to analyze
molecular dynamics trajectories generated by CHARMM, NAMD, Amber,
Gromacs, or LAMMPS.

It allows one to read molecular dynamics trajectories and access the
atomic coordinates through numpy arrays. This provides a flexible and
relatively fast framework for complex analysis tasks. In addition,
CHARMM-style atom selection commands are implemented. Trajectories can
also be manipulated (for instance, fit to a reference structure) and
written out. Time-critical code is written in C for speed.

Help is also available through the mailinglist at
http://groups.google.com/group/mdnalysis-discussion

Please report bugs and feature requests through the issue tracker at
http://issues.mdanalysis.org

Citation
--------

When using MDAnalysis in published work, please cite

    N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and
    O. Beckstein. MDAnalysis: A Toolkit for the Analysis of Molecular Dynamics
    Simulations. J. Comput. Chem. 32 (2011), 2319--2327, doi:`10.1002/jcc.21787`_
    http://www.mdanalysis.org

For citations of included algorithms and sub-modules please see the references_.

.. _`10.1002/jcc.21787`: http://dx.doi.org/10.1002/jcc.21787
.. _references: http://docs.mdanalysis.org/documentation_pages/references.html


Getting started
---------------

Import the package::

  >>> import MDAnalysis

(note that not everything in MDAnalysis is imported right away; for
additional functionality you might have to import sub-modules
separately, e.g. for RMS fitting ``import MDAnalysis.analysis.align``.)

Build a "universe" from a topology (PSF, PDB) and a trajectory (DCD, XTC/TRR);
here we are assuming that PSF, DCD, etc contain file names. If you don't have
trajectories at hand you can play with the ones that come with MDAnalysis for
testing (see below under `Examples`_)::

  >>> u = MDAnalysis.Universe(PSF, DCD)

Select the C-alpha atoms and store them as a group of atoms::

  >>> ca = u.select_atoms('name CA')
  >>> len(ca)
  214

Calculate the centre of mass of the CA and of all atoms::

  >>> ca.center_of_mass()
  array([ 0.06873595, -0.04605918, -0.24643682])
  >>> u.atoms.center_of_mass()
  array([-0.01094035,  0.05727601, -0.12885778])

Calculate the CA end-to-end distance (in angstroem)::
  >>> from numpy import sqrt, dot
  >>> coord = ca.coordinates()
  >>> v = coord[-1] - coord[0]   # last Ca minus first one
  >>> sqrt(dot(v, v,))
  10.938133

Define a function eedist():
  >>> def eedist(atoms):
  ...     coord = atoms.coordinates()
  ...     v = coord[-1] - coord[0]
  ...     return sqrt(dot(v, v,))
  ...
  >>> eedist(ca)
  10.938133

and analyze all timesteps *ts* of the trajectory::
  >>> for ts in u.trajectory:
  ...      print eedist(ca)
  10.9381
  10.8459
  10.4141
   9.72062
  ....

.. SeeAlso:: :class:`MDAnalysis.core.AtomGroup.Universe` for details


Examples
--------

MDAnalysis comes with a number of real trajectories for testing. You
can also use them to explore the functionality and ensure that
everything is working properly::

  from MDAnalysis import *
  from MDAnalysis.tests.datafiles import PSF,DCD, PDB,XTC
  u_dims_adk = Universe(PSF,DCD)
  u_eq_adk = Universe(PDB, XTC)

The PSF and DCD file are a closed-form-to-open-form transition of
Adenylate Kinase (from [Beckstein2009]_) and the PDB+XTC file are ten
frames from a Gromacs simulation of AdK solvated in TIP4P water with
the OPLS/AA force field.

.. [Beckstein2009] O. Beckstein, E.J. Denning, J.R. Perilla and T.B. Woolf,
   Zipping and Unzipping of Adenylate Kinase: Atomistic Insights into the
   Ensemble of Open <--> Closed Transitions. J Mol Biol 394 (2009), 160--176,
   doi:10.1016/j.jmb.2009.09.009

"""

__all__ = ['Timeseries', 'Universe', 'as_Universe', 'Writer', 'collection']

import logging
import warnings

from .version import __version__

# custom exceptions and warnings
from .exceptions import (
    SelectionError, FinishTimeException, NoDataError, ApplicationError,
    SelectionWarning, MissingDataWarning, ConversionWarning, FileFormatWarning,
    StreamWarning
)

from .lib import log
from .lib.log import start_logging, stop_logging

logging.getLogger("MDAnalysis").addHandler(log.NullHandler())
del logging

# DeprecationWarnings are loud by default
warnings.simplefilter('always', DeprecationWarning)


from . import units

# Bring some often used objects into the current namespace
from .core import Timeseries
from .core.AtomGroup import Universe, as_Universe, Merge
from .coordinates.core import writer as Writer

collection = Timeseries.TimeseriesCollection()
import weakref
_anchor_universes = weakref.WeakSet()
_named_anchor_universes = weakref.WeakSet()
del weakref
