from unittest import TestCase
from unittest.mock import patch, MagicMock

from click.testing import CliRunner
from testfixtures import LogCapture

import guineabot.__main__ as main
import guineabot.age_logging as al


def _init_log_check(log_out: LogCapture, expected1: str, expected2: str, expected3: str, expected4: str) -> None:
    root = "root"
    log_level = al.logging.getLevelName(al.logging.INFO)
    log_out.check_present((root, log_level, expected1),
                          (root, log_level, expected2),
                          (root, log_level, expected3),
                          (root, log_level, expected4))


class TestMain(TestCase):

    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_help(self) -> None:
        result = self.runner.invoke(main.simulate_guinea_pig, ["--help"])
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
        result = self.runner.invoke(main.simulate_guinea_pig, ["--version"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("simulate-guinea-pig, version ", result.output)

    def test_invalid_name(self) -> None:
        result = self.runner.invoke(main.simulate_guinea_pig, ["--name", "AVeryLongForAGuineaPig"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("Error: Invalid value for '-n' / '--name': AVeryLongForAGuineaPig", result.output)

    def test_invalid_photos_folder(self) -> None:
        result = self.runner.invoke(main.simulate_guinea_pig, ["--photos-folder", "/path/to/nowhere"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("Error: Invalid value for '-p' / '--photos-folder': /path/to/nowhere", result.output)

    @patch("guineabot.__main__.create_guinea_pig")
    @patch("guineabot.__main__.create_tweeter")
    @patch("guineabot.__main__.build_guinea_pig_machine")
    def test_name(self,
                  build_guinea_pig_machine_mock: MagicMock,
                  create_tweeter: MagicMock,
                  create_guinea_pig_mock: MagicMock) -> None:
        with LogCapture(level=al.logging.INFO) as log_out:
            result = self.runner.invoke(main.simulate_guinea_pig, ["-n", "Bramble", "-d", "99"])
        self.assertEqual(result.exit_code, 0)
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
            result = self.runner.invoke(main.simulate_guinea_pig, ["-d", "99"])
        self.assertEqual(result.exit_code, 0)
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
            result = self.runner.invoke(main.simulate_guinea_pig, ["-i", "22", "-d", "99"])
        self.assertEqual(result.exit_code, 0)
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
            result = self.runner.invoke(main.simulate_guinea_pig, ["-a", "-d", "99"])
        self.assertEqual(result.exit_code, 0)
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
