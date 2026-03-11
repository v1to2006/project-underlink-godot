from py4godot import gdclass
from py4godot.classes.Control import Control


@gdclass
class Intro(Control):

    def _ready(self) -> None:
        self.btn_start = self.get_node("CenterContainer/Panel/MarginContainer/VBoxContainer/StartExpedition")

        self.btn_start.pressed.connect(self._on_start_pressed)

    def _on_start_pressed(self) -> None:
        self.get_tree().change_scene_to_file("res://assets/scenes/Expedition.tscn")
