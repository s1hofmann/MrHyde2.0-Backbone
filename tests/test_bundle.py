import unittest

from app.executable.bundle import Bundle
from app.executable.jekyll import Jekyll


class BundleTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_exec(self):
        j = Jekyll()
        b = Bundle()
        self.assertListEqual(b.exec(j).cmd, ["bundle", "exec", "jekyll", "build"])

    def test_install(self):
        b = Bundle()
        self.assertListEqual(b.install().cmd, ["bundle", "install"])

    def test_install_twice(self):
        b = Bundle()
        b.install()
        self.assertListEqual(b.install().cmd, ["bundle", "install"])

    def test_switch_commands(self):
        b = Bundle()
        b.install()
        self.assertListEqual(b.update().cmd, ["bundle", "update"])

    def test_update(self):
        b = Bundle()
        self.assertListEqual(b.update().cmd, ["bundle", "update"])

    def test_update_twice(self):
        b = Bundle()
        b.update()
        self.assertListEqual(b.update().cmd, ["bundle", "update"])
