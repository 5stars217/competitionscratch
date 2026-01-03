from aicomp_sdk.guardrails.base import GuardrailBase, Decision

class Guardrail(GuardrailBase):
    def decide(self, tool_name, tool_args, context):
        return Decision.allow("allow all")
