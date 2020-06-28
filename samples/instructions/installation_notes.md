# TD Ameritrade Installation

Current PyPi Test Version - 0.2.1
Current PyPi Version - 0.3.0

Once we build our TD Ameritrade library we are probably going to want and distribute it so other people can use it. Now at this point I think it pays to define some terms before we continue. To start out, I will be referrring to my `td` client as a package. A `package`, is simply a collection of python modules. A `module` is simply a python script. Technically we have another level, a library. A `library` is a colleciton of various packages, however, conceptually there is no difference between a library and a package.

## The Goal

At the end of this process I want to be able to bundle all my python modules and any other resources together, package them using the `setuptools` module, and upload that pacakge to `pypi` so that other users can install it on their systems.

## The Steps

To reach our end goal, we need to do te following steps:

1. Create `setup.py` file.
2. Create a `MANIFEST.in` file.
3. Install `setuptools`, if we already don't have it.
4. Install `twine`, if we already don't have it.
5. Build our project using `setuptools`.
6. Upload our project to `pypi` using the `twine` module.

### Step 1: Create `setup.py` File

First part of the installation process is creating our setup.py file. The `setup.py` file is the centre of all activity in building, distributing, and installing modules using the `setuptools`. The main purpose of the setup script is to describe your module distribution to the `setuptools`, so that the various commands that operate on your modules do the right thing. The setup script consists mainly of a call to `setup()`, and most information supplied to the `setuptools` by the module developer is supplied as keyword arguments to `setup()`. Below, I provide an example of what I put inside my `setup.py` file along with what each item is specifying in the process.

```python
from setuptools import setup, find_packages

# I want my readme to be part of the setup, so let's read it.
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(

      # this will be my Library name.
      name='td-ameritrade-python-api',

      # Want to make sure people know who made it.
      author='Alex Reed',

      # also an email they can use to reach out.
      author_email='coding.sigma@gmail.com',

      # I'm in alpha development still, so a compliant version number is a1.
      # read this as MAJOR VERSION 0, MINOR VERSION 1, MAINTENANCE VERSION 0
      version='0.1.0',

      # here is a simple description of the library, this will appear when someone searches for the library on https://pypi.org/search
      description='A python client lirbary for the TD Ameritrade API.',

      # I have a long description but that will just be my README file, note the variable up above where I read the file.
      long_description=long_description,

      # want to make sure that I specify the long description as MARKDOWN.
      long_description_content_type="text/markdown",

      # here is the URL you can find the code, this is just the GitHub URL.
      url='https://github.com/areed1192/td-ameritrade-python-api',

      # there are some dependencies to use the library, so let's list them out.
      install_reqs = [
            'websockets==8.0.2',
            'requests==2.22.0'
      ],

      # some keywords for my library.
      keywords = 'finance, td ameritrade, api',

      # here are the packages I want "build."
      packages=find_packages(include = ['td']),

      # I also have some package data, like photos and JSON files, so I want to include those too.
      include_package_data=True,

      # additional classifiers that give some characteristics about the package.
      classifiers=[

            # I want people to know it's still early stages.
           'Development Status :: 3 - Alpha',

            # My Intended audience is mostly those who understand finance.
           'Intended Audience :: Financial and Insurance Industry',

           # My License is MIT.
           'License :: OSI Approved :: MIT License',

           # I wrote the client in English
           'Natural Language :: English',

           # The client should work on all OS.
           'Operating System :: OS Independent',

           # The client is intendend for PYTHON 3
           'Programming Language :: Python :: 3'
      ],

      # you will need python 3.7 to use this libary.
      python_requires='>=3.7'

     )
```

### Step 2: Create a MANIFEST file

In my `setup()` function above, I specifed a very important argument that designated I wanted to include additional files in my installation. When I specified the `include_package_data=True` argument, I told the `setuptools` module that I have extra data files I want to include in the proces. However, I never specified what files I wanted to include, so to specify the files I want I need to create something called a MANIFEST file. The MANIFEST file is used to specify what files you want included in the package during the installation. Inside of my MANIFEST file I have the following:

```python
# file GENERATED by distutils, do NOT edit
include setup.py
include td/client.py
include td/enums.py
include td/fields.py
include td/option_chain.py
include td/orders.py
include td/stream.py
include td/watchlist_item.py

# I want all my sample files.
recursive-include samples *

# Do not want my config file.
global-exclude td/config.py
```

### Step3: Install `setuptools`

We will be using the `setuptools` module to package our modules. If you don't have have `setuptools` installed you'll need to install it. To install it, run the following command in your console.

```console
pip install setuptools wheel
```

if you already have you'll want to make sure you're on the latest version, so make sure to update it using the following commands:

```console
pip install --upgrade setuptools wheel
```

### Step 4: Install `twine`

Twine is the primary tool developers use to upload packages to the Python Package Index or other Python package indexes. It is a command-line program that passes program files and metadata to a web API. Developers use it because it’s the official PyPI upload tool, it’s fast and secure, it’s maintained, and it reliably works. To install `twine`, run the following command:

```console
pip install twine
```

if you already have ir you'll want to make sure you're on the latest version, so make sure to update it using the following commands:

```console
pip install --upgrade twine
```

### Step 5: Build our Distribution Package

Now that we have everything installed, we can build or distribution package. To build our distribution pacakge run the following command:

```console
python setup.py sdist bdist_wheel
```

This will generate a distrubtion archives in the _dist_ folder. In fact, if you look in your directory you should see a few new folders one called _dist_ and one called _build_. These were generated when we ran the command.

### Step 6: Upload our Distribution Pacakge to PyPi test Index

Before you run this command you need to have an account registered with PyPi, to register an account go to this [link](https://test.pypi.org/account/register). After you register your account you'll want an access token so that way you can upload distribtions to the index.

To upload the distribution run the following command:

```console
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

```console
twine upload --repository testpypi --config-file pypirc dist/*
```

```console
twine upload --repository pypi --config-file pypirc dist/*
```

You will be prompted to enter your `username` and `password` once you've done that you should see similar output as seen below:

```console
Uploading distributions to https://test.pypi.org/legacy/
Enter your username: [your username]
Enter your password:
Uploading example_pkg_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
100%|█████████████████████| 4.65k/4.65k [00:01<00:00, 2.88kB/s]
Uploading example_pkg_YOUR_USERNAME_HERE-0.0.1.tar.gz
100%|█████████████████████| 4.25k/4.25k [00:01<00:00, 3.05kB/s]
```

Alternatively, if you don't want to enter your username and password, then you can use your access token instead. However, to use your access token set `username` to `__token__` and for the `password` use the `token_value` including the `pypi-` prefix. Here is how it would look:

```console
Uploading distributions to https://test.pypi.org/legacy/
Enter your username: __token__
Enter your password: pypi-<MY_ACCESS_TOKEN>
Uploading example_pkg_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
100%|█████████████████████| 4.65k/4.65k [00:01<00:00, 2.88kB/s]
Uploading example_pkg_YOUR_USERNAME_HERE-0.0.1.tar.gz
100%|█████████████████████| 4.25k/4.25k [00:01<00:00, 3.05kB/s]
```

Once uploaded your package should be viewable on TestPyPI, for example, <https://test.pypi.org/project/example-pkg-YOUR-USERNAME-HERE>

### Step 7: Install the newly uploaded package

You can use pip to install your package and verify that it works. To install your package you would run the following command in your console:

```console
pip install --index-url https://test.pypi.org/simple/ example_pkg
```

pip should install the package from Test PyPI and the output should look something like this:

```console
Collecting example-pkg-YOUR-USERNAME-HERE
  Downloading https://test-files.pythonhosted.org/packages/.../example-pkg-YOUR-USERNAME-HERE-0.0.1-py3-none-any.whl
Installing collected packages: example-pkg-YOUR-USERNAME-HERE
Successfully installed example-pkg-YOUR-USERNAME-HERE-0.0.1
```

```console
pip show td-ameritrade-python-api
```

### Step 8: Test that the package was installed correctly

You can test that it was installed correctly by importing the package. Run the Python interpreter and from the interpreter shell import the package. Here is how it will look:

```python
python

>>> import example_pkg
```
