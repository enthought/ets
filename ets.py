#! /usr/bin/env python
"""A thin replacement for ETSProjectTools. Performs checkout, update, install,
build, etc, of all actively maintained ETS packages, and allows arbitrary
shell commands to be run on all packages.
"""

import sys
import subprocess

usage = """\
Usage: ets -h | --help | clone [--ssh] | COMMAND [args] | ALIAS [args]
   -h, --help  Print this message.

   clone       Clone the entire Enthought Tool Suite into the current working
               directory, each actively maintained package placed in its own
               sub-directory.
               By default, the https github access URLs are used.
               The --ssh option changes this to SSH.

   COMMAND     Run this shell command, with any following arguments, inside
               each package's sub-directory. If any command arguments must be
               quoted, you may need to use nested quotes, depending on the
               quote handling in your shell. For example:
                  ets git commit -a -m "'commit comment for all packages'"

   ALIAS       Each alias is shorthand for a shell command with arguments.
               The available aliases are pre-defined by this script, not by
               the user. Any alias may be followed by optional additional
               arguments.


   The available aliases and their equivalent commands are:%s

   Examples:
      Fresh install all packages from master:
         mkdir ETS
         cd ETS
         ets clone
         ets develop

      Update all packages from master:
         ets pull

   The ETS packages referenced, in order of processing, are:\n%s"""

aliases = """\n
      pull     git pull
      status   git status
      branch   git branch
      checkout git checkout
      diff     git diff
      revert   git revert
      fetch    git fetch
      setup    python setup.py
      build    python setup.py build
      install  python setup.py install
      develop  python setup.py develop"""

"""\
======================================================================
ETS installation dependencies (documentation only).
Derived from ets_dependends.log, holding the output of ets_depends.py.
Dependent packages are listed below and to the right of their dependencies.
======================================================================
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

Notes:
1.  * BlockCanvas's multiple dependencies are listed individually.
2. This string is for documentation only. Unlike the ets_package_names string
   below, this  is not used programatically. However, string ets_package_names
   *is* manually derived from the info in this string.
3. This string does not list ETS run-time, nor any non-ETS, dependencies.
4. To avoid clutter, this string does not list redundant dependencies. For
   example, it does not list Traits or EnthoughtBase dependencies for packages
   which depend on TraitsGUI, because TraitsGUI itself depends on both of these.
"""


ets_package_names = """\
      traits             pyface             traitsui
      codetools          etsdevtools        scimath
      enable             apptools           envisage
      chaco              mayavi             graphcanvas
      blockcanvas        etsproxy"""

ets_ssh = "git@github.com:enthought/%s.git"
ets_https = "https://github.com/enthought/%s.git"

alias_dict = {}
for line in aliases.split('\n'):
    tokens = line.split()
    if tokens:
         alias_dict[tokens[0]] = tokens[1:]


def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith('-'):
        print usage % (aliases, ets_package_names)
        return

    arg1 = sys.argv[1]
    clone = bool(arg1 == 'clone')

    if not clone:
        if arg1 in alias_dict:
            cmd = alias_dict[arg1] + sys.argv[2:]
            if cmd[0] == 'python':
                cmd[0] = sys.executable
        else:
            cmd = sys.argv[1:]

    for ets_pkg_name in ets_package_names.split():
        if clone:
            print "Cloning package %s" % ets_pkg_name
            if '--ssh' in sys.argv:
                pkg_url = ets_ssh % ets_pkg_name
            else:
                pkg_url = ets_https % ets_pkg_name
            print "URL: %s" % pkg_url
            subprocess.check_call(['git', 'clone', pkg_url, ets_pkg_name])
        else:
            print "Running command %r in package %s" % (cmd, ets_pkg_name)
            try:
                subprocess.check_call(cmd, cwd=ets_pkg_name)
            except (OSError, subprocess.CalledProcessError), detail:
                print "   Error running command in package %s:\n   %s" % (
                                      ets_pkg_name, detail)
                raw_input("   Press enter to process remaining packages.")

        print

if __name__ == "__main__":
    main()
