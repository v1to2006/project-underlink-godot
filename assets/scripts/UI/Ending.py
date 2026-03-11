from py4godot import gdclass
from py4godot.classes.Control import Control
from py4godot.classes.Input import Input


@gdclass
class Ending(Control):

    def _ready(self) -> None:
        self.input = Input.instance()

        self.btn_menu = self.get_node("CenterContainer/Panel/MarginContainer/VBoxContainer/ReturnToMenu")
        self.btn_quit = self.get_node("CenterContainer/Panel/MarginContainer/VBoxContainer/Quit")

        self.btn_menu.pressed.connect(self._on_menu_pressed)
        self.btn_quit.pressed.connect(self._on_quit_pressed)

        self.input.set_mouse_mode(0)

    def _on_menu_pressed(self) -> None:
        self.get_tree().change_scene_to_file("res://assets/scenes/MainMenu/PlayMenu.tscn")

    def _on_quit_pressed(self) -> None:
        self.get_tree().quit()