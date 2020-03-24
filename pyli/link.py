import urllib.parse

import requests
import typer
from typer import Option

from pyli.server import SERVER_ADDR, get_current_server_config, get_token

app = typer.Typer()


@app.command()
def create(url: str = Option(..., prompt=True), text: str = Option(..., prompt=True)):
    server_config = get_current_server_config()
    auth_header = get_token()
    print(auth_header)
    data = f'{{"text":"{text}","link":"{url}"}}'
    endpoint = urllib.parse.urljoin(server_config[SERVER_ADDR], "/ulink/")
    headers = {"Authorization": auth_header}
    resp = requests.post(endpoint, data=data, headers=headers)
    print(resp.status_code)
    print(resp.text)
