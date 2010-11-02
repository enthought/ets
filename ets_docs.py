#! /usr/bin/env python
"""A thin replacement for SetupDocs. Performs documentation building, check in, updating, etc of all actively 
maintained ETS packages.
"""

import sys
import os
import subprocess

usage = """\
Usage: ets_docs -h | --help | co | COMMAND [args] | ALIAS [args]
   -h, --help  Print this message.

   co          Check out the CEC projects directory into the current working
               directory. This is the repository for the live ETS website.
               Therefore, in order to update the website, you need a local
               checkout.

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

   Examples:
      Fresh install all packages from trunk:
         mkdir ETS
         cd ETS
         ets co
         ets install

      Update all packages from trunk:
         ets up

   The ETS packages referenced, in order of processing, are:%s
   """

aliases = """\n
      html     make html
      latex    make latex
      """ 
ets_package_names = """\n
      Traits             CodeTools          Chaco
      """


ets_url = "https://svn.enthought.com/svn/enthought/%s/trunk"
cec_url = "https://svn.enthought.com/svn/cec/trunk/"

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

    # Checkout 'projects/' dir
    if arg1 == 'co':
        print "Checking out projects documentation directory" 
        subprocess.check_call(['svn', 'co', cec_url + 'projects/', 'projects/'])
        return 

    # Determine command from either alias or command line
    if arg1 in alias_dict:
        cmd = alias_dict[arg1] + sys.argv[2:]
        if cmd[0] == 'python':
            cmd[0] = sys.executable
    else:
        cmd = sys.argv[1:]

    # Run the command
    for ets_pkg_name in ets_package_names.split():
        print "Running command %r in package %s" % (' '.join(cmd), ets_pkg_name)
        
        try:
            subprocess.check_call(cmd, cwd=ets_pkg_name + '/docs/')
            print
        except (OSError, subprocess.CalledProcessError), detail:
            print "   Error running command in package %s:\n   %s" % (ets_pkg_name, detail)
            raw_input("   Press enter to process remaining packages.")


if __name__ == "__main__":
    main()
