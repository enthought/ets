=================================
Enthought Tool Suite meta-project
=================================

http://github.enthought.com/

The Enthought Tool Suite (ETS) is a collection of components developed by
Enthought and our partners, which we use every day to construct custom
scientific applications.

This project is a "meta-project wrapper" that bundles up the actual
projects.

But, it also contains the ets.py module, which allows pulling all other
ETS projects from github, and other useful features.

Installation::

  mkdir ets
  cd ets
  git clone git@github.com:enthought/ets.git
  cd ets
  python setup.py develop
  cd ..
  ets -h
