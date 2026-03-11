from py4godot.classes import gdclass
from py4godot.classes.Area2D import Area2D


@gdclass
class DangerZone(Area2D):

    def _ready(self) -> None:
        self.zone_type = "gas"   # change per zone in code or inspector if supported
        self.triggered = False

        self.body_entered.connect(self._on_body_entered)

    def _on_body_entered(self, body) -> None:
        if self.triggered:
            return

        # Optional: only react to player marker/drill
        if body.get_name() != "PlayerDrill":
            return

        self.triggered = True

        event_manager = self.get_node("/root/expedition/EventManager")
        event_manager.trigger_zone_event(self.zone_type, self)