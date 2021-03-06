import urllib.parse

import requests
import typer
from typer import Option

import pyli.conf as conf
import pyli.create as create
import pyli.list as list
import pyli.server as server
import pyli.update as update
from pyli.server import SERVER_ADDR, get_current_server_config, get_token

app = typer.Typer()
app.add_typer(create.app, name="create")
app.add_typer(server.app, name="server")
app.add_typer(conf.app, name="conf")
app.add_typer(list.app, name="list")
app.add_typer(update.app, name="update")


@app.command()
def join(invite_id: str = Option(..., prompt=True)):
    server_config = get_current_server_config()
    auth_header = get_token()
    headers = {"Authorization": auth_header}
    params = (("link_id", invite_id),)
    endpoint = urllib.parse.urljoin(server_config[SERVER_ADDR], "/invite")
    response = requests.get(url=endpoint, headers=headers, params=params)  # type:ignore
    print(response.status_code)
    print(response.text)


def main():
    app()


if __name__ == "__main__":
    main()
