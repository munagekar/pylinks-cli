import typer

from pyli.config_files import CONF_FILE  # noqa

app = typer.Typer()


@app.command()
def add(server_name: str, address: str):
    """
    Adds the Server to Pylinks-Cli

    Args:
        server_name: The name to used for testing
        address: Address of the server. Eg https://localhost.com
    """
    pass
