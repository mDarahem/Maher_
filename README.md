# Maher — A+ Scaffold

## Quick Start (Dev)
```bash
python -m venv .venv && . .venv/Scripts/activate  # Windows
pip install -e .
cp .env.example .env
maher --help
maher analyze --text samples.txt --profile configs/profiles/lab.yaml
```

## Lab (Compose)

```bash
docker compose -f deploy/docker/docker-compose.lab.yml up -d --build
```

## Swap Models

* Ollama: set `LLM_PROVIDER=ollama` + `OLLAMA_MODEL`.
* HuggingFace: set `LLM_PROVIDER=hf` + `HF_MODEL_ID` (install extras: `pip install .[transformers]`).
