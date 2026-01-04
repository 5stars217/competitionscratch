# Comprehensive Fix Plan - Critical Issues

**Created**: 2026-01-04  
**Priority Order**: Critical issues first, then high-impact, then cleanup

---

## Executive Summary

This plan addresses 8 critical issues found in the codebase that cause:
- **Runtime failures** (broken imports)
- **Documentation mismatches** (missing tools, wrong constants, inconsistent API)
- **Logic inconsistencies** (untrusted source handling)
- **Configuration conflicts** (evaluation parameters)

### Top 3 Most Critical Issues (Fix Immediately)

1. **Issue #7** - Broken imports in compare_guardrails.py (BLOCKS EXECUTION)
2. **Issue #2** - Broken import in attacker_goexplore.py (BLOCKS EXECUTION)
3. **Issue #4** - Scoring constant mismatch 200000 vs 400 (BREAKS FAIRNESS)

---

## PRIORITY 1: CRITICAL (Blocks Execution)

### Issue #7: Broken Import in compare_guardrails.py

**Impact**: File cannot execute - ImportError on missing `examples_hooks_submission` module

**Root Cause**: References non-existent directory `examples_hooks_submission/`. Only `examples/` exists.

**Affected Files**:
- `compare_guardrails.py` (lines 16-17)
- `scripts/compare_guardrails_openai.py` (lines 16-17)
- `scripts/compare_guardrails.py` (lines 19-20)
- `scripts/find_shell_chains.py` (line 17)
- `scripts/find_exfil_chains.py` (lines 16-17)
- `scripts/find_secret_read_chains.py` (lines 16-17)
- `scripts/find_delete_chains.py` (lines 16-17)
- `scripts/collect_all_experimental_data.py` (lines 22-23)
- `scripts/run_comprehensive_experiments.py` (lines 47-48)
- `scripts/test_ensemble_diversity_scaling_guardrail.py` (line 20)
- `run_attack_openai.py` (line 282)

**Fix Option A (Recommended)**: Remove/archive broken scripts
- These appear to be research/experimental scripts referencing old structure
- Move to `research/archived_scripts/` if they have historical value
- Files: All scripts/* files listed above, plus root-level `compare_guardrails.py`

**Fix Option B**: Update imports to use correct paths
- Change `examples_hooks_submission` → `examples/guardrails` or `examples/attacks`
- But note: Some referenced files don't exist (e.g., `guardrail_prompt_injection.py`, `attack_working.py`)
- Would need to verify each import path individually

**Recommendation**: **Option A** - Archive broken scripts. These reference non-existent files and aren't part of the core SDK.

---

### Issue #2: Broken Import in attacker_goexplore.py

**Impact**: Import fails if `tests/` directory structure doesn't have `test_verify_findings.py` at root level

**Current Code** (`aicomp_sdk/attacks/baselines/attacker_goexplore.py:12-14`):
```python
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tests"))
try:
    from test_verify_findings import detect_real_attacks
```

**Problem**: Assumes `tests/test_verify_findings.py`, but file is at `tests/integration/test_verify_findings.py`

**Fix**:

**File**: `aicomp_sdk/attacks/baselines/attacker_goexplore.py`

**Lines 12-14** - REPLACE:
```python
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tests"))
try:
    from test_verify_findings import detect_real_attacks
```

**WITH**:
```python
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tests" / "integration"))
try:
    from test_verify_findings import detect_real_attacks
```

**Alternative Fix** (more robust):
```python
# Import from tests.integration without path manipulation
try:
    from tests.integration.test_verify_findings import detect_real_attacks
```

---

## PRIORITY 2: CRITICAL (Breaks Competition Fairness)

### Issue #4: Scoring Constant Mismatch

**Impact**: Documentation shows wrong values, misleads competitors about scoring

**Current State**:
- **Code** (`aicomp_sdk/scoring.py:17`): `ATTACK_ELITE_RAW = 200000.0`
- **Code** (`aicomp_sdk/scoring.py:16`): `ATTACK_BASELINE_RAW = 100000.0`
- **Docs**: Multiple files show `400.0` and `200.0`

**Analysis**:
- Code value of 200000.0 is intentional (aspirational target for vulnerable agent)
- Code comments on lines 8-23 explain: "These are ASPIRATIONAL TARGETS, not actual agent performance"
- Docs were written for different calibration (200/400 raw scores)

**Fix**: Update ALL documentation to match code constants

**Affected Documentation Files**:

1. **docs/SCORING.md**
   - Line 212: Change `ATTACK_ELITE_RAW = 400.0` → `ATTACK_ELITE_RAW = 200000.0`
   - Line 213: Update normalization formula context
   - Line 416-418: Update example calculation

2. **docs/SCORING_CHANGES.md**
   - Line 13: Change `ATTACK_BASELINE_RAW = 200.0` → `ATTACK_BASELINE_RAW = 100000.0`
   - Line 14: Change `ATTACK_ELITE_RAW = 400.0` → `ATTACK_ELITE_RAW = 200000.0`
   - Line 21: Update normalization formula reference
   - Line 117-118: Update constants in code example
   - Line 135-136: Update calibration example

3. **docs/API_REFERENCE.md**
   - Line 933: Change `ATTACK_BASELINE_RAW = 200.0` → `ATTACK_BASELINE_RAW = 100000.0`
   - Line 934: Change `ATTACK_ELITE_RAW = 400.0` → `ATTACK_ELITE_RAW = 200000.0`

**Important Note**: Also verify that `SCORING_FINAL_NOTES.md` is correct (lines 32-33 already show 100000/200000 - these are CORRECT).

---

## PRIORITY 3: HIGH (Documentation Mismatch)

### Issue #1: Missing Tools (fs.list, http.get)

**Impact**: Documentation references tools that don't exist, confuses users

**Current State**:
- `aicomp_sdk/core/tools.py` implements 9 tools
- Missing: `fs.list`, `http.get`
- Found 15 references across 7 documentation files

**Decision Required**: Implement tools OR remove from docs?

**Recommendation**: **Remove from documentation** (simpler, maintains current behavior)

**Rationale**:
- `fs.list` overlaps with `shell.run("ls")` (line 165 in tools.py already implements ls)
- `http.get` not needed - competition focuses on `http.post` for exfiltration
- No code currently uses these tools
- Implementing them adds attack surface without clear benefit

**Affected Documentation Files**:

1. **docs/DOCS_OUTLINE.md**
   - Line 361: Remove `fs.list` from tool list
   - Line 362: Remove `http.get` from tool list

2. **docs/GETTING_STARTED.md**
   - Line 111: Remove `http.get` row from table
   - Line 187: Remove `http.get` from list
   - Line 214: Remove `fs.list(path)` line
   - Line 217: Remove `http.get(url)` line

3. **docs/README.md**
   - Line 187: Change `http.get, http.post` → just `http.post`
   - Line 214-217: Remove `fs.list` and `http.get` examples

4. **docs/API_REFERENCE.md**
   - Lines 446-467: Remove entire `fs.list` section
   - Lines 471-492: Remove entire `http.get` section

5. **docs/GUARDRAILS_GUIDE.md**
   - Line 314: Remove `http.get` from list (keep http.post, web.open)
   - Line 434: Remove `http.get` from untrusted sources list
   - Line 660: Remove `http.get` from tainted source list
   - Line 1167: Remove `http.get` from untrusted sources list

6. **docs/ATTACKS_GUIDE.md**
   - Line 530: Remove `http.get` from untrusted source list

7. **docs/FIXTURE_GENERATION_REPORT.md**
   - Line 338: Remove `http.get()` row from table

**Alternative**: If implementing tools is preferred, see Appendix A for implementation details.

---

### Issue #3: Context Key Inconsistency

**Impact**: Documentation doesn't match runtime API, user code will fail

**Current State**:
- **Runtime uses**: `last_user` (5 files)
- **Docs reference**: `last_user_message` (17 references across 7 docs)

**Root Cause**: API was renamed but docs weren't updated

**Decision**: Change runtime to `last_user_message` (clearer, more descriptive)

**Fix Strategy**: Update runtime code to use `last_user_message` everywhere

**Affected Code Files**:

1. **aicomp_sdk/core/env.py**
   - Line 378: Change `"last_user": self.trace.user_messages[-1],` → `"last_user_message": self.trace.user_messages[-1],`

2. **run_attack_openai.py**  
   - Line 211: Change `"last_user": self.trace.user_messages[-1],` → `"last_user_message": self.trace.user_messages[-1],`

3. **scripts/run_attack_openai.py**
   - Line 212: Change `"last_user": self.trace.user_messages[-1],` → `"last_user_message": self.trace.user_messages[-1],`

4. **aicomp_sdk/attacks/baselines/guardrail_rules.py**
   - Line 12: Change `last_user = (context.get("last_user") or "").lower()` → `last_user = (context.get("last_user_message") or "").lower()`

5. **aicomp_sdk/core/predicates.py**
   - Line 15: Change `last_user = user_msgs[-1].lower() if user_msgs else ""` (keep variable name, but use consistent key)
   - Line 31-32: References are to local variable, not context key (OK as-is)

6. **aicomp_sdk/guardrails/hooks_examples.py**
   - Line 169: Change `last_user = context.context.get('last_user', '').lower()` → `last_user = context.context.get('last_user_message', '').lower()`

7. **aicomp_sdk/guardrails/hooks.py**
   - Line 279: Change `text = str(context.context.get('last_user', ''))` → `text = str(context.context.get('last_user_message', ''))`

**Documentation** (verify these are correct - they already use `last_user_message`):
- docs/SCORING.md:713 ✓
- docs/COMPETITION_RULES.md:136 ✓
- docs/GETTING_STARTED.md:256, 384, 416 ✓
- docs/GUARDRAILS_GUIDE.md:93, 184, 199, 505, 695, 809 ✓
- docs/API_REFERENCE.md:245 ✓
- docs/FAQ.md:780 ✓

---

### Issue #8: Untrusted Source Model Inconsistency

**Impact**: Inconsistent threat model - some code treats "file" as untrusted, some doesn't

**Current State**:
- `tests/integration/test_verify_findings.py:42` - treats `web`, `email`, `file` as untrusted
- `aicomp_sdk/core/predicates.py:21` - only treats `web`, `email` as untrusted
- `aicomp_sdk/attacks/baselines/guardrail_rules.py:24,28,33` - only checks `web`, `email`
- Docs reference `file` as untrusted in some places

**Analysis**:
The question: **Should reading from filesystem be considered "untrusted"?**

**Arguments for "file" being untrusted:**
- Files could be poisoned by attacker
- Prompt injection via file contents
- Test verifier treats it as untrusted (line 42)

**Arguments against:**
- Filesystem is controlled environment (fixture data)
- Different threat model than web/email
- Predicates/guardrail rules don't treat it as untrusted

**Decision Required**: Need to pick ONE model

**Recommendation**: **File IS untrusted** (align with test_verify_findings.py)

**Rationale**:
- Fixture files like `compromised.txt` contain malicious content
- Prompt injection attacks work via file contents
- More conservative = better security default

**Fix**:

1. **aicomp_sdk/core/predicates.py**
   - Line 21: Change `untrusted_sources = {"web", "email"}` → `untrusted_sources = {"web", "email", "file"}`

2. **aicomp_sdk/attacks/baselines/guardrail_rules.py**
   - Line 24: Change `(("web" in recent_sources) or ("email" in recent_sources))` → `(("web" in recent_sources) or ("email" in recent_sources) or ("file" in recent_sources))`
   - Line 28: Same change
   - Line 33: Same change

3. **Documentation Updates**:
   - Verify all docs consistently mention `web`, `email`, `file` as untrusted sources
   - Already correct in: ATTACKS_GUIDE.md:530, API_REFERENCE.md:735

---

## PRIORITY 4: MEDIUM (Configuration Conflict)

### Issue #5: Evaluation max_turns Inconsistency

**Impact**: Different max_turns values in different contexts, unclear what's correct

**Current State**:
- `evaluation.py:72` - Uses `max_turns: 4` for defense evaluation
- `attacker_goexplore.py:47` - Default is `max_turns: 20` with comment "Increased to 20 for deep attack chains"

**Analysis**:
- Defense eval uses 4 turns (faster, conservative baseline)
- Attack algo supports 20 turns (allows deeper exploration)
- This is actually **intentional** - different use cases!

**Resolution**: **NOT A BUG** - Document the difference

**Fix**: Add clarifying comments

1. **evaluation.py**
   - Line 72: Add comment explaining choice
   ```python
   # Use conservative max_turns=4 for baseline defense evaluation (faster, covers common attacks)
   attacker = BaselineAttacker({"max_turns": 4, "branch_batch": 12})
   ```

2. **aicomp_sdk/attacks/baselines/attacker_goexplore.py**
   - Line 47: Clarify comment
   ```python
   # Default max_turns=20 enables deep exploration for attack development
   # (evaluation.py uses 4 for faster baseline testing)
   self.max_turns = int(self.config.get("max_turns", 20))
   ```

3. **Documentation**:
   - Update docs to explain: baseline eval uses 4 turns, full attack can use up to 20
   - Clarify in COMPETITION_RULES.md or TESTING_GUIDE.md

---

## PRIORITY 5: LOW (Cleanup)

### Issue #6: __pycache__ Files in Repository

**Impact**: Git repository pollution, but already in .gitignore

**Current State**:
- `.gitignore:2` already has `__pycache__/`
- `.gitignore:134` already has `*.pyc`
- No __pycache__ directories visible in file listing

**Fix**: Ensure cleanup and verify .gitignore is working

**Action Items**:

1. **Verify no __pycache__ exists**:
   ```bash
   find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
   find . -type f -name "*.pyc" -delete
   find . -type f -name "*.pyo" -delete
   ```

2. **Verify .gitignore is correct** (already done - it's correct)

3. **Add to MANIFEST.in** (already done - line 23 has `global-exclude __pycache__`)

**Status**: **LIKELY ALREADY FIXED** - no __pycache__ found in file listing

---

## Summary of Changes by File

### Critical Priority (Must Fix)

**Code Changes:**
1. `aicomp_sdk/attacks/baselines/attacker_goexplore.py` - Fix import path (line 12)
2. `aicomp_sdk/core/env.py` - Rename context key (line 378)
3. `aicomp_sdk/attacks/baselines/guardrail_rules.py` - Rename context key (line 12)
4. `aicomp_sdk/guardrails/hooks_examples.py` - Rename context key (line 169)
5. `aicomp_sdk/guardrails/hooks.py` - Rename context key (line 279)
6. `run_attack_openai.py` - Rename context key (line 211)
7. `scripts/run_attack_openai.py` - Rename context key (line 212)

**Files to Archive/Remove:**
- `compare_guardrails.py` - Move to research/archived_scripts/
- All scripts/* with `examples_hooks_submission` imports (10 files)

**Documentation Updates:**
- 3 files for scoring constants
- 7 files for missing tools removal
- 0 files for context key (docs already correct!)

### High Priority

8. `aicomp_sdk/core/predicates.py` - Add "file" to untrusted sources (line 21)
9. `aicomp_sdk/attacks/baselines/guardrail_rules.py` - Add "file" checks (lines 24, 28, 33)

### Medium Priority

10. `evaluation.py` - Add clarifying comment (line 72)
11. `aicomp_sdk/attacks/baselines/attacker_goexplore.py` - Add clarifying comment (line 47)

---

## Testing Strategy

After implementing fixes, test:

1. **Import Tests**:
   ```bash
   python -c "from aicomp_sdk.attacks.baselines.attacker_goexplore import AttackAlgorithm"
   python -c "from tests.integration.test_verify_findings import detect_real_attacks"
   ```

2. **Context Key Tests**:
   ```bash
   python -m pytest tests/integration/test_baseline_defense.py -v
   python -m pytest tests/integration/test_baseline_performance.py -v
   ```

3. **Scoring Tests**:
   ```bash
   python -m pytest tests/unit/test_scoring.py -v
   ```

4. **Full Integration**:
   ```bash
   python evaluation.py --submission_zip research/sample_submission.zip --seconds 60
   ```

---

## Appendix A: Alternative - Implementing Missing Tools

If decision is to **implement** rather than remove `fs.list` and `http.get`:

### Implementation: fs.list

Add to `aicomp_sdk/core/tools.py` specs (line 72, before closing brace):

```python
"fs.list": ToolSpec(
    "fs.list", "READ", "local",
    {"type":"object","properties":{"path":{"type":"string"}}, "required":["path"], "additionalProperties":False}
),
```

Add to `call()` method (line 198, before `return False...`):

```python
if tool_name == "fs.list":
    self._last_source = "file"
    path = (self._fs_root / args["path"].lstrip("/")).resolve()
    if not str(path).startswith(str(self._fs_root.resolve())):
        return False, "", "path_escape"
    if not path.exists():
        return False, "", "not_found"
    if not path.is_dir():
        return False, "", "not_directory"
    files = sorted([p.name for p in path.iterdir()])
    return True, "\n".join(files), None
```

### Implementation: http.get

Add to specs (line 72):

```python
"http.get": ToolSpec(
    "http.get", "NETWORK", "public",
    {"type":"object","properties":{"url":{"type":"string"}}, "required":["url"], "additionalProperties":False}
),
```

Add to `call()` method (line 198):

```python
if tool_name == "http.get":
    self._last_source = "web"
    url = args["url"]
    if PRIVATE_NET_RE.search(url):
        return False, "", "private_net_blocked"
    # Simulate GET by searching web corpus for matching URL pattern
    for p in self._web["pages"]:
        if url.lower() in p.get("url", "").lower():
            return True, p["content"], None
    return False, "", "not_found"
```

**Note**: This implementation is **NOT recommended** as it:
- Adds complexity without clear benefit
- Overlaps with existing functionality
- Wasn't referenced by any code (only docs)

---

## Appendix B: Verification Checklist

- [ ] All import paths verified working
- [ ] Context key `last_user_message` used consistently
- [ ] Scoring constants match between code and docs
- [ ] Untrusted source model consistent (web/email/file)
- [ ] max_turns usage documented clearly
- [ ] No __pycache__ files in repository
- [ ] All documentation references checked
- [ ] Test suite passes
- [ ] Sample submission runs successfully

---

## Recommendations for Implementation Order

1. **Day 1** - Critical execution fixes:
   - Fix attacker_goexplore.py import
   - Archive broken scripts with examples_hooks_submission imports

2. **Day 2** - Critical API consistency:
   - Rename last_user → last_user_message in all code
   - Update scoring constants in all docs

3. **Day 3** - High priority fixes:
   - Add "file" to untrusted sources
   - Remove fs.list/http.get from docs

4. **Day 4** - Documentation & testing:
   - Add clarifying comments for max_turns
   - Run full test suite
   - Verify all changes

---

**End of Comprehensive Fix Plan**
