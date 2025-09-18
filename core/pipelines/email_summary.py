from core.prompting.renderer import render_email_summary
from core.config.loader import load_config
from adapters.llm.base import get_provider
import adapters.llm.ollama  # register
try:
    import adapters.llm.hf  # optional
except Exception:
    pass

def run(text: str, profile: str|None=None) -> str:
    cfg = load_config("configs/base.yaml", profile)
    provider = cfg.llm.provider
    if provider == "ollama":
        prov = get_provider("ollama")(cfg.llm.ollama.endpoint, cfg.llm.ollama.model, cfg.llm.ollama.options.model_dump())
    elif provider == "hf":
        hf = cfg.llm.hf
        prov = get_provider("hf")(hf.model_id, hf.dtype, hf.device_map, hf.trust_remote_code, hf.max_new_tokens)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    prompt = render_email_summary(text)
    return prov.generate(prompt)
