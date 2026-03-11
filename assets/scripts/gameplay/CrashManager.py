from py4godot import gdclass
from py4godot.classes.CanvasLayer import CanvasLayer
from py4godot.classes.AudioStreamPlayer import AudioStreamPlayer
from py4godot.classes.Input import Input


@gdclass
class CrashManager(CanvasLayer):
    play_menu_scene_path: str = "res://assets/scenes/MainMenu/PlayMenu.tscn"

    def _ready(self) -> None:
        self.input = Input.instance()
        self.explosion_player: AudioStreamPlayer = self.get_node("ExplosionPlayer")

        self.is_crashing = False
        self.redirect_timer = 0.0

        print("CrashManager ready")

    def _process(self, delta: float) -> None:
        if not self.is_crashing:
            return

        self.redirect_timer -= delta
        if self.redirect_timer <= 0.0:
            self.input.set_mouse_mode(0)
            self.get_tree().change_scene_to_file(self.play_menu_scene_path)

    def start_crash_sequence(self) -> None:
        if self.is_crashing:
            return

        print("Crash sequence started")
        self.is_crashing = True
        self.redirect_timer = 2.5

        if self.explosion_player is not None:
            self.explosion_player.play()