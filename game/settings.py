import main
import asyncio
import pygame

from prompt_toolkit import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Frame, Label, Dialog, Button, RadioList
from prompt_toolkit.layout.containers import HSplit, Window, FloatContainer, Float
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.styles import Style

# ─── STYLES ────────────────────────────────────────────────────────────
style_main = Style.from_dict({
    # Only for the main menu
    "frame.border": "cyan",
    "label":        "bold",
})
style_settings = Style.from_dict({
    # Only for settings dialogs
    "":                   "bg:cyan",        # entire background
    "shadow":             "bg:cyan",        # any shadows
    "dialog.body":        "bg:cyan",
    "dialog.body text":   "bg:cyan",
    "dialog.frame.label": "bg:cyan",
    "radiolist":          "bg:cyan",
})

# ─── INIT PYGAME ───────────────────────────────────────────────────────
pygame.mixer.init()

# ─── SHARED STATE ─────────────────────────────────────────────────────
game_instance    = main.Game()
menu_items       = ["New Game", "Settings", "Quit"]
selected_index   = [0]
selected_players = ["1"]
music_playing    = [False]

# ─── MAIN MENU KEYBINDINGS ─────────────────────────────────────────────
kb = KeyBindings()

@kb.add("up")
def move_up(event):
    selected_index[0] = (selected_index[0] - 1) % len(menu_items)
    draw_menu()

@kb.add("down")
def move_down(event):
    selected_index[0] = (selected_index[0] + 1) % len(menu_items)
    draw_menu()

@kb.add("enter")
def enter_main(event):
    choice = menu_items[selected_index[0]]
    if choice == "New Game":
        get_app().exit(result="start_game")
    elif choice == "Settings":
        get_app().exit(result="settings")
    else:
        get_app().exit(result="quit")

# ─── RENDER MAIN MENU ───────────────────────────────────────────────────
labels = [Label("") for _ in menu_items]
logo = Window(
    content=FormattedTextControl(r"""
 ______   ______   ________        _______   ________   _________  _________  __       ______      
/_____/\ /_____/\ /_______/\     /_______/\ /_______/\ /________/\/________/\/_/\     /_____/\     
\::::_\/_\::::_\/_\::: _  \ \    \::: _  \ \\::: _  \ \\__.::.__\/\__.::.__\/\:\ \    \::::_\/_    
 \:\/___/\\:\/___/\\::(_)  \ \    \::(_)  \/_\::(_)  \ \  \::\ \     \::\ \   \:\ \    \:\/___/\   
  \_::._\:\\::___\/_\:: __  \ \    \::  _  \ \\:: __  \ \  \::\ \     \::\ \   \:\ \____\::___\/_  
    /____\:\\:\____/\\:.\ \  \ \    \::(_)  \ \\:.\ \  \ \  \::\ \     \::\ \   \:\/___/\\:\____/\ 
    \_____\/ \_____\/ \__\/\__\/     \_______\/ \__\/\__\/   \__\/      \__\/    \_____\/ \_____\/ 
"""),
    height=D.exact(8),
    style="bold cyan"
)
menu_frame  = Frame(HSplit([logo, *labels], padding=1), title="Battleship Menu")
menu_screen = HSplit([menu_frame])
layout      = Layout(container=menu_screen)

app = Application(
    layout=layout,
    key_bindings=kb,
    style=style_main,     # <- only main menu gets style_main
    full_screen=True,
)

def draw_menu():
    for i, lbl in enumerate(labels):
        lbl.text = ("→ " if i == selected_index[0] else "  ") + menu_items[i]

# ─── CUSTOM SETTINGS DIALOGS ───────────────────────────────────────────
async def do_settings():
    # Helpers for music
    def play_music():
        pygame.mixer.music.load("C:/Users/user/Music/forgiveness.mp3") # Give path to music file (e. g. C:/Users/user/........../aaa.mp3)
        pygame.mixer.music.play(-1)
        music_playing[0] = True

    def stop_music():
        pygame.mixer.music.stop()
        music_playing[0] = False

    # --- Dialog 1: Players ---
    player_radio = RadioList(
        values=[
            ("1","1 Player"),
            ("2","2 Players"),
            ("3","3 Players"),
            ("4","4 Players"),
        ],
        default=selected_players[0]
    )

    dlg_players = Dialog(
        title="Settings: Players",
        body=player_radio,
        buttons=[
            Button(text=" OK ", handler=lambda: app_players.exit(result="ok")),
            Button(text="Cancel", handler=lambda: app_players.exit(result=None)),
        ],
        width=D(preferred=60),
        with_background=False,
    )

    root1 = FloatContainer(
        content=Window(char=" ", style="bg:black", always_hide_cursor=True),
        floats=[Float(content=dlg_players, top=2, left=10)]
    )

    app_players = Application(
        layout=Layout(root1),
        style=style_settings,   # <- only settings use cyan style
        full_screen=True,
    )

    res = await app_players.run_async()
    if res == "ok":
        selected_players[0] = player_radio.current_value

    # --- Dialog 2: Music ---
    music_radio = RadioList(
        values=[("on","ON"),("off","OFF")],
        default="on" if music_playing[0] else "off"
    )

    dlg_music = Dialog(
        title="Settings: Music",
        body=music_radio,
        buttons=[
            Button(text=" OK ", handler=lambda: app_music.exit(result="ok")),
            Button(text="Cancel", handler=lambda: app_music.exit(result=None)),
        ],
        width=D(preferred=50),
        with_background=False,
    )

    root2 = FloatContainer(
        content=Window(char=" ", style="bg:black", always_hide_cursor=True),
        floats=[Float(content=dlg_music, top=2, left=12)]
    )

    app_music = Application(
        layout=Layout(root2),
        style=style_settings,   # <- settings style again
        full_screen=True,
    )

    res = await app_music.run_async()
    if res == "ok":
        choice = music_radio.current_value
        if choice == "on" and not music_playing[0]:
            play_music()
        elif choice == "off" and music_playing[0]:
            stop_music()

# ─── MAIN LOOP ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    draw_menu()
    while True:
        action = asyncio.run(app.run_async())

        if action == "start_game":
            main.clear_screen()
            print("\n" + "=" * 40)
            print("    Starting Battleship Game! Good Luck!")
            print("=" * 40 + "\n")
            done = game_instance.game_start()
            if done:
                print("Game over! Goodbye.")
                break
            else:
                game_instance = main.Game()
                draw_menu()
                continue

        elif action == "settings":
            asyncio.run(do_settings())  # Settings dialogs with cyan BG
            draw_menu()
            continue

        else:  # Quit
            print("Goodbye!")
            break
