import hashlib
from typing import Dict, List, Tuple

def _h(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

def cell_signature(tool_events: List[Dict], n_tool: int = 5) -> Dict[str, object]:
    # tool_events are dicts with fields: name, side_effect, scope, source, error
    seq = [e["name"] for e in tool_events][-n_tool:]
    se = [e["side_effect"] for e in tool_events][-n_tool:]
    sc = [e["scope"] for e in tool_events][-n_tool:]
    src = [e["source"] for e in tool_events][-min(2, len(tool_events)):]
    out = [("ok" if e.get("ok") else "err") for e in tool_events][-min(3, len(tool_events)):]
    sig_str = "|".join(seq + ["--"] + se + ["--"] + sc + ["--"] + src + ["--"] + out)
    return {
        "tool_seq_ngram": seq,
        "side_effects": se,
        "scopes": sc,
        "sources": src,
        "outcomes": out,
        "hash": _h(sig_str),
    }
