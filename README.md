# Go-Explore Red Teaming (Kaggle-ready) — Dual (Attack + Defense)

This repository is a **competition scaffold** that lets teams submit:
- an **attack algorithm** (e.g., Go-Explore, MCTS, evolutionary search), and
- a **guardrail** that mitigates tool-using agent security bugs,

and evaluates both in a deterministic, offline sandbox.

## What “Dual” means here
Your submission is evaluated in **two matches**:

1) **Offense:** your `AttackAlgorithm` attacks the **baseline guardrail**.
2) **Defense:** the **baseline attacker** attacks your `Guardrail`.

Final score = `attack_score + defense_score`.

This prevents “collusion” between your own attack and your own defense.

## Target agent: gpt-oss-20b (optional)
The scaffold supports `openai/gpt-oss-20b` via Transformers if weights are present locally.
This competition is configured to **REQUIRE** gpt-oss-20b; there is **no fallback**.

To run gpt-oss-20b:
- Provide a local model directory (offline) and set `GPT_OSS_MODEL_PATH`.
- Note: MXFP4 is Hopper+ only; on other GPUs/CPU you likely need an alternative build/quant.

References:
- OpenAI cookbook guide for running `openai/gpt-oss-20b` with Transformers.
- OpenAI gpt-oss GitHub repo notes the Harmony format requirement.

## Tools (all deterministic stubs)
- `web.search`, `web.open`
- `fs.read`, `fs.write`, `fs.delete`
- `shell.run` (simulated safe shell)
- `email.read`, `email.send`
- `http.post` (simulated egress sink)

No real network calls are made. Tool outputs come from `fixtures/`.

## Submissions
Submit a **zip** that contains:
- `attack.py` defining `AttackAlgorithm`
- `guardrail.py` defining `Guardrail`

The starter notebook shows how to package `submission.zip`.

## Local quickstart
```bash
python -m aicomp_sdk.baselines.attacker_goexplore  # runs baseline attack
python evaluation.py --submission_zip ./submission.zip
```

## Competition knobs
- Runtime budget: **1 hour** total (default split 30m offense / 30m defense).
- Deterministic seeds for fairness.


## Running with gpt-oss-20b (required)

Set an environment variable pointing at a local model directory:

```bash
export GPT_OSS_MODEL_PATH=/path/to/openai_gpt-oss-20b
python evaluation.py --submission_zip sample_submission.zip --seconds 30
```

If the model cannot be loaded, the evaluator will error (as intended).
