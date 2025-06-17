from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Box, Frame, Label
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import D

from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.application.current import get_app
# import main

# game = main.Game()

game_output = FormattedTextControl(text="Starting game...")
game_output_window = Window(content=game_output, wrap_lines=True)

# === Shared State ===
menu_items = ["New Game", "Load Game", "Settings", "Quit"]
selected_index = [0]
kb = KeyBindings()
# app = None


@kb.add("up")
@kb.add("w")
def move_up(event):
    selected_index[0] = (selected_index[0] - 1) % len(menu_items)
    update_menu()


@kb.add("down")
@kb.add("s")
def move_down(event):
    selected_index[0] = (selected_index[0] + 1) % len(menu_items)
    update_menu()


# @kb.add("enter")
# def select(event):
#     selection = menu_items[selected_index[0]]
#     if selection == "New Game":
#         show_game_screen()
#     elif selection == "Quit":
#         app.exit()
#     # else:
#         # print(f"{selection} not implemented yet.")


@kb.add("enter")
def select(event):
    selection = menu_items[selected_index[0]]
    if selection == "New Game":
        app.layout.container = create_game_screen()
    elif selection == "Quit":
        app.exit()


@kb.add("escape")
def back_to_menu(event):
    show_menu_screen()


labels = [Label("") for _ in menu_items]


def update_menu():
    for i, label in enumerate(labels):
        if i == selected_index[0]:
            label.text = f"-> {menu_items[i]}"
        else:
            label.text = f"  {menu_items[i]}"

# update_menu()


logo_text = r"""
 ______   ______   ________        _______   ________   _________  _________  __       ______      
/_____/\ /_____/\ /_______/\     /_______/\ /_______/\ /________/\/________/\/_/\     /_____/\     
\::::_\/_\::::_\/_\::: _  \ \    \::: _  \ \\::: _  \ \\__.::.__\/\__.::.__\/\:\ \    \::::_\/_    
 \:\/___/\\:\/___/\\::(_)  \ \    \::(_)  \/_\::(_)  \ \  \::\ \     \::\ \   \:\ \    \:\/___/\   
  \_::._\:\\::___\/_\:: __  \ \    \::  _  \ \\:: __  \ \  \::\ \     \::\ \   \:\ \____\::___\/_  
    /____\:\\:\____/\\:.\ \  \ \    \::(_)  \ \\:.\ \  \ \  \::\ \     \::\ \   \:\/___/\\:\____/\ 
    \_____\/ \_____\/ \__\/\__\/     \_______\/ \__\/\__\/   \__\/      \__\/    \_____\/ \_____\/ 
                                                                                                   
"""
logo = Window(
    content=FormattedTextControl(logo_text),
    height=D.exact(len(logo_text.splitlines())),
    style="bold cyan",
)




menu_screen = HSplit([
    Frame(
        HSplit([logo, *labels], padding=1),
        title="Battleship Menu"
    )
])

# game_screen = HSplit([
#     Frame(
#         HSplit([
#             game.game_start()
#             # game_output_window
#         ], padding=1),
#         title="Battleship - Game View"
#     )
# ])


def create_game_screen():
    return HSplit([
        Frame(
            HSplit([
                # game.game_start()
                game_output_window

            ], padding=1),
            title="Battleship - Game View"
        )
    ])


# # Menu Screen
# # menu_container = Box(
# #     body=Frame(HSplit([logo, *labels], padding=1), title="Battleship Menu"),
# #     padding=2,
# # )
# menu_container = Frame(
#     HSplit([logo, *labels], padding=1),
#     title="Battleship Menu"
# )
#
# # Game Screen
# # game_container = Box(
# #     body=Frame(
# #         HSplit([
# #             Label(text="Game Started! Press Esc to return to menu."),
# #             Label(text="(Here you can add your game UI)")
# #         ], padding=1),
# #         title="Battleship - Game View"
# #     ),
# #     padding=2,
# # )
# game_container = Frame (
#     HSplit ([
#         Label(text="Game Started! Press Esc to return to menu."),
#         Label(text="(Here you can add your game UI)")
#     ], padding=1),
#     title="Battleship - Game View"
# )


layout = Layout(container=menu_screen)  # Start with menu


def show_menu_screen():
    update_menu()
    layout.container = menu_screen  # Valid: HSplit is a container

# def show_game_screen():
#     layout.container = game_screen  # Also valid


style = Style.from_dict({
    "frame.border": "cyan",
    "label": "bold",
})

app = Application(
    layout=layout,
    key_bindings=kb,
    style=style,
    full_screen=True
)


update_menu()
app.run()

