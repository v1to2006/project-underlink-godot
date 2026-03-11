from urllib.parse import urlencode

from py4godot import gdclass
from py4godot.classes.Node import Node

from BackendHttp import BackendHttp


@gdclass
class GameData(Node):
    username: str = "v1to"
    backend_base_url: str = "http://127.0.0.1:5000"

    def _ready(self) -> None:
        self.backend = BackendHttp(self.backend_base_url)

        self.route: list[dict] = []
        self.opened_airports: list[str] = []
        self.progress_index: int = 0
        self.completed: bool = False

        self.current_airport_point = None
        self.current_airport_data: dict = {}

        self.console = None
        self.world_airports_controller = None

        self.login_or_start_game()

    def register_console(self, console) -> None:
        self.console = console

    def register_world_airports_controller(self, controller) -> None:
        self.world_airports_controller = controller
        self._refresh_world_airports()

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

    def get_airport_info(self, icao_code: str) -> dict:
        query = urlencode({"icao_code": icao_code})
        return self.backend.get_json(f"/airport?{query}")

    def get_next_airport(self) -> dict:
        if self.progress_index >= len(self.route):
            return {}
        return self.route[self.progress_index]

    def is_airport_next(self, icao_code: str) -> bool:
        next_airport = self.get_next_airport()

        if not next_airport:
            return False

        return next_airport.get("icao_code", "") == icao_code

    def on_airport_reached(self, airport_point) -> None:
        if self.completed:
            self._show_console_error("Expedition already completed.")
            return

        airport_data = airport_point.airport_data
        icao_code = airport_data.get("icao_code", "")

        if icao_code == "":
            self._show_console_error("Airport has no ICAO code.")
            return

        if not self.is_airport_next(icao_code):
            next_airport = self.get_next_airport()
            next_code = next_airport.get("icao_code", "UNKNOWN")
            self._show_console_error(f"Wrong airport. Next airport is {next_code}.")
            return

        self.current_airport_point = airport_point
        self.current_airport_data = airport_data

        if self.console is not None:
            self.console.show_airport_found(airport_data)

    def establish_connection(self) -> None:
        if self.current_airport_point is None:
            self._show_console_error("No airport selected.")
            return

        icao_code = self.current_airport_data.get("icao_code", "")

        if icao_code == "":
            self._show_console_error("Invalid airport ICAO.")
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

        self._refresh_world_airports()

        if self.console is not None:
            self.console.show_airport_info(
                full_airport_data,
                self.progress_index,
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