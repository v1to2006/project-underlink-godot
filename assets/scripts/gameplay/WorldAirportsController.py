from py4godot import gdclass
from py4godot.classes.Node import Node

@gdclass
class WorldAirportsController(Node):
    def _ready(self) -> None:
        self.airport_points = [
            self.get_node("/root/Expedition/Airports/AirportPoint1"),
            self.get_node("/root/Expedition/Airports/AirportPoint2"),
            self.get_node("/root/Expedition/Airports/AirportPoint3"),
            self.get_node("/root/Expedition/Airports/AirportPoint4"),
            self.get_node("/root/Expedition/Airports/AirportPoint5"),
        ]

        GameData.register_world_airports_controller(self)

    def assign_route(self, route: list[dict]) -> None:
        for index, airport_point in enumerate(self.airport_points):
            if index >= len(route):
                continue

            airport_point.assign_airport(index, route[index])

    def refresh_visual_states(
        self,
        progress_index: int,
        opened_airports: list[str],
        completed: bool,
    ) -> None:
        for index, airport_point in enumerate(self.airport_points):
            airport_point.clear_state_suffix()

            airport_data = airport_point.airport_data
            icao_code = airport_data.get("icao_code", "")

            is_completed = icao_code in opened_airports
            is_active = (index == progress_index) and (not completed)
            is_locked = (index > progress_index) and (not completed)

            airport_point.set_visual_state(is_active, is_completed, is_locked)