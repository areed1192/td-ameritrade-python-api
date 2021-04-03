from configparser import ConfigParser

# Initialize the Parser.
config = ConfigParser()

# Read the file.
config.read('configs/config.ini')

# Get the specified credentials.
config.get('main', '')
