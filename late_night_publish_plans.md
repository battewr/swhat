# Publishing swhat to PyPI

## Current Status

The `pyproject.toml` is **nearly ready** for publishing.

### What's Already Configured

| Field | Status | Value |
|-------|--------|-------|
| name | Done | `swhat` |
| version | Done | `0.3.2` |
| description | Done | Specification-driven development CLI... |
| readme | Done | `README.md` |
| license | Done | `MIT` |
| requires-python | Done | `>=3.10` |
| authors | Done | `swhat contributors` |
| keywords | Done | cli, specification, ai, development, planning |
| classifiers | Done | Alpha, Console, MIT, Python 3.10-3.12 |
| dependencies | Done | `click>=8.0` |
| scripts | Done | `swhat = swhat.cli:main` |
| build-system | Done | hatchling |

### What's Missing

Add `project.urls` to `pyproject.toml`:

```toml
[project.urls]
Homepage = "https://github.com/battewr/swhat"
Repository = "https://github.com/battewr/swhat"
Issues = "https://github.com/battewr/swhat/issues"
```

Optional: Add email to authors:
```toml
authors = [
    { name = "swhat contributors", email = "your@email.com" }
]
```

---

## Prerequisites

1. **PyPI account**: Register at https://pypi.org/account/register/
2. **API token**: Create at https://pypi.org/manage/account/token/
   - Scope: Entire account (for first upload) or project-specific (after first upload)

---

## Publishing Steps

### Step 1: Add Project URLs

Edit `pyproject.toml` and add the `[project.urls]` section shown above.

### Step 2: Build Distribution Packages

```bash
# Using UV (recommended)
uv build

# This creates:
#   dist/swhat-0.3.2-py3-none-any.whl
#   dist/swhat-0.3.2.tar.gz
```

### Step 3: Test on TestPyPI First (Recommended)

```bash
# Upload to TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/

# When prompted, use:
#   Username: __token__
#   Password: your-testpypi-api-token

# Test the install
uv pip install --index-url https://test.pypi.org/simple/ swhat

# Verify it works
swhat --version
swhat --help
```

### Step 4: Publish to Real PyPI

```bash
# Upload to PyPI
uv publish

# When prompted, use:
#   Username: __token__
#   Password: your-pypi-api-token
```

### Step 5: Verify

```bash
# Install from PyPI
uv pip install swhat

# Or with pip
pip install swhat
```

---

## Credential Storage (Optional)

To avoid entering credentials each time, create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-REAL-PYPI-TOKEN

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN
```

Set permissions: `chmod 600 ~/.pypirc`

---

## Alternative: Using Twine Directly

```bash
# Install twine
uv pip install twine

# Check package before upload
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

---

## Version Bumping for Future Releases

Before each release:

1. Update version in `src/swhat/__init__.py`
2. Update version in `pyproject.toml`
3. Commit and tag: `git tag v0.3.3`
4. Build and publish

---

## Checklist

- [ ] Add `[project.urls]` to pyproject.toml
- [ ] Create PyPI account
- [ ] Create PyPI API token
- [ ] Create TestPyPI account (optional but recommended)
- [ ] Create TestPyPI API token (optional)
- [ ] Run `uv build`
- [ ] Test on TestPyPI
- [ ] Publish to PyPI
- [ ] Verify installation works: `uv pip install swhat`
