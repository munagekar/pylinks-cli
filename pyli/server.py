from typing import Dict

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


@app.command()
def add(server_name: str, addr: str = Option(...,), user: str = Option(...)):
    """
    Adds the Server to Pylinks-Cli

    Args:
        server_name: The name to used for testing
        addr: Address of the server. Eg https://localhost.com
        user: Username to be used with the server
    """
    conf = toml.loads(CONF_FILE.read_text())
    conf[CURRENT_SERVER] = server_name

    CONF_FILE.write_text(toml.dumps(conf))

    server_config = {SERVER_ADDR: addr, SERVER_USER: user}

    servers: Dict[str, Dict[str, str]] = conf.get(SERVER_CONF_KEY, {})
    servers[server_name] = server_config
    conf[SERVER_CONF_KEY] = servers

    CONF_FILE.write_text(toml.dumps(conf))
