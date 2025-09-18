from typing import Tuple, Dict, Any
import yaml
from pathlib import Path


def get_task_routing(
    task: str, routing_file: str = "configs/routing.yaml"
) -> Tuple[str, Dict[str, Any]]:
    """Get provider and model configuration for a specific task.

    Args:
        task: Task name (e.g., 'email_summary', 'reply_suggestion')
        routing_file: Path to routing configuration file

    Returns:
        Tuple of (provider, model_config) where model_config contains
        either 'model' for ollama or 'model_id' for hf
    """
    if not Path(routing_file).exists():
        raise FileNotFoundError(f"Routing file not found: {routing_file}")

    with open(routing_file, "r", encoding="utf-8") as f:
        routing = yaml.safe_load(f) or {}

    tasks = routing.get("tasks", {})
    if task not in tasks:
        raise ValueError(
            f"Task '{task}' not found in routing config. Available: {list(tasks.keys())}"
        )

    task_config = tasks[task]
    provider = task_config["provider"]

    # Extract model config based on provider
    if provider == "ollama":
        model_config = {"model": task_config["model"]}
    elif provider == "hf":
        model_config = {"model_id": task_config["model_id"]}
    else:
        # Pass through all config for unknown providers
        model_config = {k: v for k, v in task_config.items() if k != "provider"}

    return provider, model_config
