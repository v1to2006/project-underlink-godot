import json
import urllib.request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

from py4godot import gdclass
from py4godot.classes.Node import Node


class BackendHttp:
	def __init__(self, base_url: str) -> None:
		self.base_url = base_url.rstrip("/")

	def get_json(self, path: str) -> dict:
		try:
			url = f"{self.base_url}{path}"

			with urllib.request.urlopen(url, timeout=5) as response:
				response_text = response.read().decode("utf-8")
				return json.loads(response_text)

		except HTTPError as error:
			print(f"[BackendHttp] HTTPError GET {path}: {error}")
		except URLError as error:
			print(f"[BackendHttp] URLError GET {path}: {error}")
		except Exception as error:
			print(f"[BackendHttp] Exception GET {path}: {error}")

		return {}

	def post_json(self, path: str, payload: dict) -> dict:
		try:
			url = f"{self.base_url}{path}"
			body = json.dumps(payload).encode("utf-8")

			request = urllib.request.Request(
				url,
				data=body,
				headers={"Content-Type": "application/json"},
				method="POST",
			)

			with urllib.request.urlopen(request, timeout=5) as response:
				response_text = response.read().decode("utf-8")
				return json.loads(response_text)

		except HTTPError as error:
			print(f"[BackendHttp] HTTPError POST {path}: {error}")
		except URLError as error:
			print(f"[BackendHttp] URLError POST {path}: {error}")
		except Exception as error:
			print(f"[BackendHttp] Exception POST {path}: {error}")

		return {}


@gdclass
class GameData(Node):
	username: str = "v1toasdasd"
	backend_base_url: str = "http://127.0.0.1:5000"

	def _ready(self) -> None:
		self.backend = BackendHttp(self.backend_base_url)

		self.route = []
		self.opened_airports = []
		self.progress_index = 0
		self.completed = False

		self.current_airport_point = None
		self.current_airport_data = {}

		self.console = None
		self.world_airports_controller = None

		self.login_or_start_game()

	def register_console(self, console) -> None:
		self.console = console
		self.refresh_console_idle()

	def register_world_airports_controller(self, controller) -> None:
		self.world_airports_controller = controller
		self._refresh_world_airports()
		self.refresh_console_idle()

	def login_or_start_game(self) -> None:
		login_data = self.backend.post_json(
			"/login",
			{
				"username": self.username,
			},
		)

		if not login_data:
			self._show_console_error("Login failed.")
			return

		self.progress_index = int(login_data.get("progress_index", 0))
		self.completed = bool(login_data.get("completed", False))
		self.opened_airports = list(login_data.get("opened_airports", []))

		route_codes = list(login_data.get("route", []))

		if len(route_codes) == 0:
			start_data = self.backend.post_json(
				"/start",
				{
					"username": self.username,
				},
			)

			if not start_data:
				self._show_console_error("Start failed.")
				return

			self.route = list(start_data.get("route", []))
			self.progress_index = int(start_data.get("progress_index", 0))
			self.completed = bool(start_data.get("completed", False))
			self.opened_airports = []

			self._refresh_world_airports()
			self.refresh_console_idle()
			return

		self.route = []

		for order_index, icao_code in enumerate(route_codes, start=1):
			airport_info = self.get_airport_info(icao_code)

			if airport_info:
				self.route.append(
					{
						"order_index": order_index,
						"icao_code": airport_info.get("icao_code", icao_code),
						"name": airport_info.get("name", icao_code),
						"country_code": airport_info.get("country_code", ""),
					}
				)
			else:
				self.route.append(
					{
						"order_index": order_index,
						"icao_code": icao_code,
						"name": icao_code,
						"country_code": "",
					}
				)

		self._refresh_world_airports()
		self.refresh_console_idle()

	def get_airport_info(self, icao_code: str) -> dict:
		query = urlencode({"icao_code": icao_code})
		return self.backend.get_json(f"/airport?{query}")

	def get_next_airport(self) -> dict:
		if self.progress_index >= len(self.route):
			return {}

		return self.route[self.progress_index]

	def get_next_airport_point_node(self):
		if self.world_airports_controller is None:
			return None

		return self.world_airports_controller.get_active_airport_point_node()

	def get_next_airport_display_coordinates(self) -> dict:
		airport_point_node = self.get_next_airport_point_node()

		if airport_point_node is None:
			return {}

		position = airport_point_node.global_position

		return {
			"x": round(position.x, 1),
			"y": round(position.z, 1),
		}

	def is_airport_next(self, icao_code: str) -> bool:
		next_airport = self.get_next_airport()

		if not next_airport:
			return False

		return next_airport.get("icao_code", "") == icao_code

	def on_airport_reached(self, airport_point) -> None:
		if self.completed:
			return

		airport_data = airport_point.airport_data
		icao_code = airport_data.get("icao_code", "")

		if icao_code == "":
			return

		if not self.is_airport_next(icao_code):
			return

		self.current_airport_point = airport_point
		self.current_airport_data = airport_data

		if self.console is not None:
			self.console.show_airport_found(airport_data)

	def on_airport_left(self, airport_point) -> None:
		if self.current_airport_point != airport_point:
			return

		self.current_airport_point = None
		self.current_airport_data = {}
		self.refresh_console_idle()

	def establish_connection(self) -> None:
		if self.current_airport_point is None:
			return

		icao_code = self.current_airport_data.get("icao_code", "")

		if icao_code == "":
			return

		full_airport_data = self.get_airport_info(icao_code)

		if not full_airport_data:
			self._show_console_error("Failed to load airport info.")
			return

		update_data = self.backend.post_json(
			"/update",
			{
				"username": self.username,
				"icao_code": icao_code,
			},
		)

		if not update_data:
			self._show_console_error("Failed to update progress.")
			return

		self.progress_index = int(update_data.get("progress_index", self.progress_index))
		self.completed = bool(update_data.get("completed", False))
		self.opened_airports = list(update_data.get("opened_airports", self.opened_airports))

		self.current_airport_point = None
		self.current_airport_data = {}

		self._refresh_world_airports()

		if self.console is not None:
			self.console.show_airport_info(
				full_airport_data,
				self.progress_index,
				self.completed,
				self.get_next_airport(),
				self.get_next_airport_display_coordinates(),
			)

	def refresh_console_idle(self) -> None:
		if self.console is None:
			return

		self.console.show_idle_navigation(
			self.get_next_airport(),
			self.get_next_airport_display_coordinates(),
			self.completed,
		)

	def _refresh_world_airports(self) -> None:
		if self.world_airports_controller is None:
			return

		self.world_airports_controller.assign_route(self.route)
		self.world_airports_controller.refresh_visual_states(
			self.progress_index,
			self.opened_airports,
			self.completed,
		)

	def _show_console_error(self, message: str) -> None:
		print(f"[GameData] {message}")

		if self.console is not None:
			self.console.show_error(message)
