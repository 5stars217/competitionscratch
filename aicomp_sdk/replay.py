import copy
from typing import Dict, List
from pathlib import Path

from .tools import ToolSuite
from .trace import Trace, ToolEvent

class ReplayHarness:
    def __init__(self, fixtures_dir: Path):
        self.fixtures_dir = fixtures_dir

    def replay(self, seed: int, user_messages: List[str], agent, guardrail) -> Dict:
        env = __import__("aicomp_sdk.env", fromlist=["SandboxEnv"]).SandboxEnv(
            seed=seed, fixtures_dir=self.fixtures_dir, agent=agent, guardrail=guardrail
        )
        env.reset()
        for um in user_messages:
            env.interact(um)
        return env.export_trace_dict()
