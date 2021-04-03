from configparser import ConfigParser

# Initialize the Parser.
config = ConfigParser()

# Add the Section.
config.add_section('main')

# Set the Values.
config.set('main', 'api_key', '')

# Write the file.
with open(file='configs/config.ini', mode='w+') as f:
    config.write(f)
