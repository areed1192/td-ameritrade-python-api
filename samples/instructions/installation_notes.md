# TD Ameritrade Installation

## Step 1: Create `setup.py` File

First part of the installation process is creating our setup.py file.

```python
from distutils.core import setup

setup(name='TD Ameritrade API',
      version='1.0.0',
      description='A python client lirbary for the TD Ameritrade API.',
      author='Alex Reed',
      author_email='coding.sigma@gmail.com',
      url='https://github.com/areed1192/td-ameritrade-python-api',
      packages=['td'],
      platform='win32',
      install_reqs = parse_requirements('requirements.txt', session='hack')
     )
```

## Step 2: Run `pip install` in Development Mode

```bash
pip install -e "C:\Users\Alex\OneDrive\Desktop\Sigma\Repo - TD API Client\td-ameritrade-python-api"
```

## Versioning Notes

```python
1.2.0.dev1  # Development release
1.2.0a1     # Alpha Release
1.2.0b1     # Beta Release
1.2.0rc1    # Release Candidate
1.2.0       # Final Release
1.2.0.post1 # Post Release
15.10       # Date based release
23          # Serial release
```

pipreqs "C:\Users\Alex\OneDrive\Desktop\Sigma\Repo - TD API Client\td-ameritrade-python-api\td"