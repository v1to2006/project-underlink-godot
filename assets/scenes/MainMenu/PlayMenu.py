from py4godot.classes import gdclass
from py4godot.classes.Control import Control


@gdclass
class PlayMenu(Control):
    def _ready(self) -> None:
        # Button references
        self.btn_new_game = self.get_node("NewGame")
        self.btn_continue = self.get_node("Continue")
        self.btn_quit = self.get_node("Quit")

        # Connect button signals
        self.btn_new_game.pressed.connect(self._on_new_game_pressed)
        self.btn_continue.pressed.connect(self._on_continue_pressed)
        self.btn_quit.pressed.connect(self._on_quit_pressed)

        # Example: disable Continue until account/save exists
        if not self._account_exists():
            self.btn_continue.disabled = True

    def _on_new_game_pressed(self) -> None:
        print("New Game pressed")

        success = self._create_new_account()

        if success:
            print("New account created successfully")
            self.get_tree().change_scene_to_file("res://Scenes/ScannerConsole.tscn")
        else:
            print("Failed to create new account")

    def _on_continue_pressed(self) -> None:
        print("Continue pressed")

        success = self._load_existing_account()

        if success:
            print("Account loaded successfully")
            self.get_tree().change_scene_to_file("res://Scenes/ScannerConsole.tscn")
        else:
            print("Failed to load account")

    def _on_quit_pressed(self) -> None:
        print("Quit pressed")
        self.get_tree().quit()

    def _account_exists(self) -> bool:
        # Placeholder:
        # later this should check your database
        return False

    def _create_new_account(self) -> bool:
        # Placeholder:
        # later connect to school DB and insert new player row
        return True

    def _load_existing_account(self) -> bool:
        # Placeholder:
        # later connect to school DB and read player/account row
        return True