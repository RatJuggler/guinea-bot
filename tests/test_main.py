from unittest import TestCase
from click.testing import CliRunner

import guineabot.__main__ as main


class TestMain(TestCase):

    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_help(self) -> None:
        result = self.runner.invoke(main.simulate_guinea_pig, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(" --version ", result.output)
        self.assertIn(" -a, --accelerated ", result.output)
        self.assertIn(" -d, --duration ", result.output)
        self.assertIn(" -i, --interval ", result.output)
        self.assertIn(" -l, --log-level ", result.output)
        self.assertIn(" -n, --name ", result.output)
        self.assertIn(" -p, --photos-folder ", result.output)
        self.assertIn(" -q, --quiet ", result.output)
        self.assertIn(" --help ", result.output)

    # TODO: Requires "python3 setup.py sdist" to have been run to pass, review.
    def test_version(self) -> None:
        result = self.runner.invoke(main.simulate_guinea_pig, ['--version'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("simulate-guinea-pig, version ", result.output)
