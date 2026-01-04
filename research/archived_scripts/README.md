# Archived Research Scripts

This directory contains research scripts that have been archived due to outdated dependencies on non-existent code structures.

## Reason for Archival

These scripts were archived on 2026-01-04 because they import from `examples_hooks_submission/`, a directory structure that no longer exists in the current codebase.

## Archived Scripts

The following 11 scripts have been moved here:

1. `compare_guardrails.py` - Root level comparison script
2. `compare_guardrails.py` - Scripts directory comparison script
3. `compare_guardrails_openai.py` - OpenAI-based guardrail comparison
4. `test_collaborative_multiagent.py` - Collaborative multi-agent testing
5. `test_ensemble_diversity_scaling.py` - Ensemble diversity scaling tests
6. `test_ensemble_diversity_scaling_guardrail.py` - Guardrail-specific ensemble tests
7. `test_ensemble_vs_enhanced.py` - Ensemble vs enhanced comparison
8. `test_negative_rewards.py` - Negative rewards testing
9. `test_seed_sensitivity.py` - Seed sensitivity analysis
10. `run_comprehensive_experiments.py` - Comprehensive experiment runner
11. `collect_all_experimental_data.py` - Experimental data collection

## Current Code Structure

The current codebase uses:
- `examples/guardrails/` for guardrail examples
- `examples/attacks/` for attack examples
- `aicomp_sdk/guardrails/` for core guardrail functionality
- `aicomp_sdk/attacks/` for core attack functionality

## Restoration

To restore these scripts, the imports would need to be updated to reference the current code structure:
- Change `examples_hooks_submission/` imports to appropriate paths in `examples/` or `aicomp_sdk/`
- Verify all referenced modules and classes exist in the current codebase
- Update any deprecated API calls to match the current SDK

## Historical Context

These scripts were part of earlier research experiments that predated the current package reorganization. They may contain valuable research insights but require significant refactoring to work with the current codebase.
