import unittest

from app.executable import Executable
from app.executable.jekyll import Jekyll, JekyllError


class JekyllTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple(self):
        j = Jekyll()
        self.assertListEqual(j.cmd, ["jekyll", "build"])

    def test_add_parameter_string(self):
        j = Jekyll()

        j.add_parameter("test")
        self.assertListEqual(j.cmd, ["jekyll", "build", "test"])

    def test_add_parameter_key_value(self):
        j = Jekyll()

        j.add_parameter("--source", "./")
        self.assertListEqual(j.cmd, ["jekyll", "build", "--source", "./"])

    def test_add_parameter_executable(self):
        j = Jekyll()
        e = Executable("test", "executable", "with", "parameters")

        j.add_parameter(e)
        self.assertListEqual(j.cmd, ["jekyll", "build"] + e.cmd)

    def test_executable_error(self):
        e = Jekyll(source="test")
        with self.assertRaises(JekyllError) as context:
            e.call()

        self.assertTrue(context.exception.return_code == 1)
