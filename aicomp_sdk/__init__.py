"""AI Competition SDK for red teaming tool-using AI agents.

This package provides a comprehensive framework for:
- Building and testing AI agent security
- Implementing attack algorithms  
- Creating defensive guardrails
- Running security competitions
"""

__version__ = "1.0.0"

# Core SDK
from .core.env import SandboxEnv
from .guardrails.base import GuardrailBase, Decision

# Advanced hooks API (for power users)
from .guardrails.hooks import (
    HookRegistry,
    HookStage,
    HookContext,
    HookResult,
    HookCallback,
    get_hook_registry,
    create_payload_injection_hook,
    create_trigger_hook,
    create_detection_hook,
    create_memory_hook,
    create_lpci_vector_store_hook,
    create_lpci_tool_poisoning_hook,
    create_lpci_cross_session_hook,
)

# Simple hooks API (recommended for most users)
from .guardrails.hooks_simple import (
    attack_hook,
    defense_hook,
    clear_hooks,
    store_payload,
    poison_tool,
)

__all__ = [
    # Core SDK
    'SandboxEnv',
    'GuardrailBase',
    'Decision',
    
    # Simple Hooks API (recommended)
    'attack_hook',
    'defense_hook',
    'clear_hooks',
    'store_payload',
    'poison_tool',
    
    # Advanced Hooks API
    'HookRegistry',
    'HookStage',
    'HookContext',
    'HookResult',
    'HookCallback',
    'get_hook_registry',
    'create_payload_injection_hook',
    'create_trigger_hook',
    'create_detection_hook',
    'create_memory_hook',
    'create_lpci_vector_store_hook',
    'create_lpci_tool_poisoning_hook',
    'create_lpci_cross_session_hook',
]
