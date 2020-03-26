import typer

from pyli import list

app = typer.Typer()


@app.command()
def lro():
    current_lro = list.lro(silent=True)
    current_teams = list.teams(silent=True)
    print("Current LRO:", current_lro)
    print("Current Teams", current_teams)
