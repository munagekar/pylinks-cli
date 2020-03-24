import typer

import pyli.server as server

app = typer.Typer()

app.add_typer(server.app, name="server")


def main():
    app()


if __name__ == "__main__":
    main()
