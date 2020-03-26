import json
import urllib

import requests
import typer

from pyli.server import SERVER_ADDR, get_current_server_config, get_token

app = typer.Typer()


@app.command()
def teams(silent: bool = False):
    server_config = get_current_server_config()
    auth_header = get_token()
    headers = {"Authorization": auth_header}
    endpoint = urllib.parse.urljoin(server_config[SERVER_ADDR], "/team")
    response = requests.get(url=endpoint, headers=headers)
    if not silent:
        print(response.status_code)
        print(response.text)

    return json.loads(response.text)


@app.command()
def lro(silent: bool = False):
    server_config = get_current_server_config()
    auth_header = get_token()
    headers = {"Authorization": auth_header}
    endpoint = urllib.parse.urljoin(server_config[SERVER_ADDR], "/lro")
    response = requests.get(url=endpoint, headers=headers)
    if not silent:
        print(response.status_code)
        print(response.text)
    return json.loads(response.text)
