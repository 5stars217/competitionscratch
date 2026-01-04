# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-03

### Added
- Initial PyPI-ready release
- Reorganized package structure with proper submodules:
  - `aicomp_sdk.core`: Core SDK functionality (env, tools, trace, predicates)
  - `aicomp_sdk.agents`: Agent implementations (OpenAI agent)
  - `aicomp_sdk.guardrails`: Guardrail system with hooks API
  - `aicomp_sdk.attacks.baselines`: Baseline attack algorithms
  - `aicomp_sdk.utils`: Utility functions
- Complete Go-Explore implementation with snapshot/restore
- Advanced hooks API for custom attack and defense strategies
- Simple hooks API for easier development
- Dual competition format (attack + defense scoring)
- Comprehensive test suite
- Example implementations for guardrails and attacks
- Full documentation in `docs/` directory
- PyPI packaging configuration:
  - `setup.py` with proper metadata
  - `pyproject.toml` for modern Python packaging
  - `MANIFEST.in` for including data files
  - MIT License
  - Updated `.gitignore` for Python development

### Changed
- Restructured repository for production readiness
- Moved all tests to `tests/` directory
- Moved all examples to `examples/` directory
- Consolidated documentation to `docs/` directory
- Archived research artifacts to `research/` directory

### Fixed
- Import paths updated for new package structure
- Package discovery configuration for clean PyPI distribution

## [Unreleased]

### Planned
- Additional baseline algorithms
- Enhanced documentation with Sphinx
- Performance optimizations
- Extended API documentation
- More example implementations
