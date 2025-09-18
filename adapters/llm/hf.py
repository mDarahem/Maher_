from adapters.llm.base import register
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch


@register("hf")
class HFLLM:
    def __init__(
        self,
        model_id: str,
        dtype="bfloat16",
        device_map="auto",
        trust_remote_code=False,
        max_new_tokens=512,
        gen_kwargs=None,
    ):
        tok = AutoTokenizer.from_pretrained(
            model_id, trust_remote_code=trust_remote_code
        )
        mdl = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=getattr(torch, dtype, torch.bfloat16),
            device_map=device_map,
            trust_remote_code=trust_remote_code,
        )
        self.pipe = pipeline("text-generation", model=mdl, tokenizer=tok)
        self.max_new_tokens = max_new_tokens
        self.gen_kwargs = gen_kwargs or {}

    def generate(self, prompt: str, **opts) -> str:
        out = self.pipe(
            prompt,
            max_new_tokens=opts.get("max_new_tokens", self.max_new_tokens),
            do_sample=True,
            **{**self.gen_kwargs, **opts},
        )
        return out[0]["generated_text"]
