# Import the main game logic
import main

# Import prompt_toolkit components
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Box, Frame, Label
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.application.current import get_app

# No longer directly instantiate Game with default players here.
# The Game instance will be created just before calling game_start in the main loop.


# --- UI Elements & Shared State ---
game_output = FormattedTextControl(text="Starting game...")
game_output_window = Window(content=game_output, wrap_lines=True)

menu_items = ["New Game", "Load Game", "Settings", "Quit"]
selected_index = [0]
kb = KeyBindings()


# --- Key Binding Functions ---
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


@kb.add("enter")
def select(event):
    selection = menu_items[selected_index[0]]
    if selection == "New Game":
        get_app().exit(result="start_game")  # Signal to the main loop to start the game

    elif selection == "Quit":
        get_app().exit(result="quit_app")


@kb.add("escape")
def back_to_menu(event):
    show_menu_screen()


# --- Menu Rendering Functions ---
labels = [Label("") for _ in menu_items]


def update_menu():
    for i, label in enumerate(labels):
        if i == selected_index[0]:
            label.text = f"-> {menu_items[i]}"
        else:
            label.text = f"  {menu_items[i]}"


logo_text = r"""
 ______   ______   ________        _______   ________   _________  _________  __       ______      
/_____/\ /_____/\ /_______/\     /_______/\ /_______/\ /________/\/________/\/_/\     \::::_\/_    
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


def create_game_screen():
    return HSplit([
        Frame(
            HSplit([
                game_output_window
            ], padding=1),
            title="Battleship - Game View"
        )
    ])


# --- Application Setup ---
layout = Layout(container=menu_screen)


def show_menu_screen():
    update_menu()
    layout.container = menu_screen


style = Style.from_dict({
    "frame.border": "cyan",
    "label": "bold",
    "selected-label": "bg:#00FF00 #000000",
})

app = Application(
    layout=layout,
    key_bindings=kb,
    style=style,
    full_screen=True
)

# --- Run the Application Loop ---
if __name__ == "__main__":
    while True:
        update_menu()

        menu_action = app.run()

        if menu_action == "start_game":
            # Clear the prompt_toolkit menu screen before asking for names
            main.clear_screen()
            print("\n" + "=" * 40)
            print("    Starting Battleship Game! Good Luck!")
            print("=" * 40 + "\n")


            # --- END NEW ---

            # Create a fresh Game instance *here*, right before starting the game
            game_instance = main.Game()
            # Pass the collected names to game_start()
            game_completed_successfully = game_instance.game_start()

            if game_completed_successfully:
                print("\n" + "=" * 40)
                print("       Game Over! Thanks for playing!")
                print("=" * 40 + "\n")
                break
            else:
                print("\nReturning to main menu...")
                # No need to re-instantiate game_instance here, as it will be done on the next "New Game" selection
                main.clear_screen()
                continue

        elif menu_action == "quit_app":
            print("\nExiting Battleship. Goodbye!")
            break
        else:
            print("An unexpected menu action occurred. Exiting.")
            break
