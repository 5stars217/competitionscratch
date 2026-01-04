#!/usr/bin/env python3
"""
Complete Experimental Data Collection for Paper
Runs all experiments and generates comprehensive dataset
Now with async parallelization for faster execution
"""

import asyncio
import json
import os
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

from examples_hooks_submission.guardrail_prompt_injection import (
    Guardrail as PromptInjectionGuardrail,
)

from aicomp_sdk.attacks.baselines.attacker_goexplore import AttackAlgorithm
from aicomp_sdk.attacks.baselines.guardrail_allow import Guardrail as AllowGuardrail
from aicomp_sdk.core.env import SandboxEnv

sys.path.insert(0, str(repo_root / "tests"))
from test_verify_findings import detect_real_attacks

# Verify API key
if not os.environ.get("OPENAI_API_KEY"):
    print("ERROR: OPENAI_API_KEY required")
    sys.exit(1)

fixtures = repo_root / "fixtures"
results = {
    "metadata": {
        "timestamp": datetime.now().isoformat(),
        "agent": "GPT-4o-mini",
        "note": "Complete experimental data for paper",
    }
}


def extract_tool_stats(findings):
    """Extract detailed statistics from findings"""
    stats = {
        "total_findings": len(findings),
        "tool_calls": defaultdict(int),
        "successful_tools": defaultdict(int),
        "depth_dist": defaultdict(int),
        "real_attacks_by_type": defaultdict(int),
        "chains_by_operation": defaultdict(list),
    }

    for f in findings:
        msgs = f.get("user_messages", [])
        stats["depth_dist"][len(msgs)] += 1

        events = f.get("trace", {}).get("tool_events", [])
        for evt in events:
            tool = evt.get("name", "")
            stats["tool_calls"][tool] += 1
            if evt.get("ok"):
                stats["successful_tools"][tool] += 1

        # Real attacks
        real = detect_real_attacks(events)
        for attack in real:
            atype = attack.get("type", "UNKNOWN")
            stats["real_attacks_by_type"][atype] += 1

        # Track chains per operation
        for evt in events:
            if evt.get("ok"):
                tool = evt.get("name", "")
                if tool in ["shell.run", "fs.delete", "http.post", "email.send"]:
                    stats["chains_by_operation"][tool].append(
                        {
                            "chain": " -> ".join(msgs),
                            "depth": len(msgs),
                            "args": evt.get("args", {}),
                        }
                    )

    return dict(stats)


def run_experiment(name, seed, fixtures, guardrail_cls, attack_config, budget):
    """Run a single experiment (for parallel execution)"""
    print(f"[{name}] Starting...")
    env = SandboxEnv(seed=seed, fixtures_dir=fixtures, guardrail=guardrail_cls())
    atk = AttackAlgorithm(attack_config)
    findings = atk.run(env, budget)
    stats = extract_tool_stats(findings)
    print(
        f"[{name}] Complete: {stats['total_findings']} findings, {sum(stats['real_attacks_by_type'].values())} real attacks"
    )
    return stats


async def run_all_experiments_async():
    """Run all experiments in parallel using async"""
    print("=" * 70)
    print("COMPREHENSIVE DATA COLLECTION FOR PAPER (ASYNC)")
    print("=" * 70)
    print(f"\nStarted: {datetime.now().strftime('%H:%M:%S')}")

    # Define all experiments
    experiments = [
        # Main experiments
        (
            "1_general_150s_noguard",
            42,
            AllowGuardrail,
            {"max_turns": 6, "branch_batch": 12, "target_shell": False},
            {"seconds": 150},
        ),
        (
            "2_general_150s_guard",
            42,
            PromptInjectionGuardrail,
            {"max_turns": 6, "branch_batch": 12, "target_shell": False},
            {"seconds": 150},
        ),
        (
            "3_targeted_120s_noguard",
            42,
            AllowGuardrail,
            {"max_turns": 6, "branch_batch": 12, "target_shell": True},
            {"seconds": 120},
        ),
        (
            "4_targeted_120s_guard",
            42,
            PromptInjectionGuardrail,
            {"max_turns": 6, "branch_batch": 12, "target_shell": True},
            {"seconds": 120},
        ),
        (
            "5_baseline_20s",
            42,
            AllowGuardrail,
            {"max_turns": 6, "branch_batch": 12, "target_shell": False},
            {"seconds": 20},
        ),
        (
            "6_intermediate_60s",
            42,
            AllowGuardrail,
            {"max_turns": 6, "branch_batch": 12, "target_shell": False},
            {"seconds": 60},
        ),
    ]

    # Signature ablations
    for variant_name, config in [
        (
            "sig_tools_only",
            {
                "use_args": False,
                "use_outputs": False,
                "use_intent": False,
                "causality_bonus": 0,
                "high_bonus": 0,
                "critical_bonus": 0,
                "medium_bonus": 0,
            },
        ),
        (
            "sig_args3",
            {
                "use_args": True,
                "args_count": 3,
                "use_outputs": False,
                "use_intent": False,
                "causality_bonus": 0,
                "high_bonus": 0,
                "critical_bonus": 0,
                "medium_bonus": 0,
            },
        ),
        (
            "sig_args5",
            {
                "use_args": True,
                "args_count": 5,
                "use_outputs": False,
                "use_intent": False,
                "causality_bonus": 0,
                "high_bonus": 0,
                "critical_bonus": 0,
                "medium_bonus": 0,
            },
        ),
        (
            "sig_args_outputs",
            {
                "use_args": True,
                "args_count": 5,
                "use_outputs": True,
                "use_intent": False,
                "causality_bonus": 0,
                "high_bonus": 0,
                "critical_bonus": 0,
                "medium_bonus": 0,
            },
        ),
        (
            "sig_full_intent",
            {
                "use_args": True,
                "args_count": 5,
                "use_outputs": True,
                "use_intent": True,
                "causality_bonus": 0,
                "high_bonus": 0,
                "critical_bonus": 0,
                "medium_bonus": 0,
            },
        ),
    ]:
        full_config = {"max_turns": 6, "branch_batch": 12, **config}
        experiments.append((variant_name, 42, AllowGuardrail, full_config, {"seconds": 90}))

    # Reward ablations
    for variant_name, config in [
        (
            "rew_no_bonus",
            {
                "use_intent": True,
                "use_args": True,
                "use_outputs": True,
                "causality_bonus": 0,
                "high_bonus": 0,
                "critical_bonus": 0,
                "medium_bonus": 0,
            },
        ),
        (
            "rew_with_bonus",
            {
                "use_intent": True,
                "use_args": True,
                "use_outputs": True,
                "causality_bonus": 100,
                "high_bonus": 75,
                "critical_bonus": 150,
                "medium_bonus": 25,
            },
        ),
    ]:
        full_config = {"max_turns": 6, "branch_batch": 12, **config}
        experiments.append((variant_name, 42, AllowGuardrail, full_config, {"seconds": 90}))

    # Individual enhancement ablations
    for variant_name, config in [
        (
            "enh_baseline",
            {
                "use_intent": False,
                "use_args": False,
                "use_outputs": False,
                "causality_bonus": 0,
                "high_bonus": 0,
                "critical_bonus": 0,
                "medium_bonus": 0,
                "target_shell": False,
            },
        ),
        (
            "enh_intent_only",
            {
                "use_intent": True,
                "use_args": False,
                "use_outputs": False,
                "causality_bonus": 0,
                "high_bonus": 0,
                "critical_bonus": 0,
                "medium_bonus": 0,
                "target_shell": False,
            },
        ),
        (
            "enh_reward_only",
            {
                "use_intent": False,
                "use_args": False,
                "use_outputs": False,
                "causality_bonus": 100,
                "high_bonus": 75,
                "critical_bonus": 150,
                "medium_bonus": 25,
                "target_shell": False,
            },
        ),
        (
            "enh_targeted_only",
            {
                "use_intent": False,
                "use_args": False,
                "use_outputs": False,
                "causality_bonus": 0,
                "high_bonus": 0,
                "critical_bonus": 0,
                "medium_bonus": 0,
                "target_shell": True,
            },
        ),
        (
            "enh_all_combined",
            {
                "use_intent": True,
                "use_args": True,
                "use_outputs": True,
                "causality_bonus": 100,
                "high_bonus": 75,
                "critical_bonus": 150,
                "medium_bonus": 25,
                "target_shell": True,
            },
        ),
    ]:
        full_config = {"max_turns": 6, "branch_batch": 12, **config}
        experiments.append((variant_name, 42, AllowGuardrail, full_config, {"seconds": 90}))

    print(f"\nRunning {len(experiments)} experiments in parallel...")

    # Run in parallel using ThreadPoolExecutor
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=4) as executor:
        tasks = [
            loop.run_in_executor(
                executor, run_experiment, name, seed, fixtures, guard, config, budget
            )
            for name, seed, guard, config, budget in experiments
        ]
        all_stats = await asyncio.gather(*tasks)

    # Map results back
    exp_map = {name: stats for (name, *_), stats in zip(experiments, all_stats)}

    return exp_map


# Main execution
async def main():
    exp_results = await run_all_experiments_async()

    # Build results structure
    results = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "agent": "GPT-4o-mini",
            "note": "Complete experimental data with ablations (async)",
        },
        "general_150s": {
            "no_guard": exp_results["1_general_150s_noguard"],
            "with_guard": exp_results["2_general_150s_guard"],
        },
        "shell_targeted": {
            "no_guard": exp_results["3_targeted_120s_noguard"],
            "with_guard": exp_results["4_targeted_120s_guard"],
            "shell_chains_no_guard": len(
                exp_results["3_targeted_120s_noguard"]["chains_by_operation"].get("shell.run", [])
            ),
            "shell_chains_with_guard": len(
                exp_results["4_targeted_120s_guard"]["chains_by_operation"].get("shell.run", [])
            ),
        },
        "baseline_20s": {"no_guard": exp_results["5_baseline_20s"]},
        "intermediate_60s": {"no_guard": exp_results["6_intermediate_60s"]},
    }

    # Runtime scaling metrics
    results["runtime_scaling"] = {
        "20s": {
            "findings": exp_results["5_baseline_20s"]["total_findings"],
            "real_attacks": sum(exp_results["5_baseline_20s"]["real_attacks_by_type"].values()),
        },
        "60s": {
            "findings": exp_results["6_intermediate_60s"]["total_findings"],
            "real_attacks": sum(exp_results["6_intermediate_60s"]["real_attacks_by_type"].values()),
        },
        "150s": {
            "findings": exp_results["1_general_150s_noguard"]["total_findings"],
            "real_attacks": sum(
                exp_results["1_general_150s_noguard"]["real_attacks_by_type"].values()
            ),
        },
    }

    # Ablations
    results["ablations"] = {
        "state_signatures": {
            "tools_only": exp_results["sig_tools_only"],
            "tools_args3": exp_results["sig_args3"],
            "tools_args5": exp_results["sig_args5"],
            "tools_args_outputs": exp_results["sig_args_outputs"],
            "full_with_intent": exp_results["sig_full_intent"],
        },
        "reward_shaping": {
            "no_bonus": exp_results["rew_no_bonus"],
            "with_bonus": exp_results["rew_with_bonus"],
        },
        "enhancement_isolation": {
            "baseline": exp_results["enh_baseline"],
            "intent_only": exp_results["enh_intent_only"],
            "reward_only": exp_results["enh_reward_only"],
            "targeted_only": exp_results["enh_targeted_only"],
            "all_combined": exp_results["enh_all_combined"],
        },
    }

    # Print summary
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"\n📊 Main Experiments:")
    print(
        f"  General 150s (no guard): {results['general_150s']['no_guard']['total_findings']} findings"
    )
    print(
        f"  Targeted 120s (with guard): {results['shell_targeted']['with_guard']['total_findings']} findings, {results['shell_targeted']['shell_chains_with_guard']} shells"
    )

    # Save to JSON
    output_file = repo_root / "paper_experimental_data.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n💾 Complete dataset saved to: {output_file}")
    print(
        f"✅ All {len(exp_results)} experiments complete at {datetime.now().strftime('%H:%M:%S')}"
    )
    print(f"\n{'='*70}\n")


if __name__ == "__main__":
    asyncio.run(main())
