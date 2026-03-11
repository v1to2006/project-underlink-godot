from py4godot import gdclass
from py4godot.classes.Node3D import Node3D
from py4godot.classes.Area3D import Area3D


@gdclass
class AirportPoint(Node3D):
    def _ready(self) -> None:
        game_data_node = self.get_node("/root/GameData")
        self.game_data = game_data_node.get_pyscript()

        self.airport_data = {}
        self.slot_index = -1

        self.trigger_area: Area3D = self.get_node("TriggerArea")
        self.map_mark = self.get_node("MapMark")
        self.omni_light = self.get_node("OmniLight3D")

        self.trigger_area.area_entered.connect(self._on_area_entered)
        self.trigger_area.area_exited.connect(self._on_area_exited)

        self.hide_completely()

    def assign_airport(self, slot_index: int, airport_data: dict) -> None:
        self.slot_index = slot_index
        self.airport_data = airport_data

    def show_only_this_airport(self) -> None:
        if self.map_mark is not None:
            self.map_mark.visible = True

        if self.omni_light is not None:
            self.omni_light.visible = True

        if self.trigger_area is not None:
            self.trigger_area.monitoring = True
            self.trigger_area.monitorable = True

    def hide_completely(self) -> None:
        if self.map_mark is not None:
            self.map_mark.visible = False

        if self.omni_light is not None:
            self.omni_light.visible = False

        if self.trigger_area is not None:
            self.trigger_area.monitoring = False
            self.trigger_area.monitorable = False

    def set_visual_state(self, is_active: bool, is_completed: bool, is_locked: bool) -> None:
        if is_active:
            self.show_only_this_airport()
            return

        self.hide_completely()

    def _on_area_entered(self, area) -> None:
        if area is None:
            return

        if area.get_name() != "CrashArea":
            return

        self.game_data.on_airport_reached(self)

    def _on_area_exited(self, area) -> None:
        if area is None:
            return

        if area.get_name() != "CrashArea":
            return

        self.game_data.on_airport_left(self)