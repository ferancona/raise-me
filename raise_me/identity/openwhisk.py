from . import HTTP_INVOKER_ACTION_NAME


class OWResourceIdentifier:
    @classmethod
    def http_invoker(cls) -> str:
        return HTTP_INVOKER_ACTION_NAME
    
    @classmethod
    def http_mediator(cls, event_name: str) -> str:
        return f'raise_mediator-{event_name}'
    
    @classmethod
    def trigger(cls, event_name: str) -> str:
        return f'raise_trigger-{event_name}'
    
    @classmethod
    def rule(cls, trigger_name: str, target_name: str) -> str:
        return f'raise_rule-{trigger_name}-{target_name}'