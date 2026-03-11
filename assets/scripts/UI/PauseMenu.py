from py4godot import gdclass
from py4godot.classes.Control import Control
from py4godot.classes.Input import Input


@gdclass
class PauseMenu(Control):

    def _ready(self) -> None:
        self.input = Input.instance()

        self.center_container = self.get_node("CenterContainer")
        self.btn_resume = self.get_node("CenterContainer/VBoxContainer/Resume")
        self.btn_main_menu = self.get_node("CenterContainer/VBoxContainer/MainMenu")
        self.btn_quit = self.get_node("CenterContainer/VBoxContainer/Quit")

        self.btn_resume.pressed.connect(self._on_resume_pressed)
        self.btn_main_menu.pressed.connect(self._on_main_menu_pressed)
        self.btn_quit.pressed.connect(self._on_quit_pressed)

        self.visible = False

    def _unhandled_input(self, event) -> None:
        if not event.is_action_pressed("ui_cancel"):
            return

        if self.visible:
            self._close_menu()
        else:
            self._open_menu()

    def _open_menu(self) -> None:
        self.visible = True
        self.get_tree().paused = True
        self.input.set_mouse_mode(0)

    def _close_menu(self) -> None:
        self.visible = False
        self.get_tree().paused = False
        self.input.set_mouse_mode(2)

    def _on_resume_pressed(self) -> None:
        self._close_menu()

    def _on_main_menu_pressed(self) -> None:
        self.get_tree().paused = False
        self.input.set_mouse_mode(0)
        self.visible = False
        self.get_tree().change_scene_to_file("res://assets/scenes/MainMenu/PlayMenu.tscn")

    def _on_quit_pressed(self) -> None:
        self.get_tree().quit()