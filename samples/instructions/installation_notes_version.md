# Versioning Conventions

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

## Running `pip install` in development mode

```bash
pip install -e "C:\Users\Alex\OneDrive\Desktop\Sigma\Repo - TD API Client\td-ameritrade-python-api"
```

## Creating a `Requirement.txt` file

Install `pipreqs`

```console
pip install pipreqs
```

Run `pipreqs`

```console
pipreqs "td-ameritrade-python-api\td"
```
