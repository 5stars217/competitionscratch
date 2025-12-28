from .env import SandboxEnv
from .guardrail_base import GuardrailBase, Decision

# Advanced hooks API (for power users)
from .hooks import (
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
from .hooks_simple import (
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
