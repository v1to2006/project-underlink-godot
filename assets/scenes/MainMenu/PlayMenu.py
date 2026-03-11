import random

from py4godot.classes import gdclass
from py4godot.classes.Control import Control


@gdclass
class PlayMenu(Control):

    def _ready(self) -> None:
        self.panel = self.get_node("TerminalPanel")
        self.title_label = self.get_node("TerminalPanel/VBox/TitleLabel")
        self.subtitle_label = self.get_node("TerminalPanel/VBox/SubtitleLabel")
        self.status_label = self.get_node("TerminalPanel/VBox/StatusLabel")

        self.btn_new = self.get_node("TerminalPanel/VBox/NewGame")
        self.btn_continue = self.get_node("TerminalPanel/VBox/Continue")
        self.btn_quit = self.get_node("TerminalPanel/VBox/Quit")

        self.flicker_timer = self.get_node("FlickerTimer")

        self.btn_new.pressed.connect(self._on_new_pressed)
        self.btn_continue.pressed.connect(self._on_continue_pressed)
        self.btn_quit.pressed.connect(self._on_quit_pressed)

        self.flicker_timer.timeout.connect(self._on_flicker)
        self.flicker_timer.wait_time = 0.08
        self.flicker_timer.start()

        self.full_subtitle = "SALVAGE NAVIGATION TERMINAL"
        self.current_index = 0
        self.subtitle_label.text = ""
        self.status_label.text = "BOOTING..."

    def _process(self, delta: float) -> None:
        # Simple typewriter effect for subtitle
        if self.current_index < len(self.full_subtitle):
            self.current_index += 1
            self.subtitle_label.text = self.full_subtitle[:self.current_index]
        elif self.status_label.text == "BOOTING...":
            self.status_label.text = "SYSTEM READY"

    def _on_flicker(self) -> None:
        # Slight flicker by changing panel alpha a bit
        try:
            color = self.panel.modulate
            color.a = random.uniform(0.92, 1.0)
            self.panel.modulate = color
        except Exception:
            pass

    def _on_new_pressed(self) -> None:
        self.status_label.text = "OPENING USER REGISTRATION..."
        self.get_tree().change_scene_to_file("res://scenes/MainMenu/EnterYourUsername.tscn")

    def _on_continue_pressed(self) -> None:
        self.status_label.text = "AWAITING SAVE LINK..."
        print("Continue pressed")

    def _on_quit_pressed(self) -> None:
        self.get_tree().quit()