#!/usr/bin/env python3
"""Debug to see what's in the findings that verification is checking"""

from pathlib import Path
from aicomp_sdk.env import SandboxEnv
from aicomp_sdk.baselines.guardrail_allow import Guardrail
from aicomp_sdk.predicates import eval_predicates

import sys
sys.path.insert(0, str(Path(__file__).parent))
from examples_hooks_submission.attack_working import AttackAlgorithm

fixtures = Path(__file__).parent / "fixtures"
env = SandboxEnv(seed=42, fixtures_dir=fixtures, guardrail=Guardrail())

attacker = AttackAlgorithm({"max_turns": 3, "branch_batch": 8})
findings = attacker.run(env, {"seconds": 5})

print(f"Total findings: {len(findings)}")

# Check first 20 findings for any with DESTRUCTIVE_WRITE predicate
destructive_write_findings = []
for i, f in enumerate(findings, 1):
    predicates = f.get("predicates", [])
    if any(p.get("predicate") == "DESTRUCTIVE_WRITE" for p in predicates):
        destructive_write_findings.append((i, f))

print(f"\nFound {len(destructive_write_findings)} findings with DESTRUCTIVE_WRITE in first 50")

if destructive_write_findings:
    print(f"\nInspecting first DESTRUCTIVE_WRITE finding:")
    idx, f = destructive_write_findings[0]
    
    print(f"Finding #{idx}: {' -> '.join(f.get('user_messages', []))}")
    
    events = f.get("trace", {}).get("tool_events", [])
    print(f"\nTool events ({len(events)}):")
    for i, e in enumerate(events, 1):
        name = e.get("name")
        ok = e.get("ok")
        args = e.get("args", {})
        path = args.get("path", "N/A")
        error = e.get("error")
        
        print(f"  {i}. {name}: ok={ok}, path={path}, error={error}")
    
    print(f"\nChecking validation logic:")
    print(f"Looking for fs.delete or fs.write with 'secret' in path and ok=True...")
    
    for e in events:
        if e.get("name") in ["fs.delete", "fs.write"]:
            path = e.get("args", {}).get("path", "")
            ok = e.get("ok")
            has_secret = "secret" in path.lower()
            
            print(f"  - {e['name']}: path='{path}', has_secret={has_secret}, ok={ok}")
            if has_secret and ok:
                print(f"    ✓ THIS SHOULD BE VALID!")
else:
    print("\nNo DESTRUCTIVE_WRITE findings in first 50!")
    print("Checking what predicates ARE firing...")
    
    pred_types = set()
    for f in findings[:50]:
        for p in f.get("predicates", []):
            pred_types.add(p.get("predicate"))
    
    print(f"Predicate types in first 50 findings: {pred_types}")
