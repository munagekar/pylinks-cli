import time
import urllib.parse
from getpass import getpass
from typing import Any, Dict, Optional

import jwt
import requests
import toml
import typer
from typer import Option

from pyli.config_files import CONF_FILE, TOKEN_DIR

app = typer.Typer()

CURRENT_SERVER = "current_server"
SERVER_CONF_KEY = "servers"
SERVER_NAME = "server_name"
SERVER_ADDR = "server_addr"
SERVER_USER = "user"


# TODO : Covert Config to Class and make this readable


def get_current_server() -> str:
    conf = load_config()
    return conf[CURRENT_SERVER]


def load_config() -> Dict[str, Any]:
    return toml.loads(CONF_FILE.read_text())  # type: ignore


def write_config(config):
    CONF_FILE.write_text(toml.dumps(config))


def get_server_config(server_name: str) -> Dict[str, str]:
    conf = load_config()
    server_conf = conf[SERVER_CONF_KEY][server_name]
    return server_conf


def update_server_config(server_name: str, config):
    conf = load_config()
    conf[SERVER_CONF_KEY][server_name] = config
    write_config(conf)


def update_curent_server_config(config):
    update_server_config(get_current_server(), config)


def get_current_server_config() -> Dict[str, str]:
    return get_server_config(get_current_server())


def add(server_name: str, addr: str = Option(..., "-a")):
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
def signup(
    server_name: str = Option("default", prompt=True),
    server_address: str = Option(..., prompt=True),
    user: str = Option(..., "-u", prompt=True),
    password: str = Option(..., "-p", prompt=True, confirmation_prompt=True, hide_input=True),
):
    """
    Sign up on the Link Server

    Args:
        user : Username
        password: Password
    """
    add(server_name, server_address)
    server_config = get_current_server_config()
    server_address = server_config[SERVER_ADDR]
    server_config[SERVER_USER] = user

    endpoint = urllib.parse.urljoin(server_address, "/user/")
    data = f'{{"username":"{user}","password":"{password}"}}'
    resp = requests.post(endpoint, data=data)
    print(resp.status_code)
    print(resp.text)

    if resp.status_code == 200:
        update_curent_server_config(server_config)
        create_token(password)


@app.command()
def set(user: Optional[str] = Option(None, "-u"), address: Optional[str] = Option("-a")):
    server_config = get_current_server_config()
    if user:
        server_config[SERVER_USER] = user
    if address:
        server_config[SERVER_ADDR] = address

    update_curent_server_config(server_config)


def create_token(password: Optional[str] = None) -> str:
    server_config = get_current_server_config()
    username = server_config[SERVER_USER]

    if not password:
        password = getpass(f"Please Enter Password for username={username} To Refresh Token\n:")
    tokenfile = TOKEN_DIR / get_current_server()

    data = f'{{"username":"{username}","password":"{password}"}}'
    endpoint = urllib.parse.urljoin(server_config[SERVER_ADDR], "/jwt/")
    resp = requests.post(endpoint, data=data)

    if resp.status_code == 200:
        tokenfile.write_text(resp.text)
        return resp.text
    else:
        print("Incorrect Password")
        return create_token()


def read_token():
    tokenfile = TOKEN_DIR / get_current_server()
    if not tokenfile.exists():
        return None
    token = tokenfile.read_text()
    token = token.strip('"')
    return token


def token_is_expired(token: str) -> bool:
    _, _, token_core = token.partition(" ")
    decoded = jwt.decode(token_core.encode(), verify=False)
    exp = decoded["exp"]
    if exp - 5 < time.time():
        return True
    return False


def get_token():
    token = read_token()
    if token and not token_is_expired(token):
        return token

    return create_token()
