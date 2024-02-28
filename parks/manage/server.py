import typer
import uvicorn


options = {
    "context_settings": dict(help_option_names=["-h", "--help"]),
    "no_args_is_help": True,
}
app = typer.Typer()


@app.command()
def serve(
    host: str = typer.Option(
        "0.0.0.0",
        "-ho",
        "--host",
        help="Port to host Fastapi on",
    ),
    port: int = typer.Option(
        8000,
        "-p",
        "--port",
        help="Port to host Fastapi on",
    ),
    reload: bool = typer.Argument(
        default=False,
        help="Reload code on saves",
        envvar="dev_reload",
    ),
):
    uvicorn.run("parks.server:app", host=host, port=port, reload=reload)
