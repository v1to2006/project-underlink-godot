from py4godot import gdclass
from py4godot.classes.Control import Control


@gdclass
class EnterYourUsername(Control):

    def _ready(self) -> None:
        game_data_node = self.get_node("/root/GameData")
        self.game_data = game_data_node.get_pyscript()

        self.username_input = self.get_node("CenterContainer/VBoxContainer/UserNameInput")
        self.btn_confirm = self.get_node("CenterContainer/VBoxContainer/Confirm")
        self.status_label = self.get_node("CenterContainer/VBoxContainer/StatusLabel")

        self.btn_confirm.pressed.connect(self._on_confirm_pressed)

        self.status_label.text = ""

        if self.game_data.is_logged_in():
            self.username_input.text = self.game_data.username

    def _on_confirm_pressed(self) -> None:
        username = self.username_input.text.strip()

        if username == "":
            self.status_label.text = "Username cannot be empty"
            return

        self.status_label.text = "Logging in..."

        if not self.game_data.login(username):
            self.status_label.text = "Login failed"
            return

        self.status_label.text = "Login successful"
        self.get_tree().change_scene_to_file("res://assets/scenes/MainMenu/PlayMenu.tscn")