#! /usr/bin/env python
# flake8: noqa
# type: ignore
# nosec

# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""A thin replacement for SetupDocs (which is no longer part of ETS).
Performs documentation building, check in, updating, etc of all actively
maintained ETS packages.
"""

import sys
import os
import subprocess
from distutils.dir_util import copy_tree

usage = """\
Usage: ets_docs -h | --help | update [PROJ] | COMMAND [args] | ALIAS [args]
   -h, --help  Print this message.

   update      This command performs a 'remote update', ie it updates the
               live website from the repository.  If your remote username
               is different than your local username, you may specify the
               remote one here.

   COMMAND     Run this shell command, with any following arguments, inside
               each package's documentation sub-directory. If any command
               arguments must be quoted, you may need to use nested quotes,
               depending on the quote handling in your shell. For example:
                  ets_docs svn ci "'check-in comment for all packages'"

   ALIAS       Each alias is shorthand for a shell command with arguments.
               The available aliases are pre-defined by this script, not by
               the user. Any alias may be followed by optional additional
               arguments.


   The available aliases and their equivalent commands are:%s

   Example:
      Fresh install and basic workflow:
        ets_docs html          # Generate new HTML docs
        ets_docs update traits # Updates the gh-pages branch.


   The ETS packages referenced, in order of processing, are:\n%s
   """

aliases = """\n
      html     make html
      latex    make latex
      """

ets_package_names = """\
      traits             pyface             traitsui
      codetools          etsdevtools        scimath
      enable             apptools           envisage
      chaco              mayavi             blockcanvas
      """

alias_dict = {}
for line in aliases.split('\n'):
    tokens = line.split()
    if tokens:
         alias_dict[tokens[0]] = tokens[1:]


def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith('-'):
        print(usage % (aliases, ets_package_names))
        return

    arg1 = sys.argv[1]

    # Update the gh-pages branch
    if arg1 == 'update':
        if 2 < len(sys.argv):
            ets_packages = sys.argv[2:]
        else:
            ets_packages = ets_package_names.split()

        for ets_pkg_name in ets_packages:
            print("Updating documentation branch for {0}...".format(ets_pkg_name))

            # Find the current branch, so that we may return to it
            branches = subprocess.check_output(['git', 'branch'], cwd=ets_pkg_name)
            current_branch = [line.split()[1] for line in branches.splitlines() if line.startswith('*')]
            current_branch = current_branch[0]

            # Checkout the gh-pages branch
            try:
                subprocess.check_call(['git', 'checkout', 'gh-pages'], cwd=ets_pkg_name)
            except (OSError, subprocess.CalledProcessError) as detail:
                print("   Error running command in package %s:\n   %s" % (ets_pkg_name, detail))
                input("   Press enter to process remaining packages.")
                continue

            # Copy the files over
            print("Copying files for {0}".format(ets_pkg_name))
            if ets_pkg_name == 'mayavi':
                copy_tree(ets_pkg_name + '/docs/build/tvtk/html/',   ets_pkg_name + '/tvtk/')
                copy_tree(ets_pkg_name + '/docs/build/mayavi/html/', ets_pkg_name + '/mayavi/')
            else:
                copy_tree(ets_pkg_name + '/docs/build/html/', ets_pkg_name)

            # Add everything to the repository
            try:
                subprocess.check_call(['git', 'add', '.'], cwd=ets_pkg_name)
            except (OSError, subprocess.CalledProcessError) as detail:
                print("   Error running command in package %s:\n   %s" % (ets_pkg_name, detail))
                input("   Press enter to process remaining packages.")
                continue

            # Commit to the repo.
            try:
                subprocess.check_call(['git', 'commit', '-a', '-m', '"Updated docs."'], cwd=ets_pkg_name)
            except (OSError, subprocess.CalledProcessError) as detail:
                print("   Error running command in package %s:\n   %s" % (ets_pkg_name, detail))
                input("   Press enter to process remaining packages.")
                continue

            # Push these changes.
            try:
                subprocess.check_call(['git', 'push'], cwd=ets_pkg_name)
            except (OSError, subprocess.CalledProcessError) as detail:
                print("   Error running command in package %s:\n   %s" % (ets_pkg_name, detail))
                input("   Press enter to process remaining packages.")
                continue

            # Return to the current branch
            try:
                subprocess.check_call(['git', 'checkout', current_branch], cwd=ets_pkg_name)
            except (OSError, subprocess.CalledProcessError) as detail:
                print("   Error running command in package %s:\n   %s" % (ets_pkg_name, detail))
                input("   Press enter to process remaining packages.")
                continue

            print

        return

    # Determine command from either alias or command line
    if arg1 in alias_dict:
        cmd = alias_dict[arg1] + sys.argv[2:]
        if cmd[0] == 'python':
            cmd[0] = sys.executable
    else:
        cmd = sys.argv[1:]

    # Run the command in each project directory
    for ets_pkg_name in ets_package_names.split():
        print("Running command %r in package %s" % (' '.join(cmd), ets_pkg_name))

        try:
            subprocess.check_call(cmd, cwd=ets_pkg_name + '/docs/')
            print
        except (OSError, subprocess.CalledProcessError) as detail:
            print("   Error running command in package %s:\n   %s" % (ets_pkg_name, detail))
            input("   Press enter to process remaining packages.")


if __name__ == "__main__":
    main()
