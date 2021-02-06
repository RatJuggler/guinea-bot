from unittest import TestCase
from unittest.mock import patch, MagicMock

from click.testing import CliRunner
from testfixtures import LogCapture

from tests.utils import log_check

from guineabot.age_logging import configure_logging, logging

import guineabot.__main__ as main


class TestMain(TestCase):

    def setUp(self) -> None:
        configure_logging()
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
        with LogCapture(level=logging.INFO) as log_out:
            result = self.runner.invoke(main.simulate_guinea_pig, ['-n', 'Bramble', '-d', '99'])
        self.assertEqual(0, result.exit_code)
        log_check(log_out,
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
        with LogCapture(level=logging.INFO) as log_out:
            result = self.runner.invoke(main.simulate_guinea_pig, ['-d', '99'])
        self.assertEqual(0, result.exit_code)
        log_check(log_out,
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
        with LogCapture(level=logging.INFO) as log_out:
            result = self.runner.invoke(main.simulate_guinea_pig, ['-i', '22', '-d', '99'])
        self.assertEqual(0, result.exit_code)
        log_check(log_out,
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
        with LogCapture(level=logging.INFO) as log_out:
            result = self.runner.invoke(main.simulate_guinea_pig, ['-d', '99', '-a'])
        self.assertEqual(0, result.exit_code)
        log_check(log_out,
                  "INITIALISE >> Booting guinea pig 'Holly'...",
                  "INITIALISE >> Accelerated running, quiet mode enforced.",
                  "INITIALISE >> Bot duration (guinea pig lifespan): 99 days",
                  "INITIALISE >> State interval (changes in guinea pig activity): 15 minutes",
                  "INITIALISE >> It's alive!")
        create_guinea_pig_mock.assert_called_once()
        create_tweeter.assert_called_once()
        build_guinea_pig_machine_mock.assert_called_once()

    @patch("guineabot.__main__.TwitterServiceLive")
    def test_test(self,
                  twitter_service_live_mock: MagicMock) -> None:
        result = self.runner.invoke(main.simulate_guinea_pig, ['-t'])
        self.assertEqual(0, result.exit_code)
        twitter_service_live_mock.assert_called_once()

    def test_test_fail(self) -> None:
        result = self.runner.invoke(main.simulate_guinea_pig, ['-t'])
        self.assertEqual(1, result.exit_code)
        self.assertEqual("Unable to connect to the Twitter API, access token 'TWITTER_CONSUMER_KEY' not found!",
                         result.exception.code)
