import typer, os
from rich import print
from core.pipelines import email_summary

app = typer.Typer(help="Maher CLI")

@app.command()
def analyze(text: str = typer.Option(..., help="Plain text or path to file"),
            profile: str = typer.Option(None, help="Override config (e.g., configs/profiles/lab.yaml)")):
    if os.path.exists(text):
        text = open(text, "r", encoding="utf-8").read()
    res = email_summary.run(text, profile=profile)
    out = "output/analysis.txt"
    os.makedirs("output", exist_ok=True)
    open(out, "w", encoding="utf-8").write(res)
    print(f"[green]Wrote[/green] {out}")

if __name__ == "__main__":
    app()
