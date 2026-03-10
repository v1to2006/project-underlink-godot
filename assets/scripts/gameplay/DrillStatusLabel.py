import math
from py4godot import gdclass
from py4godot.classes.Label3D import Label3D
from py4godot.classes.Node3D import Node3D

@gdclass
class DrillStatusLabel(Label3D):
    drill_node_path: str = "/root/Expedition/ProxyCube"
    value_type: str = "x"   # "x", "z", "rotation"
    prefix: str = "X"
    decimals: int = 0

    def _ready(self) -> None:
        self.drill_node: Node3D = self.get_node(self.drill_node_path)
        self._update_text()

    def _process(self, delta: float) -> None:
        self._update_text()

    def _update_text(self) -> None:
        if self.drill_node is None:
            self.text = f"{prefix}: ---"
            return

        if self.value_type == "x":
            value = self.drill_node.global_position.x
        elif self.value_type == "z":
            value = self.drill_node.global_position.z
        elif self.value_type == "rotation":
            value = math.degrees(self.drill_node.rotation.y)
            value = self._normalize_angle(value)
        else:
            self.text = self.prefix + ": ???"
            return

        self.text = self.prefix + ": " + self._format_value(value)

    def _format_value(self, value: float) -> str:
        rounded_value = round(value, self.decimals)

        if self.decimals <= 0:
            return str(int(rounded_value))

        return str(rounded_value)

    def _normalize_angle(self, angle: float) -> float:
        while angle < 0.0:
            angle += 360.0

        while angle >= 360.0:
            angle -= 360.0

        return angle