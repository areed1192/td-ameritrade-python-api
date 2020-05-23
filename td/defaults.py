import os
import sys
import json
import pathlib

from typing import Any
from typing import Dict
from typing import List
from typing import Union
from typing import Optional

# if sys.version_info >= (3, 5):
#     home_dir = str(pathlib.Path.home())
# else:
#     home_dir = os.path.expanduser('~')

# default_dir = os.path.join(home_dir, '.tdunofficial')

class StatePath(type(pathlib.Path())):

    def __init__(self, credentials_file: str = None):

        """Initalizes the StatePath Class"""        
        self.python_version = sys.version_info
        self.credenitals_file_name = 'td_state.json'
        self.settings_location = {}

        if credentials_file and isinstance(credentials_file, str):
            self.credentials_file: pathlib.Path = pathlib.Path(credentials_file)
        else:
            self.credentials_file: pathlib.Path = self.library_directory
    
    @property
    def get_file_path(self):

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
            json.dump(obj=state,fp=credenitals_file)

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
            json.dump(obj=state,fp=credenitals_file)

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

        file_path.unlink()

    def define_settings_location(self, location_id:str, location: str) -> pathlib.Path:

        new_path = pathlib.Path(location)

        self.settings_location[location_id] = new_path

        return new_path


if __name__ == '__main__':

    state_path = StatePath()
    state_path.write_to_settings(state={'value':'key'})
