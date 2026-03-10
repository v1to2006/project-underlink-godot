from py4godot import gdclass
from py4godot.classes.Node3D import Node3D
from py4godot.classes.core import Vector3

@gdclass
class CockpitButton(Node3D):
    action_name: str = ""
    drill_node_path: str = "/root/Expedition/ProxyCube"

    press_depth: float = 0.02
    press_time: float = 0.15

    def _ready(self) -> None:
        self.base_position = self.position
        self.is_pressed_visual: bool = False
        self.is_being_held: bool = False
        self.press_timer: float = 0.0

    def _process(self, delta: float) -> None:
        if self.is_being_held:
            return

        if not self.is_pressed_visual:
            return

        self.press_timer -= delta
        if self.press_timer <= 0.0:
            self.position = self.base_position
            self.is_pressed_visual = False

    def interact(self) -> None:
        self._press_visual_once()

        drill_script = self._get_drill_script()
        if drill_script is None:
            return

        if hasattr(drill_script, "start_button"):
            drill_script.start_button(self.action_name)
        if hasattr(drill_script, "stop_button"):
            drill_script.stop_button(self.action_name)

    def begin_hold(self) -> None:
        self.is_being_held = True
        self.is_pressed_visual = True
        self._set_pressed_visual()

        drill_script = self._get_drill_script()
        if drill_script is None:
            return

        if hasattr(drill_script, "start_button"):
            drill_script.start_button(self.action_name)

    def end_hold(self) -> None:
        self.is_being_held = False
        self.press_timer = self.press_time

        drill_script = self._get_drill_script()
        if drill_script is None:
            return

        if hasattr(drill_script, "stop_button"):
            drill_script.stop_button(self.action_name)

    def _get_drill_script(self):
        if self.drill_node_path == "":
            print("CockpitButton: drill_node_path is empty")
            return None

        drill_node = self.get_node(self.drill_node_path)
        if drill_node is None:
            print("CockpitButton: drill node not found")
            return None

        drill_script = drill_node.get_pyscript()
        if drill_script is None:
            print("CockpitButton: drill node has no python script")
            return None

        return drill_script

    def _press_visual_once(self) -> None:
        self.is_being_held = False
        self.is_pressed_visual = True
        self._set_pressed_visual()
        self.press_timer = self.press_time

    def _set_pressed_visual(self) -> None:
        pressed_position = Vector3.new3(
            self.base_position.x,
            self.base_position.y - self.press_depth,
            self.base_position.z
        )

        self.position = pressed_position