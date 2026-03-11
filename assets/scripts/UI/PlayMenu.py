from py4godot import gdclass
from py4godot.classes.Control import Control


@gdclass
class PlayMenu(Control):

    def _ready(self) -> None:
        game_data_node = self.get_node("/root/GameData")
        self.game_data = game_data_node.get_pyscript()

        self.panel = self.get_node("CenterContainer/TerminalPanel")
        self.title_label = self.get_node("CenterContainer/TerminalPanel/VBoxContainer/TitleLabel")
        self.subtitle_label = self.get_node("CenterContainer/TerminalPanel/VBoxContainer/SubtitleLabel")
        self.status_label = self.get_node("CenterContainer/TerminalPanel/VBoxContainer/StatusLabel")

        self.btn_new = self.get_node("CenterContainer/TerminalPanel/VBoxContainer/NewGame")
        self.btn_continue = self.get_node("CenterContainer/TerminalPanel/VBoxContainer/Continue")
        self.btn_quit = self.get_node("CenterContainer/TerminalPanel/VBoxContainer/Quit")
        self.btn_logout = self.get_node("CenterContainer/TerminalPanel/VBoxContainer/Logout")
        self.logged_in_label = self.get_node("CenterContainer/TerminalPanel/VBoxContainer/LoggedInLabel")

        self.btn_new.pressed.connect(self._on_new_pressed)
        self.btn_continue.pressed.connect(self._on_continue_pressed)
        self.btn_quit.pressed.connect(self._on_quit_pressed)
        self.btn_logout.pressed.connect(self._on_logout_pressed)

        self.title_label.text = "DEEP DRIFT"
        self.subtitle_label.text = "SALVAGE NAVIGATION TERMINAL"

        if not self.game_data.is_logged_in():
            self.get_tree().change_scene_to_file("res://assets/scenes/MainMenu/EnterYourUsername.tscn")
            return

        self.logged_in_label.text = f"Logged in as: {self.game_data.username}"

        if self.game_data.has_active_save():
            self.status_label.text = "SYSTEM READY"
        else:
            self.status_label.text = "No active save found"

    def _on_new_pressed(self) -> None:
        self.status_label.text = "STARTING NEW EXPEDITION..."

        if not self.game_data.start_new_game():
            self.status_label.text = "Failed to start new game"
            return

        self.get_tree().change_scene_to_file("res://assets/scenes/Expedition.tscn")

    def _on_continue_pressed(self) -> None:
        if not self.game_data.has_active_save():
            self.status_label.text = "No active save to continue"
            return

        self.status_label.text = "LOADING EXPEDITION..."
        self.get_tree().change_scene_to_file("res://assets/scenes/Expedition.tscn")

    def _on_logout_pressed(self) -> None:
        self.game_data.logout()
        self.get_tree().change_scene_to_file("res://assets/scenes/MainMenu/EnterYourUsername.tscn")

    def _on_quit_pressed(self) -> None:
        self.get_tree().quit()