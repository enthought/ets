#! /usr/bin/env python
"""A thin replacement for SetupDocs (which is no longer part of ETS).
Performs documentation building, check in, updating, etc of all actively 
maintained ETS packages.
"""

import sys
import os
import subprocess
from distutils.dir_util import copy_tree

usage = """\
Usage: ets_docs -h | --help | co | cp | ru [username] | COMMAND [args] | ALIAS [args]
   -h, --help  Print this message.

   co          Check out the CEC projects directory into the current working
               directory. This is the repository for the live ETS website.
               Therefore, in order to update the website, you need a local
               checkout.

   cp          Copies the documentation from the various build directories
               to the local code.enthought.com repsository.

   ru          This command performs a 'remote update', ie it updates the 
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
        ets_docs co     # Checkout documentation repository
        ets_docs html   # Generate new HTML docs
        ets_docs cp     # Copy over new docs to local repo
        ets_docs status # See which files changed
        ets_docs commit -m 'A commit message'
        ets_docs ru     # Update the website with the commit


   The ETS packages referenced, in order of processing, are:\n%s
   """

aliases = """\n
      html     make html
      latex    make latex
      up       svn up
      add      svn add
      status   svn status
      commit   svn commit
      update   svn update
      """

project_aliases = """html latex"""

repository_aliases = """up add status commit update"""
 
ets_package_names = """\
      enthoughtbase      traits             codetools
      traitsgui          etsdevtools        scimath
      traitsbackendqt    traitsbackendwx    enable
      apptools           envisagecore       envisageplugins
      chaco              mayavi             blockcanvas
      """

ets_url = "https://svn.enthought.com/svn/enthought/%s/trunk"
cec_url = "https://svn.enthought.com/svn/cec/trunk/"
cec_dir = "projects/"

html_dirs = """\
    EnthoughtBase/docs/build/html/      projects/enthought_base/docs/html/
    Traits/docs/build/html/             projects/traits/docs/html/
    CodeTools/docs/build/html/          projects/code_tools/docs/html/
    TraitsGUI/docs/build/html/          projects/traits_gui/docs/html/
    ETSDevTools/docs/build/html/        projects/ets_dev_tools/docs/html/
    SciMath/docs/build/html/            projects/sci_math/docs/html/
    TraitsBackendQt/docs/build/html/    projects/traits_backend_qt/docs/html/
    TraitsBackendWX/docs/build/html/    projects/traits_backend_wx/docs/html/
    Enable/docs/build/html/             projects/enable/docs/html/
    AppTools/docs/build/html/           projects/app_tools/docs/html/
    EnvisageCore/docs/build/html/       projects/envisage/docs/html/
    Chaco/docs/build/html/              projects/chaco/docs/html/
    Mayavi/docs/build/mayavi/html/      projects/mayavi/docs/development/html/mayavi/
    Mayavi/docs/build/tvtk/html/        projects/mayavi/docs/development/html/tvtk/
    BlockCanvas/docs/build/html/        projects/block_canvas/docs/html/"""

alias_dict = {}
for line in aliases.split('\n'):
    tokens = line.split()
    if tokens:
         alias_dict[tokens[0]] = tokens[1:]

def copy_html_docs():
    n = 0
    for line in html_dirs.splitlines():
        ls = line.split()

        if n == 0:
            n += 1
        else:
            print
        print "Copying documentation from %s to %s" % (ls[0], ls[1])

        ct = copy_tree(*ls)
        #for f in ct: 
        #    print f

def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith('-'):
        print usage % (aliases, ets_package_names)
        return

    arg1 = sys.argv[1]

    # Checkout 'projects/' dir
    if arg1 == 'co':
        print "Checking out projects documentation directory" 
        subprocess.check_call(['svn', 'co', cec_url + cec_dir, cec_dir])
        return 
    # Copy documentation
    elif arg1 == 'cp':
        copy_html_docs()
        return
    # Update the remote server 
    elif arg1 == 'ru':
        rucmd = ['ssh', 'www.enthought.com', "'cd /www/htdocs/code/%s; svn up'" % cec_dir]

        if len(sys.argv) == 3:
            rucmd[1] = sys.argv[2] + '@' + rucmd[1]

        print "Running command %r" % (' '.join(rucmd))
        try:
            subprocess.check_call(" ".join(rucmd), shell=True)
        except:
            pass
        return

    # Determine command from either alias or command line
    if arg1 in alias_dict:
        cmd = alias_dict[arg1] + sys.argv[2:]
        if cmd[0] == 'python':
            cmd[0] = sys.executable
    else:
        cmd = sys.argv[1:]

    # Run the command in each project directory
    if arg1 in project_aliases.split():
        for ets_pkg_name in ets_package_names.split():
            print "Running command %r in package %s" % (' '.join(cmd), ets_pkg_name)
        
            try:
                subprocess.check_call(cmd, cwd=ets_pkg_name + '/docs/')
                print
            except (OSError, subprocess.CalledProcessError), detail:
                print "   Error running command in package %s:\n   %s" % (ets_pkg_name, detail)
                raw_input("   Press enter to process remaining packages.")

    # Run the command only in repository directory
    else:
        print "Running command %r in %s" % (' '.join(cmd), cec_dir)
        subprocess.check_call(cmd, cwd=cec_dir)
        

if __name__ == "__main__":
    main()
