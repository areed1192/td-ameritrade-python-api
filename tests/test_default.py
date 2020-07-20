from td.defaults import StatePath

my_path = StatePath()
print(my_path.get_file_path)
print(my_path.json_settings_path())
print(my_path.json_library_path())

print(my_path.credentials_file.is_file())
print(my_path.credentials_file.is_dir())