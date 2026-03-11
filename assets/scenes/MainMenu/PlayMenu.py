from py4godot import gdclass
from py4godot.classes.Control import Control


@gdclass
class PlayMenu(Control):

    def _ready(self) -> None:
        self.panel = self.get_node("CenterContainer/TerminalPanel")
        self.title_label = self.get_node("CenterContainer/TerminalPanel/VBoxContainer/TitleLabel")
        self.subtitle_label = self.get_node("CenterContainer/TerminalPanel/VBoxContainer/SubtitleLabel")
        self.status_label = self.get_node("CenterContainer/TerminalPanel/VBoxContainer/StatusLabel")

        self.btn_new = self.get_node("CenterContainer/TerminalPanel/VBoxContainer/NewGame")
        self.btn_continue = self.get_node("CenterContainer/TerminalPanel/VBoxContainer/Continue")
        self.btn_quit = self.get_node("CenterContainer/TerminalPanel/VBoxContainer/Quit")

        self.panel.visible = True
        self.title_label.visible = True
        self.subtitle_label.visible = True
        self.status_label.visible = True
        self.btn_new.visible = True
        self.btn_continue.visible = True
        self.btn_quit.visible = True

        self.title_label.text = "UNDERLINK"
        self.subtitle_label.text = "SALVAGE NAVIGATION TERMINAL"
        self.status_label.text = "SYSTEM READY"

        self.btn_new.pressed.connect(self._on_new_pressed)
        self.btn_continue.pressed.connect(self._on_continue_pressed)
        self.btn_quit.pressed.connect(self._on_quit_pressed)

    def _on_new_pressed(self) -> None:
        self.status_label.text = "OPENING USER REGISTRATION..."
        self.get_tree().change_scene_to_file("res://scenes/MainMenu/EnterYourUsername.tscn")

    def _on_continue_pressed(self) -> None:
        self.status_label.text = "AWAITING SAVE LINK..."
        print("Continue pressed")

    def _on_quit_pressed(self) -> None:
        self.get_tree().quit()