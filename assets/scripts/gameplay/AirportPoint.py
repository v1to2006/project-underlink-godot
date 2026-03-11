from py4godot import gdclass
from py4godot.classes.Node3D import Node3D
from py4godot.classes.Area3D import Area3D
from py4godot.classes.Label3D import Label3D


@gdclass
class AirportPoint(Node3D):
    def _ready(self) -> None:
        self.airport_data: dict = {}
        self.slot_index: int = -1

        self.label_3d: Label3D = self.get_node("Label3D")
        self.trigger_area: Area3D = self.get_node("TriggerArea")

        self.trigger_area.connect("body_entered", self._on_body_entered)

        self.label_3d.text = "UNASSIGNED"

    def assign_airport(self, slot_index: int, airport_data: dict) -> None:
        self.slot_index = slot_index
        self.airport_data = airport_data

        airport_name = airport_data.get("name", "Unknown Airport")
        icao_code = airport_data.get("icao_code", "UNKNOWN")

        self.label_3d.text = f"{slot_index + 1}. {icao_code}\n{airport_name}"

    def set_visual_state(self, is_active: bool, is_completed: bool, is_locked: bool) -> None:
        if is_completed:
            self.label_3d.text = self.label_3d.text + "\n[COMPLETED]"
            return

        if is_active:
            self.label_3d.text = self.label_3d.text + "\n[ACTIVE]"
            return

        if is_locked:
            self.label_3d.text = self.label_3d.text + "\n[LOCKED]"

    def clear_state_suffix(self) -> None:
        if not self.airport_data:
            self.label_3d.text = "UNASSIGNED"
            return

        airport_name = self.airport_data.get("name", "Unknown Airport")
        icao_code = self.airport_data.get("icao_code", "UNKNOWN")
        self.label_3d.text = f"{self.slot_index + 1}. {icao_code}\n{airport_name}"

    def _on_body_entered(self, body) -> None:
        if body is None:
            return

        if not body.is_in_group("player"):
            return

        GameData.on_airport_reached(self)