import urllib.parse
from typing import Any, Dict

import requests
import toml
import typer
from typer import Option

from pyli.config_files import CONF_FILE

app = typer.Typer()

CURRENT_SERVER = "current_server"
SERVER_CONF_KEY = "servers"
SERVER_NAME = "server_name"
SERVER_ADDR = "server_addr"
SERVER_USER = "user"


def get_current_server() -> str:
    conf = load_config()
    return conf[CURRENT_SERVER]


def load_config() -> Dict[str, Any]:
    return toml.loads(CONF_FILE.read_text())  # type: ignore


def get_server_config(server_name: str) -> Dict[str, str]:
    conf = load_config()
    server_conf = conf[SERVER_CONF_KEY][server_name]
    return server_conf


def get_current_server_config() -> Dict[str, str]:
    return get_server_config(get_current_server())


@app.command()
def add(server_name: str, addr: str = Option(...,)):
    """
    Adds the Server to Pylinks-Cli

    Args:
        server_name: The name to used for testing
        addr: Address of the server. Eg https://localhost.com
    """
    conf = load_config()
    conf[CURRENT_SERVER] = server_name

    CONF_FILE.write_text(toml.dumps(conf))

    server_config = {SERVER_ADDR: addr}

    servers: Dict[str, Dict[str, str]] = conf.get(SERVER_CONF_KEY, {})
    servers[server_name] = server_config
    conf[SERVER_CONF_KEY] = servers

    CONF_FILE.write_text(toml.dumps(conf))


@app.command()
def signup(user: str = Option(..., "-u"), password: str = Option(..., "-p")):
    """
    Sign up on the Link Server

    Args:
        user : Username
        password: Password
    """
    server_config = get_current_server_config()
    server_address = server_config[SERVER_ADDR]

    endpoint = urllib.parse.urljoin(server_address, "/user/")
    data = f'{{"username":"{user}","password":"{password}"}}'
    resp = requests.post(endpoint, data=data)
    print(resp)
