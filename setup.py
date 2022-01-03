from setuptools import setup
from setuptools import find_namespace_packages

# load the README file.
with open(file="README.md", mode="r") as fh:
    long_description = fh.read()

setup(
    # this will be my Library name.
    name='py-tda-api',

    # Want to make sure people know who made it.
    author='Alex Reed',

    # also an email they can use to reach out.
    author_email='coding.sigma@gmail.com',

    # Set the version.
    version='0.1.1',

    # here is a simple description of the library, this will appear when
    # someone searches for the library on https://pypi.org/search
    description='A python client lirbary for the TD Ameritrade API.',

    # I have a long description but that will just be my README file, note the
    # variable up above where I read the file.
    long_description=long_description,

    # want to make sure that I specify the long description as MARKDOWN.
    long_description_content_type="text/markdown",

    # here is the URL you can find the code, this is just the GitHub URL.
    url='https://github.com/areed1192/td-ameritrade-api',

    # there are some dependencies to use the library, so let's list them out.
    install_requires=[
        'requests>=2.24.0',
        'dataclasses>=0.6',
        'websockets>=9.1'
    ],

    # some keywords for my library.
    keywords='finance, td ameritrade, api',

    # here are the packages I want "build."
    packages=find_namespace_packages(
        include=['td.*'],
        exclude=['config*']
    ),

    include_package_data=True,

    # additional classifiers that give some characteristics about the package.
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],

    # you will need python 3.8 or greater to use this libary.
    python_requires='>=3.8'
)
