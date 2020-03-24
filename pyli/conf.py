import typer

from pyli.config_files import CONF_FILE

app = typer.Typer()


@app.command("print")
def print_conf():
    print(CONF_FILE.read_text())


@app.command("clean")
def clean():
    CONF_FILE.unlink()
