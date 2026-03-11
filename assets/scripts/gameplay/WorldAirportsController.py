from py4godot import gdclass
from py4godot.classes.Node import Node


@gdclass
class WorldAirportsController(Node):
	def _ready(self) -> None:
		game_data_node = self.get_node("/root/GameData")
		self.game_data = game_data_node.get_pyscript()

		self.airport_point_nodes = [
			self.get_node("/root/Expedition/Airports/AirportPoint1"),
			self.get_node("/root/Expedition/Airports/AirportPoint2"),
			self.get_node("/root/Expedition/Airports/AirportPoint3"),
			self.get_node("/root/Expedition/Airports/AirportPoint4"),
			self.get_node("/root/Expedition/Airports/AirportPoint5"),
		]

		self.airport_points = [
			self.airport_point_nodes[0].get_pyscript(),
			self.airport_point_nodes[1].get_pyscript(),
			self.airport_point_nodes[2].get_pyscript(),
			self.airport_point_nodes[3].get_pyscript(),
			self.airport_point_nodes[4].get_pyscript(),
		]

		self.game_data.register_world_airports_controller(self)

	def assign_route(self, route: list[dict]) -> None:
		for airport_point in self.airport_points:
			airport_point.hide_completely()

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
			if index >= len(self.game_data.route):
				airport_point.hide_completely()
				continue

			airport_data = airport_point.airport_data
			icao_code = airport_data.get("icao_code", "")

			is_completed = icao_code in opened_airports
			is_active = (index == progress_index) and (not completed)
			is_locked = (index > progress_index) and (not completed)

			airport_point.set_visual_state(is_active, is_completed, is_locked)

	def get_active_airport_point_node(self):
		if self.game_data.completed:
			return None

		index = self.game_data.progress_index

		if index < 0:
			return None

		if index >= len(self.airport_point_nodes):
			return None

		return self.airport_point_nodes[index]

	def get_checkpoint_airport_point_node(self, opened_airports: list[str]):
		if len(opened_airports) == 0:
			return None

		last_opened_icao = opened_airports[-1]

		for index, airport_point in enumerate(self.airport_points):
			airport_data = airport_point.airport_data
			if airport_data.get("icao_code", "") == last_opened_icao:
				return self.airport_point_nodes[index]

		return None
