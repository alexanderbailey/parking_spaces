import typer

from .migrations import app as migrations_app
from .server import app as server_app

options = {
    "context_settings": dict(help_option_names=["-h", "--help"]),
    "no_args_is_help": True,
}

app = typer.Typer(add_completion=False, **options)

app.add_typer(migrations_app, name="migrations", **options)
app.add_typer(server_app, name="server", **options)

if __name__ == "__main__":
    app()
