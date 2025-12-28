from aicomp_sdk.guardrail_base import GuardrailBase, Decision

class Guardrail(GuardrailBase):
    def decide(self, tool_name, tool_args, context):
        return Decision.allow("allow all")
