import random

from py4godot.classes import gdclass
from py4godot.classes.Node import Node


@gdclass
class EventManager(Node):

    def _ready(self) -> None:
        popup_node = self.get_node("/root/Expedition/Control/EventPopup")
        if popup_node is None:
            print("EventManager: EventPopup node not found")
            self.popup = None
        else:
            self.popup = popup_node.get_pyscript()

        self.current_zone = None

        self.events = {
            "gas": [
                {
                    "text": "GAS POCKET DETECTED",
                    "choices": ["VENT PRESSURE", "BOOST DRILL", "STOP ENGINE"],
                    "correct": 0
                },
                {
                    "text": "TOXIC FUMES RISING",
                    "choices": ["SEAL CABIN", "SPEED UP", "POWER DOWN"],
                    "correct": 0
                }
            ],
            "collapse": [
                {
                    "text": "TUNNEL COLLAPSE STARTING",
                    "choices": ["REVERSE DRILL", "SPEED FORWARD", "WAIT"],
                    "correct": 1
                },
                {
                    "text": "ROCKFALL IMMINENT",
                    "choices": ["HOLD POSITION", "BOOST THROUGH", "SHUT SYSTEMS"],
                    "correct": 1
                }
            ],
            "signal": [
                {
                    "text": "SCANNER INTERFERENCE DETECTED",
                    "choices": ["REROUTE POWER", "BOOST SIGNAL", "IGNORE"],
                    "correct": 0
                },
                {
                    "text": "UNKNOWN SIGNAL SURGE",
                    "choices": ["SCAN AGAIN", "FOLLOW SIGNAL", "CUT POWER"],
                    "correct": 0
                }
            ]
        }

    def trigger_zone_event(self, zone_type, zone_node) -> None:
        self.current_zone = zone_node

        if zone_type not in self.events:
            print("Unknown zone type:", zone_type)
            return

        if self.popup is None:
            print("EventManager: popup is missing")
            return

        event_data = random.choice(self.events[zone_type])

        self.get_tree().paused = True
        self.popup.show_event(event_data, self)

    def resolve_event(self, selected_index: int, correct_index: int) -> None:
        self.get_tree().paused = False

        if selected_index == correct_index:
            print("SAFE PASSAGE")

            if self.current_zone is not None:
                self.current_zone.queue_free()
                self.current_zone = None
        else:
            print("DRILL LOST")
            self._handle_death()

    def _handle_death(self) -> None:
        self.get_tree().paused = False
        self.get_tree().change_scene_to_file("res://assets/scenes/MainMenu/PlayMenu.tscn")