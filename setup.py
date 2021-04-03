from setuptools import setup
from setuptools import find_namespace_packages

# Open the README file.
with open(file="README.md", mode="r") as fh:
    long_description = fh.read()

setup(

    name='',

    # Define Author Info.
    author='Alex Reed',
    author_email='coding.sigma@gmail.com',

    # Define Version Info.
    version='0.1.0',

    # Define descriptions.
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Define repo location.
    url='',

    # Define dependencies.
    install_requires=[],

    # Specify folder content.
    packages=find_namespace_packages(
        include=[]
    ),

    # Define the python version.
    python_requires='>3.7',

    # Define our classifiers.
    classifiers=[

        # Phase of development my library is in.
        'Development Status :: 3 - Alpha',

        # Audience this library is intended for.
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Financial and Insurance Industry',

        # License that guides my library.
        'License :: OSI Approved :: MIT License',

        # Package was written in English.
        'Natural Language :: English',

        # Operating systems.
        'Operating System :: OS Independent',

        # Programming Languages Used..
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        # Topics.
        'Topic :: Database',
        'Topic :: Education',
        'Topic :: Office/Business'
    ]

)
