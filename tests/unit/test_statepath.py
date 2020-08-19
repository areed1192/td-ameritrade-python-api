import pathlib
import unittest

from unittest import TestCase
from td.utils import StatePath


class StatePathSession(TestCase):

    """Will perform a unit test for the StatePath Object."""

    def setUp(self) -> None:
        """Set up the StatePath Instance."""

        self.state_path = StatePath()

    def test_creates_instance_of_session(self) -> None:
        """Create an instance and make sure it's a StatePath Object."""

        # Make sure it's a state path.
        self.assertIsInstance(self.state_path, StatePath)

        # make sure our default name matches.
        self.assertEqual(
            self.state_path.credenitals_file_name, 'td_state.json'
        )

        # Make sure the Credentials File is a Windows Path.
        self.assertIsInstance(
            self.state_path.credentials_file,
            pathlib.WindowsPath
        )

    def test_home_path(self) -> None:
        """Tests creating a homepath."""

        truth = pathlib.Path.home()
        self.assertEqual(truth, self.state_path.path_home())

    def test_home_directory(self) -> None:
        """Tests grabbing the home directory."""

        truth = pathlib.Path(__file__).parents[2].joinpath('td')
        self.assertEqual(truth, self.state_path.library_directory)

    def test_settings_directory(self) -> None:
        """Tests grabbing the settings directory."""

        truth = pathlib.Path().home().joinpath('.td_python_library')
        self.assertEqual(truth, self.state_path.settings_directory)

    def test_library_directory(self) -> None:
        """Tests grabbing the home directory."""

        truth = pathlib.Path.home()
        self.assertEqual(truth, self.state_path.home_directory)

    def test_json_library_path(self) -> None:
        """Test grabbing the Library JSON file path."""

        truth = pathlib.Path(__file__).parents[2].joinpath(
            'td/td_state.json'
        )
        self.assertEqual(truth, self.state_path.json_library_path())

    def test_json_setting_path(self) -> None:
        """Test grabbing the Setting JSON file path."""

        truth = pathlib.Path().home().joinpath('.td_python_library/td_state.json')

        self.assertEqual(truth, self.state_path.json_settings_path())

    def test_write_to_settings(self) -> None:
        """Test writing the credentials to Settings Folder."""

        # Set the fake name.
        self.state_path.credenitals_file_name = 'fake_td_state.json'

        # Determine our base.
        truth = pathlib.Path().home().joinpath('.td_python_library/fake_td_state.json')

        # Get the JSON settings paht.
        json_settings = self.state_path.json_settings_path()

        # Write the credentials.
        check = self.state_path.write_credentials(
            file_path=json_settings,
            state={'value': 'settings'}
        )

        # Make sure they are equal.
        self.assertEqual(truth, check)

    def test_write_to_library(self) -> None:
        """Test writing the credentials to Library Folder."""

        # Set the fake name.
        self.state_path.credenitals_file_name = 'fake_td_state.json'

        # Determine our base.
        truth = pathlib.Path(__file__).parents[2].joinpath(
            'td/fake_td_state.json'
        )

        # Get the JSON settings paht.
        json_settings = self.state_path.json_library_path()

        # Write the credentials.
        check = self.state_path.write_credentials(
            file_path=json_settings,
            state={'value': 'library'}
        )

        # Make sure they are equal.
        self.assertEqual(truth, check)

    def test_write_to_custom(self) -> None:
        """Test writing to a User Provided Path."""

        # Define the file path.
        file_path = 'config/td_state_custom.json'

        # Define the truth.
        truth = pathlib.Path(__file__).parents[2].joinpath(file_path)

        # Write and check.
        self.assertEqual(truth, self.state_path.write_credentials(
            file_path=file_path,
            state={'value': 'custom'}
        )
        )

    def test_read_from_settings(self) -> None:
        """Test writing the credentials to Settings Folder."""

        # Set the fake name.
        self.state_path.credenitals_file_name = 'fake_td_state.json'

        truth = {'value': 'settings'}

        file_path = self.state_path.json_settings_path()
        check = self.state_path.read_credentials(file_path=file_path)

        # Make sure they are equal.
        self.assertEqual(truth, check)

    def test_read_from_library(self) -> None:
        """Test writing the credentials to Library Folder."""

        # Set the fake name.
        self.state_path.credenitals_file_name = 'fake_td_state.json'

        truth = {'value': 'library'}

        file_path = self.state_path.json_library_path()

        check = self.state_path.read_credentials(file_path=file_path)

        self.assertEqual(truth, check)

    def test_read_from_custom(self) -> None:
        """Test writing to a User Provided Path."""

        truth = {'value': 'custom'}

        file_path = pathlib.Path('config/td_state_custom.json')

        check = self.state_path.read_credentials(file_path=file_path)

        # Make sure they are equal.
        self.assertEqual(truth, check)

    def test_read_from_non_exist(self) -> None:
        """Test writing to a User Provided Path."""

        truth = 'Credentials File does not exist.'
        file_path = pathlib.Path('config/no/td_state_custom.json')

        with self.assertRaises(FileNotFoundError) as context:
            self.state_path.read_credentials(file_path=file_path)

        # Make sure they are equal.
        self.assertEqual(truth, str(context.exception))

    def tearDown(self) -> None:
        """Teardown the StatePath Object."""

        self.state_path = None


if __name__ == '__main__':
    unittest.main()
