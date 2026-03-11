from py4godot import gdclass
from py4godot.classes.Area3D import Area3D


@gdclass
class DangerZone(Area3D):

    def _ready(self) -> None:
        self.zone_type = "gas"
        self.triggered = False

        self.body_entered.connect(self._on_body_entered)

    def _on_body_entered(self, body) -> None:
        if self.triggered:
            return

        if body is None:
            return

        self.triggered = True

        event_manager_node = self.get_node("/root/Expedition/EventManager")
        if event_manager_node is None:
            print("DangerZone: EventManager not found")
            return

        event_manager = event_manager_node.get_pyscript()
        if event_manager is None:
            print("DangerZone: EventManager script not found")
            return

        event_manager.trigger_zone_event(self.zone_type, self)