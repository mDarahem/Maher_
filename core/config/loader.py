from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Any, Optional
import os
import yaml
import re

_ENV = re.compile(r"\$\{env:(?:(int|float|bool):)?([A-Z0-9_]+),\s*([^}]+)\}")


def _coerce(t: Optional[str], v: str):
    if t == "int":
        return int(v)
    if t == "float":
        return float(v)
    if t == "bool":
        return v.lower() in ("1", "true", "yes", "on")
    return v


def _resolve_env(x: Any) -> Any:
    if isinstance(x, dict):
        return {k: _resolve_env(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_resolve_env(v) for v in x]
    if isinstance(x, str):

        def replacer(m):
            default_val = m.group(3)
            # Remove quotes from default values
            if default_val.startswith('"') and default_val.endswith('"'):
                default_val = default_val[1:-1]
            return str(_coerce(m.group(1), os.environ.get(m.group(2), default_val)))

        return _ENV.sub(replacer, x)
    return x


class OllamaOptions(BaseModel):
    num_ctx: Optional[int] = 4096
    num_predict: Optional[int] = 512
    temperature: float = 0.2
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.05


class OllamaCfg(BaseModel):
    endpoint: str = "http://localhost:11434/api/generate"
    model: str = "qwen:4b"
    options: OllamaOptions = Field(default_factory=OllamaOptions)


class HFCfg(BaseModel):
    model_id: str = "Qwen/Qwen2.5-7B-Instruct"
    dtype: str = "bfloat16"
    device_map: str = "auto"
    trust_remote_code: bool = False
    max_new_tokens: int = 512


class LLMCfg(BaseModel):
    provider: str = "ollama"
    ollama: OllamaCfg = Field(default_factory=OllamaCfg)
    hf: HFCfg = Field(default_factory=HFCfg)


class RuntimeCfg(BaseModel):
    output_dir: str = "output"
    log_level: str = "INFO"


class PromptingCfg(BaseModel):
    locale: str = "ar"
    safety: dict = Field(default_factory=lambda: {"redact_ids": True, "max_len": 2048})


class Config(BaseModel):
    runtime: RuntimeCfg = Field(default_factory=RuntimeCfg)
    llm: LLMCfg = Field(default_factory=LLMCfg)
    prompting: PromptingCfg = Field(default_factory=PromptingCfg)


def deep_merge(a: Any, b: Any) -> Any:
    if isinstance(a, dict) and isinstance(b, dict):
        out = dict(a)
        for k, v in b.items():
            out[k] = deep_merge(out.get(k), v)
        return out
    return b if b is not None else a


def load_config(base="configs/base.yaml", override: str | None = None) -> Config:
    with open(base, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if override and os.path.exists(override):
        with open(override, "r", encoding="utf-8") as f:
            over = yaml.safe_load(f) or {}
        data = deep_merge(data, over)
    data = _resolve_env(data)
    return Config.model_validate(data)
