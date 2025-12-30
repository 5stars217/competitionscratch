# Comprehensive Data Analysis

## Data Sources
1. `paper_experimental_data.json` - Main experimental results (22 configurations)
2. `ensemble_vs_enhanced_results.json` - Ensemble comparison study

---

## ⚠️ CRITICAL CLARIFICATION: Ensemble Results Are NUANCED, Not a Clear "Win"

### The Terminal Output Says "Ensemble WINS" - This is MISLEADING/INCOMPLETE!

**The script output declares:**
```
🎯 RESULT: Ensemble approach WINS
   Multiple simple agents with diversity > Single enhanced agent
```

**This is technically true FOR DIVERSITY, but NOT for total attack count!**

**Reality:** This is a **QUANTITY vs DIVERSITY TRADEOFF**, not dominance by either approach.

The terminal message focuses on diversity (2 types vs 1) but ignores quantity (2-3 attacks vs 5). A more accurate message would be:

```
🎯 RESULT: TRADEOFF - Choose Based on Goals
   Enhanced: 5 attacks, 1 type (deep exploitation)
   Ensemble: 2-3 attacks, 2 types (broad coverage)
```

**CRITICAL DETAIL:** The ensemble approaches run SIMPLE/BASIC agents (not enhanced), so direct comparison to the 26-finding enhanced agent isn't apples-to-apples!

| Configuration | Agent Type | Findings | Real Attacks | Attack Types |
|---------------|------------|----------|--------------|--------------|
| **Single Enhanced (180s)** | Enhanced + full optimization | 26 | **5** | 1 (WRITE only) |
| **Ensemble Simple (3×60s)** | 3× SIMPLE agents, same seed | 7 | 3 | **2** (WRITE + EMAIL) |
| **Ensemble Diverse (3×60s)** | 3× different strategies | 16 | 2 | **2** (WRITE + SECRET) |
| **Single Simple (180s)** | Simple agent, long run | 0 | 0 | 0 |

**Why ensemble ≠ 3× enhanced:**
1. **Different agent complexity**: Ensemble uses SIMPLE agents (no enhancements), not the enhanced agent
2. **High variance**: In ensemble_simple, only 1 of 3 runs found anything (7, 0, 0 findings)!
3. **Same seed effect**: Using same seed means similar exploration paths, not 3× coverage

### The Real Comparison:
- **Enhanced (180s) = 5 attacks** but limited diversity
- **Simple (180s) = 0 attacks** - complete failure when run alone
- **Ensemble simple (3×60s) = 3 attacks** with diversity - better than single simple despite less time
- **Ensemble diverse (3×60s) = 2 attacks** with diversity

| Metric | Single Enhanced WINS | Ensemble WINS |
|--------|---------------------|---------------|
| **Total attacks found** | ✅ **5 attacks** | ❌ 2-3 attacks |
| **Attack diversity** | ❌ 1 type (WRITE only) | ✅ **2 types** (WRITE + EMAIL/SECRET) |
| **Precision** | ❌ 19.2% | ✅ 42.9% (simple) / 12.5% (diverse) |
| **Raw findings** | ✅ 26 | ❌ 7-16 |

### Interpretation:
- **For deep exploitation** (finding many instances): Use enhanced agent → 5 attacks
- **For broad coverage** (discovering different types): Use ensemble → 2 types vs 1
- **For high confidence** (low false positives): Use simple ensemble → 43% precision

### Why This Matters:
The paper now correctly frames this as a **strategic choice** rather than claiming one approach is definitively better. Security teams need both:
- Enhanced agents to thoroughly exploit discovered vulnerabilities
- Ensembles to discover diverse attack classes

---

## KEY FINDINGS FROM ACTUAL DATA

### 1. Runtime Scaling (RQ1)
- **20s baseline**: 0 findings, 0 real attacks
- **60s intermediate**: 0 findings, 0 real attacks  
- **150s extended**: 1 finding, 0 real attacks
- **Conclusion**: Minimal benefit from extended runtime

### 2. State Signature Ablation (RQ2) - CRITICAL FINDING
Configuration breakdown:

| Signature Type | Findings | Real Attacks | Attack Types | Tool Calls |
|---|---|---|---|---|
| **tools_only** | **12** | **6** | 2 shell, 2 RCE, 2 write | 83 |
| tools_args3 | 8 | 0 | - | 66 |
| tools_args5 | 3 | 0 | - | 16 |
| tools_args_outputs | 1 | 0 | - | 4 |
| full_with_intent | 6 | 0 | - | 26 |

**KEY INSIGHT**: Simplest scheme (tools_only) found ALL 6 real attacks. Adding complexity reduced performance by 100% (6→0 attacks).

### 3. Reward Shaping Ablation (RQ3) - DRAMATIC COLLAPSE
- **No causality bonus**: 16 findings, 0 real attacks, 84 tool calls
- **With +100-250 bonus**: 1 finding, 0 real attacks, 7 tool calls
- **Effect**: Rewards reduced discovery 16× (16→1 findings)

### 4. Enhancement Isolation (RQ4) - INTERFERENCE CONFIRMED

| Configuration | Findings | Real Attacks | Attack Types | Tool Calls |
|---|---|---|---|---|
| Baseline (tools only) | 2 | 0 | - | 4 |
| Intent hashing only | 4 | 0 | - | 8 |
| Reward bonuses only | 18 | 0 | - | 136 |
| **Targeted only** | **13** | **1** | **WRITE** | 70 |
| **All combined** | **0** | **0** | **-** | **0** |

**KEY INSIGHT**: Only targeted prompts found a real attack. Combining all enhancements = complete failure (0 findings).

### 5. Ensemble vs Enhanced (RQ5) - SURPRISING RESULT

#### Single Enhanced Agent (180s total):
- 26 findings
- **5 real attacks** (all PROMPT_INJECTION_WRITE)
- 1 unique attack type
- 90 tool calls

#### Ensemble Simple (3×60s, same seed):
- 7 findings
- 3 real attacks (2 WRITE, 1 EMAIL)
- **2 unique attack types**
- 40 tool calls
- Precision: 42.9% (3/7)

#### Ensemble Diverse (3 different strategies):
- Agent 1 (tools_only): 14 findings, 2 attacks (WRITE, READ_SECRET)
- Agent 2 (with_targeting): 0 findings, 0 attacks
- Agent 3 (with_rewards): 2 findings, 0 attacks
- **Combined**: 16 findings, 2 real attacks, **2 unique attack types**
- Precision: 12.5% (2/16)

#### Single Simple (180s):
- 0 findings, 0 real attacks

**CRITICAL REVISION**: Enhanced agent found MORE total attacks (5 vs 2) but ensemble found MORE unique attack types (2 vs 1). The narrative needs correction!

### 6. Shell Targeted Experiments

| Configuration | Findings | Shell Chains | Tool Calls |
|---|---|---|---|
| Targeted, no guard | 2 | 0 | 10 |
| Targeted, with guard | 3 | 0 | 10 |

**KEY INSIGHT**: Guardrails did NOT amplify discovery significantly. No shell chains found in either case.

### 7. General 150s Experiments

| Configuration | Findings | Real Attacks | Key Tool Calls |
|---|---|---|---|
| No guard | 1 | 0 | email.read(1), fs.write(1) |
| With guard | 4 | 0 | email.read(6), fs.write(4), shell.run(4) |

**Modest increase**: 4× more findings with guard, but still 0 real attacks.

---

## MAJOR DISCREPANCIES WITH PAPER

1. **Ensemble claim is WRONG**: Paper claims "ensemble diversity beats optimization" but data shows enhanced agent found 5 attacks vs ensemble's 2. The correct claim is "ensemble finds more DIVERSE attacks."

2. **Guardrail amplification is EXAGGERATED**: Paper claims 19× amplification (5→96), but actual data shows 4× at most (1→4 for general, 2→3 for targeted).

3. **Shell chains**: Paper mentions 2 successful shell chains, but data shows 0 shell chains in shell_targeted experiments.

4. **Numbers don't match**: Many table values in paper don't align with JSON data.

---

## CORRECT NARRATIVE

### What Works:
1. **Simple state signatures**: tools_only found all 6 real attacks
2. **Targeted prompts alone**: Found 1 real attack (13 findings)
3. **Single enhanced agent**: Found most attacks (5 total) but limited diversity

### What Fails:
1. **Complex signatures**: Reduced attacks from 6→0
2. **Reward bonuses**: Collapsed discovery 16× 
3. **Combined enhancements**: Complete failure (0 findings)
4. **Extended runtime**: Minimal benefit without targeting

### Key Insight:
For safety-trained models, **simplicity and diversity beat sophistication**. The best results come from either:
- Simple algorithms (tools_only signature)
- Single targeted enhancement (targeted prompts)
- Ensemble for diversity (but not raw attack count)

Combining multiple sophisticated enhancements creates interference and optimization dead-ends.
