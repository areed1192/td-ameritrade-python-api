import pathlib
import subprocess

JUST_BUILD = True

# Grab the current working directory.
current_dir = pathlib.Path().cwd().as_posix()

# Run Build.
build_result = subprocess.Popen(
    'python setup.py sdist bdist_wheel', cwd=current_dir
)

# Wait till we have the results.
build_result.wait()

# Only uploaded if needed.
if JUST_BUILD == False:

    # Upload to TestPyPi.
    upload_test_result = subprocess.Popen(
        'twine upload -r testpypi dist/*', cwd=current_dir
    )

    # Wait till we have the results.
    upload_test_result.wait()

    # Upload to TestPyPi.
    upload_result = subprocess.Popen(
        'twine upload dist/*', cwd=current_dir
    )

    # Wait till we have the results.
    upload_result.wait()
