# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest import TestCase

from ..venv import Venv
from ..util import update_os_environ

current_runtime = '{}.{}'.format(*sys.version_info[:2])


class TestVenv(TestCase):

    def test_init(self):
        with TemporaryDirectory() as tempdir:
            with update_os_environ({'ETS_VENV_PATH': tempdir}):
                env = Venv("test", current_runtime)

                self.assertEqual(env.environment, "test")
                self.assertEqual(env.runtime, current_runtime)

    def test_create_clean(self):
        with TemporaryDirectory() as tempdir:
            with update_os_environ({'ETS_VENV_PATH': tempdir}):
                env = Venv("test", current_runtime)
                env.create()

                self.assertEqual(env.environment, "test")
                self.assertEqual(env.runtime, current_runtime)

                path = Path(tempdir, 'test')

                self.assertTrue(path.exists())
                self.assertTrue(path.is_dir())

                env.clean()

                self.assertFalse(path.exists())

    def test_install(self):
        with TemporaryDirectory() as tempdir:
            with update_os_environ({'ETS_VENV_PATH': tempdir}):
                env = Venv("test", current_runtime)
                env.create()

                path = Path(tempdir, 'test')

                self.assertTrue(path.exists())
                self.assertTrue(path.is_dir())

                env.clean()

                self.assertFalse(path.exists())
