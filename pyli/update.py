import typer
from PyInquirer import Token, prompt, style_from_dict  # type: ignore

from pyli import list
from pyli.lro import user_set_lro

app = typer.Typer()

custom_style_2 = style_from_dict(
    {
        Token.Separator: "#6C6C6C",
        Token.QuestionMark: "#FF9D00 bold",
        # Token.Selected: '',  # default
        Token.Selected: "#5F819D",
        Token.Pointer: "#FF9D00 bold",
        Token.Instruction: "",  # default
        Token.Answer: "#5F819D bold",
        Token.Question: "",
    }
)


@app.command()
def lro():
    current_lro = list.lro(silent=True)
    print("Current LRO", current_lro)

    print("Please select teams for New LRO, After that you can order the LRO with GUI")

    current_teams = list.teams(silent=True)
    current_teams = [{"name": x["teamname"]} for x in current_teams]
    questions = [
        {"type": "checkbox", "qmark": "😃", "message": "Select Teams For MRO", "name": "Teams", "choices": current_teams}
    ]

    new_lro = prompt(questions, style=custom_style_2)
    new_lro = user_set_lro(new_lro["Teams"])
    # TODO : Set LRO Now
