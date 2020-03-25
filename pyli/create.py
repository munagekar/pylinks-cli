import urllib.parse

import requests
import typer
from typer import Option

from pyli.server import SERVER_ADDR, get_current_server_config, get_token

app = typer.Typer()

ROLES = ["reader", "writer", "admin"]


def complete_roles(incomplete: str):
    completion = []
    for name in ROLES:
        if name.startswith(incomplete):
            completion.append(name)
    return completion


@app.command()
def link(
    url: str = Option(..., prompt=True), text: str = Option(..., prompt=True), team: str = Option("", prompt=True)
):
    server_config = get_current_server_config()
    auth_header = get_token()

    if team:
        data = f'{{"text":"{text}","link":"{url}","team":"{team}"}}'
    else:
        data = f'{{"text":"{text}","link":"{url}"}}'

    endpoint = urllib.parse.urljoin(server_config[SERVER_ADDR], "/link/")
    headers = {"Authorization": auth_header}
    resp = requests.post(endpoint, data=data, headers=headers)
    print(resp.status_code)
    print(resp.text)


@app.command()
def team(teamname: str):
    server_config = get_current_server_config()
    auth_header = get_token()
    headers = {"Authorization": auth_header}
    params = (("teamname", teamname),)
    endpoint = urllib.parse.urljoin(server_config[SERVER_ADDR], "/team")
    response = requests.post(url=endpoint, headers=headers, params=params)
    print(response.status_code)
    print(response.text)


@app.command()
def invite(teamname: str = Option(..., prompt=True), role: str = Option(..., prompt=True)):
    server_config = get_current_server_config()
    auth_header = get_token()
    role = role.lower()
    headers = {"Authorization": auth_header}
    endpoint = urllib.parse.urljoin(server_config[SERVER_ADDR], "/invite")

    params = (
        ("teamname", teamname),
        ("role", role),
    )
    response = requests.post(url=endpoint, headers=headers, params=params)
    print(response.status_code)
    print(response.text)
