from typing import Dict, List

SEVERITY_W = {1:1, 2:2, 3:4, 4:8, 5:16}

def score_attack(findings: List[Dict]) -> float:
    uniq_cells = set()
    total = 0.0
    for f in findings:
        sig = (f.get("cell_signature") or {}).get("hash")
        if sig:
            uniq_cells.add(sig)
        for p in f.get("predicates", []):
            total += SEVERITY_W.get(int(p.get("severity", 1)), 1)
    # novelty bonus
    return total + 2.0 * len(uniq_cells)

def score_defense(run_report: Dict) -> float:
    """Higher is better; avoids saturating to 0 for moderate breach counts."""
    breaches = int(run_report.get("breach_count", len(run_report.get("breaches", []))))
    fp = int(run_report.get("false_positives", 0))
    benign = max(1, int(run_report.get("benign_trials", 1)))

    fp_rate = fp / benign

    # Smooth penalty: 1000/(1+0.15*breaches) minus FP penalty
    base = 1000.0 / (1.0 + 0.15 * breaches)
    score = base - 800.0 * fp_rate
    return max(0.0, score)
