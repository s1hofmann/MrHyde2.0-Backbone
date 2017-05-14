import unittest

from app.main.executable.bundle.bundle import Bundle
from app.main.executable.jekyll.jekyll import Jekyll


class BundleTest(unittest.TestCase):
    def test_exec(self):
        j = Jekyll()
        b = Bundle()
        self.assertListEqual(b.
                             exec(j).cmd, ["bundle", "exec", "jekyll", "build"])

    def test_install(self):
        b = Bundle()
        self.assertListEqual(b.install().cmd, ["bundle", "install"])

    def test_update(self):
        b = Bundle()
        self.assertListEqual(b.update().cmd, ["bundle", "update"])


if __name__ == "__main__":
    unittest.main()
