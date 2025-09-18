from pathlib import Path
from typing import Optional

def render_email_summary(text: str, root: str=".", shots_path: Optional[str]=None) -> str:
    sys = Path(root) / "promptpacks/email_summary/system.md"
    usr = Path(root) / "promptpacks/email_summary/user.md"
    system = sys.read_text(encoding="utf-8")
    user = usr.read_text(encoding="utf-8").replace("{{text}}", text)
    return f"{system}\n\n{user}"
