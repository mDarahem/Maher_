from typing import Dict, Type, Any, Callable

REGISTRY: Dict[str, Callable[..., Any]] = {}

def register(name: str):
    def deco(cls):
        REGISTRY[name] = cls
        return cls
    return deco

def get_provider(name: str):
    if name not in REGISTRY:
        raise KeyError(f"Unknown LLM provider '{name}', have: {list(REGISTRY)}")
    return REGISTRY[name]
