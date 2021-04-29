import json
import sys
from random import shuffle

import PySimpleGUI as sg

# SET CONSTANTS
sg.theme("DarkPurple6")
FONT = ("", 13)
LARGE_FONT = ("", 15)
LOGO_FILE = "./resources/werewolf.png"
LANG, _ = sg.Window("Choose Language",
                    layout=[[sg.Column([
                        [sg.Image(filename=LOGO_FILE, background_color=sg.theme_background_color())],
                        [sg.Button("English", key="english")],
                        [sg.Button("Deutsch", key="german")],
                        [sg.Button("Quit")]
                    ], element_justification="center")]],
                    finalize=True,
                    font=FONT).read(close=True)
if LANG not in ("english", "german"):
    sys.exit()

# GET FILE DATA
with open("./resources/character.json") as character_file:
    characters = json.load(character_file).get(LANG)
with open("./resources/data.json") as data_file:
    data = json.load(data_file).get(LANG)
    help_text = data.get("help_text")
    players = data.get("default_players")
    character_count = data.get("character_count")


def display_results(entered_players, entered_characters):
    shuffle(entered_characters)
    combination = [[player, character] for player, character in zip(entered_players, entered_characters)]

    sg.Window(title="🐺👱🧙", font=LARGE_FONT, force_toplevel=True, finalize=True,
              layout=[
                  [sg.Column([[
                      sg.Table(values=combination,
                               headings=["🧒🕵️🥷", "🐺🧙🧟"],
                               auto_size_columns=True,
                               font=LARGE_FONT,
                               num_rows=min(25, len(combination)))
                  ]])]
              ]).read(close=True)


def build_row(character: str, values):
    """
    creates a gui row for each Werewolf-Character
    :param character: The name of the character
    :param values: The Data of the character
    :return: the row
    """
    return [sg.Text(character, size=(23, 1)),
            sg.Button("❔", key=f'?-{character}'),
            sg.Input(default_text=str(values.get("default count", 0)),
                     key=f'count-{character}',
                     size=(4, 1),
                     enable_events=True,
                     justification="center")]


left_col = sg.Column([
    [sg.Image(filename=LOGO_FILE, background_color=sg.theme_background_color())],
    [sg.HSep()],
    [sg.Text("MIT License\nCopyright (c)\n2021 Valentin Kolb", size=(15, 25))]
],
    vertical_alignment="top",
    justification="center")
middle_col = sg.Column(
    [build_row(character, values) for character, values in characters.items()],
    scrollable=True,
    vertical_scroll_only=True,
)
right_col = sg.Multiline(default_text=players, key="players", size=(30, 36), font=LARGE_FONT)
footer = sg.Column([
    [sg.Text(key="character_count", size=(30, 1), justification="right"),
     sg.Button("🤔", key="help"),
     sg.Button("🔀", key="shuffle")]
],
    justification="right")

layout = [
    [left_col, middle_col, right_col],
    [footer]
]

if __name__ == '__main__':
    window = sg.Window("WerWoWasWolf", layout=layout, finalize=True, font=FONT)
    _, value = window.read(0)
    while True:
        # update count
        count = 0
        for val in [val for key, val in value.items() if key.startswith("count-")]:
            try:
                count += int(val)
            except ValueError:
                continue
        window["character_count"].update(character_count.format(character_count=count))

        # get gui events
        event, value = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event.startswith("?-"):
            _, key = event.split("-")
            sg.popup(characters[key]["help"], title=key, non_blocking=True, font=FONT)
        elif event == "help":
            sg.popup(help_text, title="🤔", non_blocking=True, font=FONT)
        elif event == "shuffle":
            entered_players = [player.strip() for player in value["players"].split("\n") if player]
            entered_characters = []
            for char, count in [(key, count) for key, count in value.items() if key.startswith("count-")]:
                _, char = char.split("-")
                try:
                    entered_characters.extend([char] * int(count))
                except ValueError:
                    continue
            display_results(entered_players, entered_characters)

    window.close()
