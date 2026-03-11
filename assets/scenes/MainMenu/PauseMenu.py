from py4godot.classes import gdclass
from py4godot.classes.Control import Control


@gdclass
class PauseMenu(Control):

    def _ready(self) -> None:
        self.btn_resume = self.get_node("VBoxContainer/Resume")
        self.btn_main_menu = self.get_node("VBoxContainer/MainMenu")
        self.btn_quit = self.get_node("VBoxContainer/Quit")

        self.btn_resume.pressed.connect(self._on_resume_pressed)
        self.btn_main_menu.pressed.connect(self._on_main_menu_pressed)
        self.btn_quit.pressed.connect(self._on_quit_pressed)

    def _on_resume_pressed(self) -> None:
        self.get_tree().paused = False
        self.visible = False

    def _on_main_menu_pressed(self) -> None:
        self.get_tree().paused = False
        self.get_tree().change_scene_to_file("res://scenes/MainMenu/PlayMenu.tscn")

    def _on_quit_pressed(self) -> None:
        self.get_tree().quit()