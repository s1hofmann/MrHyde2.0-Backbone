import unittest

from app.executable import Executable, ExecutableError


class ExecutableTest(unittest.TestCase):
    def test_single_cmd(self):
        e = Executable("test", "param1", "param2")
        self.assertListEqual(e.cmd, ["test", "param1", "param2"])

    def test_nested_cmd(self):
        e = Executable("test", "param1", "param2")
        f = Executable("wrapper", "around", e)
        self.assertListEqual(f.cmd, ["wrapper", "around"] + e.cmd)

    def test_add_arguments(self):
        e = Executable("test", "param1", "param2")
        e.add_parameter("param3")
        self.assertListEqual(e.cmd, ["test", "param1", "param2", "param3"])

    def test_executable_error(self):
        e = Executable("test")
        with self.assertRaises(ExecutableError) as context:
            e.call()

        self.assertTrue(context.exception.return_code == 1)

    def test_call_success(self):
        date = Executable("date")
        self.assertTrue(date.call().return_code() == 0)

    def test_call_bundle(self):
        jekyll = Executable("jekyll")
        bundle = Executable("bundle", "exec", jekyll)
        self.assertListEqual(bundle.cmd, ["bundle", "exec"] + jekyll.cmd)


if __name__ == "__main__":
    unittest.main()
