from py4godot.classes import gdclass
from py4godot.classes.Control import Control


@gdclass
class EnterYourUsername(Control):

    def _ready(self) -> None:
        self.username_input = self.get_node("VBoxContainer/UsernameInput")
        self.btn_confirm = self.get_node("VBoxContainer/Confirm")
        self.btn_back = self.get_node("VBoxContainer/Back")
        self.status_label = self.get_node("VBoxContainer/StatusLabel")

        self.btn_confirm.pressed.connect(self._on_confirm_pressed)
        self.btn_back.pressed.connect(self._on_back_pressed)

        self.status_label.text = "Waiting for input"

    def _on_confirm_pressed(self) -> None:
        username = self.username_input.text.strip()

        if username == "":
            self.status_label.text = "Username cannot be empty"
            return

        self.status_label.text = "Username accepted"
        print("Entered username:", username)

        # Later:
        # send username to Flask here

    def _on_back_pressed(self) -> None:
        self.get_tree().change_scene_to_file("res://scenes/MainMenu/PlayMenu.tscn")