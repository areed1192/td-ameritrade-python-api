import datetime
import os
import sys
import json
import pathlib

from typing import Any
from typing import Dict
from typing import List
from typing import Union
from typing import Optional


class StatePath(type(pathlib.Path())):

    def __init__(self, credentials_file: str = None):
        """Initalizes the `StatePath` Class object."""

        self.credenitals_file_name = 'td_state.json'
        self.settings_location = {}

        if credentials_file and isinstance(credentials_file, str):
            self.credentials_file: pathlib.Path = pathlib.Path(
                credentials_file
            )
        else:
            self.credentials_file: pathlib.Path = self.library_directory

    @property
    def get_file_path(self) -> str:
        """Resolves the file path.

        Returns:
        ----
        (str): A file path reprsented as a string.
        """        

        return self.credentials_file.absolute()

    def path_home(self) -> pathlib.PurePath:
        """Determines the user's Home Path using Pathlib.

        Returns:
        ----
        {pathlib.PurePath} -- A PurePath object that points to
            the user's home directory.
        """

        home_directory = pathlib.Path.home()
        return home_directory

    @property
    def home_directory(self) -> pathlib.PurePath:
        """Returns the Home directory path.

        Returns:
        ----
        {pathlib.PurePath} -- A path object.
        """
        return self.path_home()

    @property
    def library_directory(self) -> pathlib.PurePath:
        """Returns the TD Library directory path.

        Returns:
        ----
        {pathlib.PurePath} -- A path object.
        """
        return self.path_library()

    @property
    def settings_directory(self) -> pathlib.PurePath:
        """Returns the `.td_python_library` directory path.

        Returns:
        ----
        {pathlib.PurePath} -- A path object.
        """
        return self.path_settings()

    def path_library(self) -> pathlib.PurePath:
        """Generates the TD Library Path.

        Returns:
        ----
        {pathlib.PurePath} -- A PurePath object pointing to the TD
            library.
        """
        library_directory = pathlib.Path(__file__).parent
        return library_directory

    def path_settings(self) -> pathlib.PurePath:
        """Generates a path to the `.td_python_library` directory.

        Returns:
        ----
        {pathlib.PurePath} -- A PurePath object pointing to the `.td_python_library` 
            directory.
        """
        self.home_directory
        settings_directory = self.home_directory.joinpath('.td_python_library')
        return settings_directory

    def json_settings_path(self):
        """Generates a path to the `.td_python_library/td_state.json` file.

        Returns:
        ----
        {pathlib.PurePath} -- A PurePath object pointing to the
             `.td_python_library/td_state.json` file.
        """
        return self.settings_directory.joinpath(self.credenitals_file_name)

    def json_library_path(self):
        """Generates a path to the `td/td_state.json` file.

        Returns:
        ----
        {pathlib.PurePath} -- A PurePath object pointing to the
             `td/td_state.json` file.
        """
        return self.library_directory.joinpath(self.credenitals_file_name)

    @property
    def does_credentials_file_exist(self):
        """Sepcifies whether the passed through credentials file exists."""

        return self.credentials_file.exists()

    def does_file_exist(self, file_path: pathlib.Path) -> bool:
        """Checks if a file exists.

        Arguments:
        ----
        file_path {pathlib.Path} -- A path to a specific file.

        Returns:
        ----
        bool -- `True` if it exists, `False` if it does not exist.
        """
        return file_path.exists()

    def does_directory_exist(self, file_path: pathlib.Path) -> bool:
        """Checks if a directory exists.

        This takes a file path and checks if folder that the file is supposed
        to exist in exists. It only does one level up.

        Arguments:
        ----
        file_path {pathlib.Path} -- A path to a specific directory.

        Returns:
        ----
        bool -- `True` if it exists, `False` if it does not exist.
        """

        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path).absolute()
            directory = file_path
        else:
            file_path = file_path.absolute()
            directory = file_path.parent

        # See if it exists
        return directory.exists()

    def write_to_settings(self, state: dict) -> pathlib.Path:
        """Writes the credentials to the Settigns folder.

        Arguments:
        ----
        state {dict} -- The session state dictionary.

        Returns:
        ----
        pathlib.Path -- The path to credentials path.
        """

        json_settings_path = self.json_settings_path()

        # Check to see if the folder exists.
        if not self.does_directory_exist(file_path=json_settings_path):
            json_settings_path.parent.mkdir()

        # write to the JSON file.
        with open(file=json_settings_path, mode='w+') as credenitals_file:
            json.dump(obj=state, fp=credenitals_file)

        return json_settings_path

    def write_credentials(self, file_path: Union[pathlib.Path, str], state: dict) -> pathlib.Path:
        """Writes the credentials to the Settigns folder.

        Arguments:
        ----
        file_path {Union[pathlib.Path, str]} -- The path to the credentials file.

        state {dict} -- The session state dictionary.

        Returns:
        ----
        pathlib.Path -- The path to credentials path.
        """

        if isinstance(file_path, str):
            json_path = pathlib.Path(file_path).absolute()
        else:
            json_path = file_path.absolute()

        # Check to see if the folder exists.
        if not self.does_directory_exist(file_path=json_path):
            json_path.parent.mkdir()

        # write to the JSON file.
        with open(file=json_path, mode='w+') as credenitals_file:
            json.dump(obj=state, fp=credenitals_file)

        return json_path

    def read_credentials(self, file_path: Union[pathlib.Path, str]) -> dict:
        """Read the credentials file.

        Arguments:
        ----
        file_path {Union[pathlib.Path, str]} -- The path to the credentials file.

        Returns:
        ----
        {dict} -- The session state dictionary.
        """

        # Handle the file path input.
        if isinstance(file_path, str):
            json_path = pathlib.Path(file_path).absolute()
        else:
            json_path = file_path.absolute()

        # Check to see if the folder exists.
        if not self.does_directory_exist(file_path=json_path):
            raise FileNotFoundError("Credentials File does not exist.")

        # read the JSON file.
        with open(file=json_path, mode='r') as credenitals_file:
            state_dict = json.load(fp=credenitals_file)

        return state_dict

    def set_path(self, path: str) -> None:
        """Sets the path to credentials file.

        Arguments:
        ----
        path {str} -- The path to set.
        """
        self._credentials_full_path = path

    def delete_credentials(self, file_path: pathlib.Path) -> None:
        """Deletes the credential File.

        Arguments:
        ----
        file_path (pathlib.Path): [description]
        """        

        file_path.unlink()

    def define_settings_location(self, location_id: str, location: str) -> pathlib.Path:
        """Used to set a custom settings location.

        Args:
        ----
        location_id (str): The ID You want associated with this location.

        location (str): The file path to the settings file.

        Returns:
        ----
        pathlib.Path: A Pathlib object representing the file location.
        """        

        new_path = pathlib.Path(location)

        self.settings_location[location_id] = new_path

        return new_path


class TDUtilities():

    def milliseconds_since_epoch(self, dt_object: datetime.datetime) -> int:
        """converts a datetime object to milliseconds since 1970, as an integer

        Arguments:
        ----------
        dt_object {datetime.datetime} -- Python datetime object.

        Returns:
        --------
        [int] -- The timestamp in milliseconds since epoch.
        """

        return int(dt_object.timestamp() * 1000)

    def datetime_from_milliseconds_since_epoch(self, ms_since_epoch: int, timezone: datetime.timezone = None) -> datetime.datetime:
        """Converts milliseconds since epoch to a datetime object.

        Arguments:
        ----------
        ms_since_epoch {int} -- Number of milliseconds since epoch.

        Keyword Arguments:
        --------
        timezone {datetime.timezone} -- The timezone of the new datetime object. (default: {None})

        Returns:
        --------
        datetime.datetime -- A python datetime object.
        """

        return datetime.datetime.fromtimestamp((ms_since_epoch / 1000), tz=timezone)
