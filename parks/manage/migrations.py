from pathlib import Path
from subprocess import run
from typing import Optional

import typer
from template_reverse import ReverseTemplate
from yoyo import get_backend
from yoyo import read_migrations

from parks.config import db_url
from .utils import is_tool

app = typer.Typer()


@app.command()
def apply(url: Optional[str] = typer.Argument(None, help="Database URL")):
    backend = get_backend(url if url else db_url)
    migrations = read_migrations("parks/migrations")

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


@app.command()
def rollback(url: str = typer.Argument(..., help="Database URL")):
    if not (is_tool("yoyo")):
        typer.echo("Can't find yoyo, is the yoyo-migrations package installed?")
        raise typer.Exit()

    migrations_path = Path.cwd() / "parks/migrations"

    cmd = "yoyo", "rollback", migrations_path, "-d", url, "-b"

    run(cmd)


@app.command()
def create(
    name: str = typer.Option(
        ...,
        help="Migration name (prompts)",
        prompt=True,
        callback=lambda x: x.strip(),
    )
):
    if not (is_tool("yoyo")):
        typer.echo("Can't find yoyo, is the yoyo-migrations package installed?")
        raise typer.Exit()

    migrations_path = Path.cwd() / "parks/migrations"

    cmd = "yoyo", "new", migrations_path, "-m", name, "--sql", "-b"

    run(cmd)