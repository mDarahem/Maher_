from core.config.loader import load_config


def test_config_loads():
    cfg = load_config("configs/base.yaml")
    assert cfg.runtime.output_dir
    assert cfg.llm.provider in ("ollama", "hf")
