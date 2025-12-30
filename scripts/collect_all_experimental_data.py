#!/usr/bin/env python3
"""
Complete Experimental Data Collection for Paper
Runs all experiments and generates comprehensive dataset
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

from aicomp_sdk.env import SandboxEnv
from aicomp_sdk.baselines.guardrail_allow import Guardrail as AllowGuardrail
from examples_hooks_submission.guardrail_prompt_injection import Guardrail as PromptInjectionGuardrail
from aicomp_sdk.baselines.attacker_goexplore import AttackAlgorithm

sys.path.insert(0, str(repo_root / "tests"))
from test_verify_findings import detect_real_attacks

# Verify API key
if not os.environ.get("OPENAI_API_KEY"):
    print("ERROR: OPENAI_API_KEY required")
    sys.exit(1)

fixtures = repo_root / "fixtures"
results = {"metadata": {
    "timestamp": datetime.now().isoformat(),
    "agent": "GPT-4o-mini",
    "note": "Complete experimental data for paper"
}}

def extract_tool_stats(findings):
    """Extract detailed statistics from findings"""
    stats = {
        'total_findings': len(findings),
        'tool_calls': defaultdict(int),
        'successful_tools': defaultdict(int),
        'depth_dist': defaultdict(int),
        'real_attacks_by_type': defaultdict(int),
        'chains_by_operation': defaultdict(list)
    }
    
    for f in findings:
        msgs = f.get('user_messages', [])
        stats['depth_dist'][len(msgs)] += 1
        
        events = f.get('trace', {}).get('tool_events', [])
        for evt in events:
            tool = evt.get('name', '')
            stats['tool_calls'][tool] += 1
            if evt.get('ok'):
                stats['successful_tools'][tool] += 1
        
        # Real attacks
        real = detect_real_attacks(events)
        for attack in real:
            atype = attack.get('type', 'UNKNOWN')
            stats['real_attacks_by_type'][atype] += 1
        
        # Track chains per operation
        for evt in events:
            if evt.get('ok'):
                tool = evt.get('name', '')
                if tool in ['shell.run', 'fs.delete', 'http.post', 'email.send']:
                    stats['chains_by_operation'][tool].append({
                        'chain': ' -> '.join(msgs),
                        'depth': len(msgs),
                        'args': evt.get('args', {})
                    })
    
    return dict(stats)

print("="*70)
print("COMPREHENSIVE DATA COLLECTION FOR PAPER")
print("="*70)
print(f"\nStarted: {datetime.now().strftime('%H:%M:%S')}")

# Experiment 1: General Exploration 150s
print("\n[1/6] General exploration 150s - No Guardrail...")
env1 = SandboxEnv(seed=42, fixtures_dir=fixtures, guardrail=AllowGuardrail())
atk1 = AttackAlgorithm({"max_turns": 6, "branch_batch": 12, "target_shell": False})
findings1 = atk1.run(env1, {"seconds": 150})
stats1 = extract_tool_stats(findings1)

print(f"\n[2/6] General exploration 150s - With Guardrail...")
env2 = SandboxEnv(seed=42, fixtures_dir=fixtures, guardrail=PromptInjectionGuardrail())
atk2 = AttackAlgorithm({"max_turns": 6, "branch_batch": 12, "target_shell": False})
findings2 = atk2.run(env2, {"seconds": 150})
stats2 = extract_tool_stats(findings2)

results['general_150s'] = {
    'no_guard': stats1,
    'with_guard': stats2
}

# Experiment 2: Shell targeting
print(f"\n[3/6] Shell-targeted exploration - No Guardrail...")
env3 = SandboxEnv(seed=42, fixtures_dir=fixtures, guardrail=AllowGuardrail())
atk3 = AttackAlgorithm({"max_turns": 6, "branch_batch": 12, "target_shell": True})
findings3 = atk3.run(env3, {"seconds": 120})
stats3 = extract_tool_stats(findings3)

print(f"\n[4/6] Shell-targeted exploration - With Guardrail...")
env4 = SandboxEnv(seed=42, fixtures_dir=fixtures, guardrail=PromptInjectionGuardrail())
atk4 = AttackAlgorithm({"max_turns": 6, "branch_batch": 12, "target_shell": True})
findings4 = atk4.run(env4, {"seconds": 120})
stats4 = extract_tool_stats(findings4)

results['shell_targeted'] = {
    'no_guard': stats3,
    'with_guard': stats4,
    'shell_chains_no_guard': len(stats3['chains_by_operation'].get('shell.run', [])),
    'shell_chains_with_guard': len(stats4['chains_by_operation'].get('shell.run', []))
}

# Experiment 3: Baseline 20s for comparison
print(f"\n[5/6] Baseline 20s - No Guardrail (for comparison)...")
env5 = SandboxEnv(seed=42, fixtures_dir=fixtures, guardrail=AllowGuardrail())
atk5 = AttackAlgorithm({"max_turns": 6, "branch_batch": 12, "target_shell": False})
findings5 = atk5.run(env5, {"seconds": 20})
stats5 = extract_tool_stats(findings5)

results['baseline_20s'] = {'no_guard': stats5}

# Experiment 4: 60s intermediate point
print(f"\n[6/6] Intermediate 60s - No Guardrail...")
env6 = SandboxEnv(seed=42, fixtures_dir=fixtures, guardrail=AllowGuardrail())
atk6 = AttackAlgorithm({"max_turns": 6, "branch_batch": 12, "target_shell": False})
findings6 = atk6.run(env6, {"seconds": 60})
stats6 = extract_tool_stats(findings6)

results['intermediate_60s'] = {'no_guard': stats6}

# Compute key metrics
print("\n" + "="*70)
print("COMPUTING SUMMARY METRICS")
print("="*70)

# Runtime scaling
results['runtime_scaling'] = {
    '20s': {
        'findings': stats5['total_findings'],
        'real_attacks': sum(stats5['real_attacks_by_type'].values())
    },
    '60s': {
        'findings': stats6['total_findings'],
        'real_attacks': sum(stats6['real_attacks_by_type'].values())
    },
    '150s': {
        'findings': stats1['total_findings'],
        'real_attacks': sum(stats1['real_attacks_by_type'].values())
    }
}

# Guardrail effectiveness
no_guard_real = sum(stats1['real_attacks_by_type'].values())
with_guard_real = sum(stats2['real_attacks_by_type'].values())

results['guardrail_effectiveness'] = {
    'no_guard_findings': stats1['total_findings'],
    'with_guard_findings': stats2['total_findings'],
    'no_guard_real_attacks': no_guard_real,
    'with_guard_real_attacks': with_guard_real,
    'effectiveness_pct': ((no_guard_real - with_guard_real) / no_guard_real * 100) if no_guard_real > 0 else 0,
    'attack_types_no_guard': dict(stats1['real_attacks_by_type']),
    'attack_types_with_guard': dict(stats2['real_attacks_by_type'])
}

# Print summary
print(f"\n📊 RUNTIME SCALING:")
for runtime in ['20s', '60s', '150s']:
    data = results['runtime_scaling'][runtime]
    print(f"  {runtime}: {data['findings']} findings, {data['real_attacks']} real attacks")

print(f"\n🛡️  GUARDRAIL EFFECTIVENESS:")
print(f"  No guard: {no_guard_real} real attacks")
print(f"  With guard: {with_guard_real} real attacks")
print(f"  Change: {results['guardrail_effectiveness']['effectiveness_pct']:.1f}%")

print(f"\n🎯 TARGETED EXPLORATION:")
print(f"  Shell chains (no guard): {results['shell_targeted']['shell_chains_no_guard']}")
print(f"  Shell chains (with guard): {results['shell_targeted']['shell_chains_with_guard']}")

# Save to JSON
output_file = repo_root / "paper_experimental_data.json"
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"\n💾 Complete dataset saved to: {output_file}")
print(f"✅ All experiments complete at {datetime.now().strftime('%H:%M:%S')}")

# ABLATION STUDIES
print(f"\n{'='*70}")
print("ABLATION STUDIES")
print(f"{'='*70}\n")

# Ablation 1: State Signature Granularity
print("[ABLATION 1] State Signature Granularity...")
print("Testing different cell signature schemes to measure state collapse\n")

ablation_results = {'state_signatures': {}, 'reward_shaping': {}}

# We'll run 5 variants with increasing signature granularity
# FIX: Also disable rewards to test ONLY signature impact
signature_variants = [
    ('tools_only', {'use_args': False, 'use_outputs': False, 'use_intent': False, 'causality_bonus': 0, 'high_bonus': 0, 'critical_bonus': 0, 'medium_bonus': 0}),
    ('tools_args3', {'use_args': True, 'args_count': 3, 'use_outputs': False, 'use_intent': False, 'causality_bonus': 0, 'high_bonus': 0, 'critical_bonus': 0, 'medium_bonus': 0}),
    ('tools_args5', {'use_args': True, 'args_count': 5, 'use_outputs': False, 'use_intent': False, 'causality_bonus': 0, 'high_bonus': 0, 'critical_bonus': 0, 'medium_bonus': 0}),
    ('tools_args_outputs', {'use_args': True, 'args_count': 5, 'use_outputs': True, 'use_intent': False, 'causality_bonus': 0, 'high_bonus': 0, 'critical_bonus': 0, 'medium_bonus': 0}),
    ('full_with_intent', {'use_args': True, 'args_count': 5, 'use_outputs': True, 'use_intent': True, 'causality_bonus': 0, 'high_bonus': 0, 'critical_bonus': 0, 'medium_bonus': 0}),
]

for i, (name, config) in enumerate(signature_variants, 1):
    print(f"  [{i}/5] Testing signature scheme: {name}...")
    env_abl = SandboxEnv(seed=42, fixtures_dir=fixtures, guardrail=AllowGuardrail())
    atk_abl = AttackAlgorithm({
        "max_turns": 6,
        "branch_batch": 12,
        **config  # Pass signature config to algorithm
    })
    findings_abl = atk_abl.run(env_abl, {"seconds": 90})  # FIX: Use consistent 90s across all ablations
    stats_abl = extract_tool_stats(findings_abl)
    
    # Calculate unique cell count and collapse rate
    # In a real implementation, you'd track this in the algorithm
    # For now, use findings as proxy for exploration coverage
    ablation_results['state_signatures'][name] = {
        'findings': stats_abl['total_findings'],
        'real_attacks': sum(stats_abl['real_attacks_by_type'].values()),
        'tool_calls': sum(stats_abl['tool_calls'].values()),
        'depth_distribution': dict(stats_abl['depth_dist']),
        'config': config
    }
    print(f"      → {stats_abl['total_findings']} findings, {sum(stats_abl['real_attacks_by_type'].values())} real attacks")

# Ablation 2: Reward Shaping
print(f"\n[ABLATION 2] Reward Shaping Impact...")
print("Testing with/without causality-based reward bonuses (all other enhancements enabled)\n")

reward_variants = [
    # FIX: Keep signature features enabled, only vary rewards
    ('no_bonus', {'use_intent': True, 'use_args': True, 'use_outputs': True, 'causality_bonus': 0, 'high_bonus': 0, 'critical_bonus': 0, 'medium_bonus': 0}),
    ('with_bonus', {'use_intent': True, 'use_args': True, 'use_outputs': True, 'causality_bonus': 100, 'high_bonus': 75, 'critical_bonus': 150, 'medium_bonus': 25}),
]

for i, (name, config) in enumerate(reward_variants, 1):
    print(f"  [{i}/2] Testing reward scheme: {name}...")
    env_rew = SandboxEnv(seed=42, fixtures_dir=fixtures, guardrail=AllowGuardrail())
    atk_rew = AttackAlgorithm({
        "max_turns": 6,
        "branch_batch": 12,
        **config  # Pass reward config to algorithm
    })
    findings_rew = atk_rew.run(env_rew, {"seconds": 90})  # FIX: Use consistent 90s across all ablations
    stats_rew = extract_tool_stats(findings_rew)
    
    ablation_results['reward_shaping'][name] = {
        'findings': stats_rew['total_findings'],
        'real_attacks': sum(stats_rew['real_attacks_by_type'].values()),
        'real_attack_types': dict(stats_rew['real_attacks_by_type']),
        'detection_rate': sum(stats_rew['real_attacks_by_type'].values()) / stats_rew['total_findings'] if stats_rew['total_findings'] > 0 else 0,
        'config': config
    }
    real = sum(stats_rew['real_attacks_by_type'].values())
    det_rate = real / stats_rew['total_findings'] * 100 if stats_rew['total_findings'] > 0 else 0
    print(f"      → {stats_rew['total_findings']} findings, {real} real ({det_rate:.1f}% detection rate)")

# Ablation 3: Individual Enhancement Contribution
print(f"\n[ABLATION 3] Individual Enhancement Contributions...")
print("Testing each enhancement in isolation to establish causality\n")

enhancement_variants = [
    # TRUE BASELINE: Tool names only, no enhancements
    ('baseline', {'use_intent': False, 'use_args': False, 'use_outputs': False, 'causality_bonus': 0, 'high_bonus': 0, 'critical_bonus': 0, 'medium_bonus': 0, 'target_shell': False}),
    # Test each enhancement individually
    ('intent_only', {'use_intent': True, 'use_args': False, 'use_outputs': False, 'causality_bonus': 0, 'high_bonus': 0, 'critical_bonus': 0, 'medium_bonus': 0, 'target_shell': False}),
    ('reward_only', {'use_intent': False, 'use_args': False, 'use_outputs': False, 'causality_bonus': 100, 'high_bonus': 75, 'critical_bonus': 150, 'medium_bonus': 25, 'target_shell': False}),
    ('targeted_only', {'use_intent': False, 'use_args': False, 'use_outputs': False, 'causality_bonus': 0, 'high_bonus': 0, 'critical_bonus': 0, 'medium_bonus': 0, 'target_shell': True}),
    # Our full implementation
    ('all_combined', {'use_intent': True, 'use_args': True, 'use_outputs': True, 'causality_bonus': 100, 'high_bonus': 75, 'critical_bonus': 150, 'medium_bonus': 25, 'target_shell': True}),
]

ablation_results['enhancement_isolation'] = {}

for i, (name, config) in enumerate(enhancement_variants, 1):
    print(f"  [{i}/5] Testing enhancement config: {name}...")
    env_enh = SandboxEnv(seed=42, fixtures_dir=fixtures, guardrail=AllowGuardrail())
    atk_enh = AttackAlgorithm({
        "max_turns": 6,
        "branch_batch": 12,
        **config
    })
    findings_enh = atk_enh.run(env_enh, {"seconds": 90})
    stats_enh = extract_tool_stats(findings_enh)
    
    # Calculate efficiency metrics
    total_calls = sum(stats_enh['tool_calls'].values())
    real_attacks = sum(stats_enh['real_attacks_by_type'].values())
    efficiency = (real_attacks / total_calls * 100) if total_calls > 0 else 0
    
    ablation_results['enhancement_isolation'][name] = {
        'findings': stats_enh['total_findings'],
        'real_attacks': real_attacks,
        'tool_calls': total_calls,
        'efficiency_pct': efficiency,
        'attacks_per_100_calls': (real_attacks / total_calls * 100) if total_calls > 0 else 0,
        'config': config
    }
    print(f"      → {stats_enh['total_findings']} findings, {real_attacks} real, {total_calls} calls ({efficiency:.2f}% efficient)")

# Add ablations to results
results['ablations'] = ablation_results

# Print ablation summary
print(f"\n{'='*70}")
print("ABLATION SUMMARY")
print(f"{'='*70}\n")

print("📊 State Signature Impact:")
for name, data in ablation_results['state_signatures'].items():
    print(f"  {name:20s}: {data['findings']:3d} findings, {data['real_attacks']} real attacks")

print(f"\n🎯 Reward Shaping Impact:")
no_bonus_data = ablation_results['reward_shaping']['no_bonus']
with_bonus_data = ablation_results['reward_shaping']['with_bonus']
print(f"  Without bonus: {no_bonus_data['findings']} findings, {no_bonus_data['real_attacks']} real ({no_bonus_data['detection_rate']*100:.1f}%)")
print(f"  With bonus:    {with_bonus_data['findings']} findings, {with_bonus_data['real_attacks']} real ({with_bonus_data['detection_rate']*100:.1f}%)")
improvement = ((with_bonus_data['real_attacks'] - no_bonus_data['real_attacks']) / no_bonus_data['real_attacks'] * 100) if no_bonus_data['real_attacks'] > 0 else float('inf')
print(f"  Improvement: {improvement:+.1f}% more real attacks discovered")

print(f"\n🔬 Individual Enhancement Contributions:")
baseline = ablation_results['enhancement_isolation']['baseline']
for name, data in ablation_results['enhancement_isolation'].items():
    if name == 'baseline':
        print(f"  {name:15s}: {data['real_attacks']} real / {data['tool_calls']} calls = {data['efficiency_pct']:.2f}% (baseline)")
    else:
        improvement = data['real_attacks'] - baseline['real_attacks']
        eff_improvement = data['efficiency_pct'] - baseline['efficiency_pct']
        print(f"  {name:15s}: {data['real_attacks']} real / {data['tool_calls']} calls = {data['efficiency_pct']:.2f}% ({improvement:+d} attacks, {eff_improvement:+.2f}% efficiency)")

# Resave with ablations
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"\n💾 Complete dataset with ablations saved to: {output_file}")
print(f"✅ All experiments and ablations complete at {datetime.now().strftime('%H:%M:%S')}")
print(f"\n{'='*70}\n")
