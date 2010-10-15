#! /usr/bin/env python
"""A thin replacement for ETSProjectTools. Performs checkout, update, install,
build, etc, of all actively maintained ETS packages, and allows arbitrary
shell commands to be run on all packages.
"""

import sys
import os
import subprocess

usage = """
Usage: ets -h | --help | co | COMMAND [args] | ALIAS [args]
   -h, --help  Print this message.

   co          Check out the entire ETS repository into the current working
               directory, each actively maintained package placed in its own
               sub-directory.

   COMMAND     Run this shell command, with any following arguments, inside
               each package's sub-directory. If any command arguments must be
               quoted, you may need to use nested quotes, depending on the
               quote handling in your shell. For example:
                  ets svn ci "'check-in comment for all packages'"

   ALIAS       Each alias is shorthand for a shell command with arguments.
               The available aliases are pre-defined by this script, not by
               the user. Any alias may be followed by optional additional
               arguments.


   The available aliases and their equivalent commands are:%s

   Examples:
      Fresh install all packages from trunk:
         mkdir ETS
         cd ETS
         ets co
         ets install

      Update all packages from trunk:
         ets up

   The ETS packages referenced, in order of processing, are:%s"""[1:]

aliases = """
      diff     svn diff
      rev      svn revert
      status   svn status
      up       svn update
      setup    python setup.py
      build    python setup.py build
      bdist    python setup.py bdist
      develop  python setup.py develop
      install  python setup.py install
      sdist    python setup.py sdist"""

"""
======================================================================
ETS installation dependencies.
Derived from ets_dependends.log, holding the output of ets_depends.py.
======================================================================

Notes:
1. Does not include ETS run-time, nor any non-ETS, dependencies.
2. To avoid clutter, does not list redundant dependencies. For example, does
   not list Traits or EnthoughtBase dependencies for packages which depend on
   TraitsGUI, because TraitsGUI itself depends on both of these.

Dependent packages are listed below and to the right of their dependencies.
* BlockCanvas's multiple dependencies are listed individually.

SetupDocs  (stands alone)
EnthoughtBase & Traits
    CodeTools  (depends on Traits only)
    SciMath
        BlockCanvas*
    TraitsGUI
        ETSDevTools
            BlocCanvas*
        TraitsBackendQt
        TraitsBackendWX
        Enable
            Chaco
               BlockCanvas*
        AppTools
            Mayavi
            EnvisageCore
                EnvisagePlugins
            BlockCanvas*
"""


ets_package_names = """
      EnthoughtBase      SetupDocs          Traits
      CodeTools          TraitsGUI          ETSDevTools
      SciMath            TraitsBackendQt    TraitsBackendWX
      Enable             AppTools           EnvisageCore
      EnvisagePlugins    Chaco              Mayavi
      BlockCanvas"""

ets_url = "https://svn.enthought.com/svn/enthought/%s/trunk"

def extract_alias_defs(text_defs):
    """ Given a multi-line string, with each line containing whitespace,
    then an alias name, then whitespace then the alias definition:
    Return a dictionary whose keys are the alias nanes and whose
    values are the corresponding alias definitions.
    """
    dic = {}
    for line in text_defs.split('\n'):
        tokens = line.split()
        if tokens:
            dic[tokens[0]] = " ".join(tokens[1:])
    return dic

def main():
    if len(sys.argv) == 1 or sys.argv[1] in ['-h', '--help']:
        print usage % (aliases, ets_package_names)
        return

    arg1 = sys.argv[1]
    if arg1 != 'co':
        alias_dict = extract_alias_defs(aliases)
        if arg1 in alias_dict:
            command = " ".join([alias_dict[arg1]] + sys.argv[2:])
        else:
            command = " ".join(sys.argv[1:])

    for ets_pkg_name in ets_package_names.split():
        if arg1 =='co':
            print "Checking out package %s" % ets_pkg_name
            pkg_url = ets_url % ets_pkg_name
            status = subprocess.check_call('svn co %s %s' %
                                           (pkg_url, ets_pkg_name), shell=True)
        else:
            print "Running command '%s' in package %s" % (command, ets_pkg_name)
            try:
                os.chdir(ets_pkg_name)
                subprocess.check_call(command, shell=True)
            except (OSError, subprocess.CalledProcessError), detail:
                print "   Error running command '%s' in package %s:\n   %s" % (
                    command, ets_pkg_name, detail)
                raw_input("   Press enter to process remaining packages.")
            os.chdir('..')

if __name__ == "__main__":
    main()
