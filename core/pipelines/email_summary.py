from core.prompting.renderer import render_email_summary
from core.config.loader import load_config
from core.config.routing import get_task_routing
from adapters.llm.base import get_provider

try:
    pass  # optional
except Exception:
    pass


def run(text: str, profile: str | None = None, task: str = "email_summary") -> str:
    cfg = load_config("configs/base.yaml", profile)

    # Try task-specific routing first, fallback to global config
    try:
        provider, model_config = get_task_routing(task)
    except (FileNotFoundError, ValueError):
        # Fallback to global LLM config
        provider = cfg.llm.provider
        if provider == "ollama":
            model_config = {"model": cfg.llm.ollama.model}
        elif provider == "hf":
            model_config = {"model_id": cfg.llm.hf.model_id}
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    # Initialize provider
    if provider == "ollama":
        model = model_config.get("model", cfg.llm.ollama.model)
        prov = get_provider("ollama")(
            cfg.llm.ollama.endpoint, model, cfg.llm.ollama.options.model_dump()
        )
    elif provider == "hf":
        hf = cfg.llm.hf
        model_id = model_config.get("model_id", hf.model_id)
        prov = get_provider("hf")(
            model_id, hf.dtype, hf.device_map, hf.trust_remote_code, hf.max_new_tokens
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    prompt = render_email_summary(text)
    return prov.generate(prompt)
