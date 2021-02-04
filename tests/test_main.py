from unittest import TestCase
from unittest.mock import patch, MagicMock

from click.testing import CliRunner
from testfixtures import LogCapture

import guineabot.__main__ as main
import guineabot.age_logging as al


def _init_log_check(log_out: LogCapture, *expects: str) -> None:
    root = "root"
    log_level = al.logging.getLevelName(al.logging.INFO)
    for expected in expects:
        log_out.check_present((root, log_level, expected))


class TestMain(TestCase):

    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_help(self) -> None:
        result = self.runner.invoke(main.simulate_guinea_pig, ['--help'])
        self.assertEqual(0, result.exit_code)
        self.assertIn(" --version ", result.output)
        self.assertIn(" -n, --name ", result.output)
        self.assertIn(" -h, --house ", result.output)
        self.assertIn(" -p, --photos ", result.output)
        self.assertIn(" -d, --duration ", result.output)
        self.assertIn(" -i, --interval ", result.output)
        self.assertIn(" -a, --accelerated ", result.output)
        self.assertIn(" -l, --log-level ", result.output)
        self.assertIn(" -q, --quiet ", result.output)
        self.assertIn(" -t, --test ", result.output)
        self.assertIn(" --help ", result.output)

    # TODO: Requires "python3 setup.py sdist" to have been run to pass, review.
    def test_version(self) -> None:
        result = self.runner.invoke(main.simulate_guinea_pig, ['--version'])
        self.assertEqual(0, result.exit_code)
        self.assertIn("simulate-guinea-pig, version ", result.output)

    def test_invalid_name(self) -> None:
        result = self.runner.invoke(main.simulate_guinea_pig, ['--name', 'AVeryLongForAGuineaPig'])
        self.assertEqual(2, result.exit_code)
        self.assertIn("Error: Invalid value for '-n' / '--name': AVeryLongForAGuineaPig", result.output)

    def test_invalid_house(self) -> None:
        result = self.runner.invoke(main.simulate_guinea_pig, ['--house', '/path/to/nowhere'])
        self.assertEqual(2, result.exit_code)
        self.assertIn("Error: Invalid value for '-h' / '--house': Directory '/path/to/nowhere' does not exist.", result.output)

    def test_invalid_photos(self) -> None:
        result = self.runner.invoke(main.simulate_guinea_pig, ['--photos', '/path/to/nowhere'])
        self.assertEqual(2, result.exit_code)
        self.assertIn("Error: Invalid value for '-p' / '--photos': Directory '/path/to/nowhere' does not exist.", result.output)

    @patch("guineabot.__main__.create_guinea_pig")
    @patch("guineabot.__main__.create_tweeter")
    @patch("guineabot.__main__.build_guinea_pig_machine")
    def test_name(self,
                  build_guinea_pig_machine_mock: MagicMock,
                  create_tweeter: MagicMock,
                  create_guinea_pig_mock: MagicMock) -> None:
        with LogCapture(level=al.logging.INFO) as log_out:
            result = self.runner.invoke(main.simulate_guinea_pig, ['-n', 'Bramble', '-d', '99'])
        self.assertEqual(0, result.exit_code)
        _init_log_check(log_out,
                        "INITIALISE >> Booting guinea pig 'Bramble'...",
                        "INITIALISE >> Bot duration (guinea pig lifespan): 99 days",
                        "INITIALISE >> State interval (changes in guinea pig activity): 15 minutes",
                        "INITIALISE >> It's alive!")
        create_guinea_pig_mock.assert_called_once()
        create_tweeter.assert_called_once()
        build_guinea_pig_machine_mock.assert_called_once()

    @patch("guineabot.__main__.create_guinea_pig")
    @patch("guineabot.__main__.create_tweeter")
    @patch("guineabot.__main__.build_guinea_pig_machine")
    def test_duration(self,
                      build_guinea_pig_machine_mock: MagicMock,
                      create_tweeter: MagicMock,
                      create_guinea_pig_mock: MagicMock) -> None:
        with LogCapture(level=al.logging.INFO) as log_out:
            result = self.runner.invoke(main.simulate_guinea_pig, ['-d', '99'])
        self.assertEqual(0, result.exit_code)
        _init_log_check(log_out,
                        "INITIALISE >> Booting guinea pig 'Holly'...",
                        "INITIALISE >> Bot duration (guinea pig lifespan): 99 days",
                        "INITIALISE >> State interval (changes in guinea pig activity): 15 minutes",
                        "INITIALISE >> It's alive!")
        create_guinea_pig_mock.assert_called_once()
        create_tweeter.assert_called_once()
        build_guinea_pig_machine_mock.assert_called_once()

    @patch("guineabot.__main__.create_guinea_pig")
    @patch("guineabot.__main__.create_tweeter")
    @patch("guineabot.__main__.build_guinea_pig_machine")
    def test_interval(self,
                      build_guinea_pig_machine_mock: MagicMock,
                      create_tweeter: MagicMock,
                      create_guinea_pig_mock: MagicMock) -> None:
        with LogCapture(level=al.logging.INFO) as log_out:
            result = self.runner.invoke(main.simulate_guinea_pig, ['-i', '22', '-d', '99'])
        self.assertEqual(0, result.exit_code)
        _init_log_check(log_out,
                        "INITIALISE >> Booting guinea pig 'Holly'...",
                        "INITIALISE >> Bot duration (guinea pig lifespan): 99 days",
                        "INITIALISE >> State interval (changes in guinea pig activity): 22 minutes",
                        "INITIALISE >> It's alive!")
        create_guinea_pig_mock.assert_called_once()
        create_tweeter.assert_called_once()
        build_guinea_pig_machine_mock.assert_called_once()

    @patch("guineabot.__main__.create_guinea_pig")
    @patch("guineabot.__main__.create_tweeter")
    @patch("guineabot.__main__.build_guinea_pig_machine")
    def test_accelerated(self,
                         build_guinea_pig_machine_mock: MagicMock,
                         create_tweeter: MagicMock,
                         create_guinea_pig_mock: MagicMock) -> None:
        with LogCapture(level=al.logging.INFO) as log_out:
            result = self.runner.invoke(main.simulate_guinea_pig, ['-d', '99', '-a'])
        self.assertEqual(0, result.exit_code)
        _init_log_check(log_out,
                        "INITIALISE >> Booting guinea pig 'Holly'...",
                        "INITIALISE >> Bot duration (guinea pig lifespan): 99 days",
                        "INITIALISE >> State interval (changes in guinea pig activity): 15 minutes",
                        "INITIALISE >> It's alive!")
        log_out.check_present(("root", al.logging.getLevelName(al.logging.INFO),
                               "INITIALISE >> Accelerated running, quiet mode enforced."))
        create_guinea_pig_mock.assert_called_once()
        create_tweeter.assert_called_once()
        build_guinea_pig_machine_mock.assert_called_once()

    @patch("guineabot.__main__.TwitterServiceLive")
    def test_test(self,
                  twitter_service_live_mock: MagicMock) -> None:
        result = self.runner.invoke(main.simulate_guinea_pig, ['-t'])
        self.assertEqual(0, result.exit_code)
        twitter_service_live_mock.assert_called_once()
