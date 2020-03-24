import typer

import pyli.conf as conf
import pyli.server as server

app = typer.Typer()

app.add_typer(server.app, name="server")
app.add_typer(conf.app, name="conf")


def main():
    app()


if __name__ == "__main__":
    main()
