# CI/CD Workflows Documentation

This directory contains GitHub Actions workflows for the `aicomp_sdk` project, providing automated testing, code quality checks, and PyPI publishing.

## 📋 Table of Contents

- [Overview](#overview)
- [Workflows](#workflows)
- [Setup Instructions](#setup-instructions)
- [Release Process](#release-process)
- [Running Tests Locally](#running-tests-locally)
- [Troubleshooting](#troubleshooting)
- [Status Badges](#status-badges)

## 🔍 Overview

The CI/CD pipeline consists of three main workflows:

1. **`ci.yml`** - Continuous Integration (testing)
2. **`lint.yml`** - Code quality and linting checks
3. **`publish.yml`** - Automated PyPI publishing on releases

All workflows are triggered automatically on pushes and pull requests to ensure code quality and prevent regressions.

## 🔄 Workflows

### 1. CI Workflow (`ci.yml`)

**Triggers:**
- Push to `main`, `master`, or `develop` branches
- Pull requests targeting these branches

**Jobs:**
- **Test Matrix**: Runs tests on Python 3.9, 3.10, and 3.11
- **Unit Tests**: Executes `pytest tests/unit/` with coverage reporting
- **Integration Tests**: Runs non-OpenAI integration tests
- **Coverage Reports**: Generates and uploads coverage artifacts
- **Package Build**: Verifies the package can be built successfully

**Key Features:**
- Dependency caching for faster builds
- Coverage reports in XML and HTML formats
- Codecov integration (optional)
- Parallel testing across Python versions

### 2. Lint Workflow (`lint.yml`)

**Triggers:**
- Push to `main`, `master`, or `develop` branches
- Pull requests targeting these branches

**Jobs:**
- **Linting**: Runs `flake8` for Python code quality
- **Formatting**: Checks code formatting with `black`
- **Import Sorting**: Verifies imports are sorted with `isort`
- **Type Checking**: Runs `mypy` for static type analysis
- **Security Checks**: Uses `bandit` to detect security issues
- **Code Complexity**: Analyzes complexity with `radon`
- **Additional Quality**: Runs `pylint` for comprehensive checks
- **Documentation**: Validates docstrings with `pydocstyle`

**Quality Gate:**
- The workflow must pass all critical linting checks
- Some checks are non-blocking (e.g., mypy, bandit) for gradual adoption

### 3. Publish Workflow (`publish.yml`)

**Triggers:**
- Tags matching `v*.*.*` pattern (e.g., `v1.0.0`, `v0.1.5`)

**Jobs:**
1. **Build Package**: Creates source distribution and wheel
2. **Publish to PyPI**: Uploads package using PyPI API token
3. **Create GitHub Release**: Generates release notes and attaches artifacts
4. **Notification**: Reports success/failure status

**Features:**
- Automatic changelog extraction
- GitHub Release creation with artifacts
- Version extraction from git tags
- Secure publishing with API tokens

## ⚙️ Setup Instructions

### Prerequisites

Before using these workflows, ensure you have:

1. A GitHub repository with the `aicomp_sdk` code
2. PyPI account and API token
3. Admin access to the repository (for secrets)

### Step 1: Set Up PyPI API Token

1. **Create a PyPI API Token:**
   - Go to [PyPI Account Settings](https://pypi.org/manage/account/)
   - Navigate to "API tokens" section
   - Click "Add API token"
   - Give it a descriptive name (e.g., "GitHub Actions - aicomp_sdk")
   - Select scope: "Entire account" or specific to `aicomp-sdk` project
   - Copy the generated token (starts with `pypi-`)

2. **Add Token to GitHub Secrets:**
   - Go to your GitHub repository
   - Navigate to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your PyPI API token
   - Click "Add secret"

### Step 2: Configure Trusted Publishing (Optional, Recommended)

For enhanced security, you can use PyPI's trusted publishing:

1. Go to your project on PyPI
2. Navigate to "Publishing" settings
3. Add GitHub as a trusted publisher:
   - Owner: Your GitHub username/org
   - Repository: `aicomp-sdk`
   - Workflow: `publish.yml`
   - Environment: `pypi`

If using trusted publishing, you can remove the `password` field from the publish step in [`publish.yml`](.github/workflows/publish.yml:82).

### Step 3: Verify Workflows

1. Make a small change to trigger CI:
   ```bash
   git checkout -b test-ci
   echo "# Test" >> README.md
   git add README.md
   git commit -m "test: Verify CI workflows"
   git push origin test-ci
   ```

2. Open a pull request and check:
   - CI workflow runs successfully
   - Lint workflow passes all checks
   - Status checks appear on the PR

## 🚀 Release Process

Follow these steps to publish a new version to PyPI:

### 1. Update Version

Edit [`pyproject.toml`](../../pyproject.toml:7) and update the version:

```toml
[project]
name = "aicomp-sdk"
version = "1.1.0"  # Update this
```

### 2. Update Changelog (Optional but Recommended)

Add release notes to [`CHANGELOG.md`](../../CHANGELOG.md):

```markdown
## [1.1.0] - 2026-01-03

### Added
- New feature X
- Support for Y

### Fixed
- Bug in Z component

### Changed
- Improved performance of A
```

### 3. Commit Changes

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore: Bump version to 1.1.0"
git push origin main
```

### 4. Create and Push Tag

```bash
# Create annotated tag
git tag -a v1.1.0 -m "Release version 1.1.0"

# Push tag to trigger publish workflow
git push origin v1.1.0
```

### 5. Monitor Workflow

1. Go to Actions tab in GitHub
2. Watch the "Publish to PyPI" workflow
3. Verify successful completion
4. Check [PyPI](https://pypi.org/project/aicomp-sdk/) for the new version
5. Verify the GitHub Release was created

### Tagging Strategy

- **Major releases**: `v1.0.0`, `v2.0.0` (breaking changes)
- **Minor releases**: `v1.1.0`, `v1.2.0` (new features)
- **Patch releases**: `v1.0.1`, `v1.0.2` (bug fixes)
- **Pre-releases**: `v1.0.0-alpha.1`, `v1.0.0-beta.2` (optional)

## 🧪 Running Tests Locally

### Install Development Dependencies

```bash
# Clone the repository
git clone https://github.com/yourusername/aicomp-sdk.git
cd aicomp-sdk

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package with dev dependencies
pip install -e ".[dev]"
```

### Run Unit Tests

```bash
# Run all unit tests with coverage
pytest tests/unit/ -v --cov=aicomp_sdk --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_scoring.py -v

# Run with verbose output
pytest tests/unit/ -vv
```

### Run Integration Tests

```bash
# Run all integration tests (excluding OpenAI)
pytest tests/integration/ -v -k "not openai"

# Run specific integration test
pytest tests/integration/test_baseline_defense.py -v
```

### Run Linting

```bash
# Run flake8
flake8 aicomp_sdk --max-line-length=127 --statistics

# Check formatting with black
black --check aicomp_sdk

# Format code with black
black aicomp_sdk

# Check imports with isort
isort --check-only aicomp_sdk

# Fix imports with isort
isort aicomp_sdk

# Run type checking
mypy aicomp_sdk
```

### Run All Quality Checks

```bash
# Create a script to run all checks
cat > check_all.sh << 'EOF'
#!/bin/bash
set -e

echo "🔍 Running flake8..."
flake8 aicomp_sdk --max-line-length=127

echo "🎨 Checking formatting..."
black --check aicomp_sdk

echo "📦 Checking imports..."
isort --check-only aicomp_sdk

echo "🔎 Running mypy..."
mypy aicomp_sdk || true

echo "🧪 Running tests..."
pytest tests/unit/ -v --cov=aicomp_sdk

echo "✅ All checks passed!"
EOF

chmod +x check_all.sh
./check_all.sh
```

### Build Package Locally

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Check package
twine check dist/*

# Test installation
pip install dist/aicomp_sdk-*.whl
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. CI Tests Failing Locally Pass

**Problem**: Tests pass locally but fail in CI

**Solutions:**
- Check Python version compatibility (CI tests on 3.9, 3.10, 3.11)
- Verify all dependencies are in `pyproject.toml`
- Check for environment-specific assumptions
- Look for race conditions in tests

```bash
# Test with specific Python version
python3.9 -m pytest tests/

# Run tests in clean environment
python -m venv clean_env
source clean_env/bin/activate
pip install -e ".[dev]"
pytest tests/
```

#### 2. PyPI Publishing Fails

**Problem**: "403 Forbidden" or authentication errors

**Solutions:**
- Verify `PYPI_API_TOKEN` secret is set correctly
- Ensure token has correct permissions
- Check if package name is available on PyPI
- Verify version doesn't already exist

```bash
# Test authentication locally
twine upload --repository testpypi dist/* --verbose
```

#### 3. Coverage Reports Not Generated

**Problem**: Coverage artifacts missing

**Solutions:**
- Ensure `pytest-cov` is installed
- Check pytest configuration in `pyproject.toml`
- Verify coverage commands in workflow

```bash
# Generate coverage locally
pytest tests/unit/ --cov=aicomp_sdk --cov-report=html
# Open htmlcov/index.html to view
```

#### 4. Linting Failures

**Problem**: Black or flake8 complains about formatting

**Solutions:**
- Run formatters locally before pushing
- Configure pre-commit hooks
- Check line length settings

```bash
# Auto-fix formatting
black aicomp_sdk
isort aicomp_sdk

# Then commit
git add .
git commit -m "style: Fix formatting"
```

#### 5. Type Checking Errors

**Problem**: mypy reports type errors

**Solutions:**
- Add type hints gradually
- Use `# type: ignore` for complex cases
- Update mypy configuration in `pyproject.toml`

```bash
# Check specific file
mypy aicomp_sdk/scoring.py

# Generate type stub files
stubgen -p aicomp_sdk -o stubs
```

#### 6. Workflow Permissions Error

**Problem**: "Resource not accessible by integration"

**Solutions:**
- Check repository Settings → Actions → General
- Enable "Read and write permissions" for GITHUB_TOKEN
- Verify workflow permissions section

#### 7. Cache Not Working

**Problem**: Dependencies reinstalled every time

**Solutions:**
- Verify `cache: 'pip'` is set in setup-python action
- Check if `requirements.txt` or `pyproject.toml` changed
- Clear cache manually in Actions settings

### Getting Help

If you encounter issues not covered here:

1. **Check workflow logs**: Actions tab → Select failed workflow → View logs
2. **Review GitHub Actions docs**: https://docs.github.com/en/actions
3. **Check PyPI publishing guide**: https://packaging.python.org/
4. **Open an issue**: Describe the problem with workflow logs

## 📊 Status Badges

Add these badges to your README.md to display workflow status:

```markdown
# aicomp-sdk

![CI](https://github.com/yourusername/aicomp-sdk/workflows/CI/badge.svg)
![Code Quality](https://github.com/yourusername/aicomp-sdk/workflows/Code%20Quality/badge.svg)
[![PyPI version](https://badge.fury.io/py/aicomp-sdk.svg)](https://badge.fury.io/py/aicomp-sdk)
[![Python Versions](https://img.shields.io/pypi/pyversions/aicomp-sdk.svg)](https://pypi.org/project/aicomp-sdk/)
[![codecov](https://codecov.io/gh/yourusername/aicomp-sdk/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/aicomp-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

Replace `yourusername` with your actual GitHub username or organization.

## 📝 Additional Configuration Files

### Markdown Link Checker Config

Create `.github/markdown-link-check-config.json` for the docs check:

```json
{
  "ignorePatterns": [
    {
      "pattern": "^http://localhost"
    }
  ],
  "timeout": "20s",
  "retryOn429": true,
  "retryCount": 3,
  "fallbackRetryDelay": "30s"
}
```

### Pre-commit Hooks (Optional)

Install pre-commit hooks to run checks before each commit:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
EOF

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

## 🎯 Best Practices

1. **Always run tests locally** before pushing
2. **Keep workflows fast** by using caching
3. **Use semantic versioning** for releases
4. **Write meaningful commit messages** following conventional commits
5. **Update CHANGELOG.md** before releases
6. **Monitor workflow runs** and fix failures promptly
7. **Keep dependencies updated** regularly
8. **Use branch protection rules** requiring status checks

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)

---

**Last Updated**: 2026-01-03  
**Maintained by**: Competition Organizers
