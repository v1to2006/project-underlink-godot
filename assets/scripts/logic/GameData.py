import json
import urllib.request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

from py4godot import gdclass
from py4godot.classes.Node import Node
from py4godot.classes.Input import Input


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
    backend_base_url: str = "http://127.0.0.1:5000"
    proxy_cube_node_path: str = "/root/Expedition/ProxyCube"
    ending_scene_path: str = "res://assets/scenes/MainMenu/Ending.tscn"

    def _ready(self) -> None:
        self.input = Input.instance()
        self.backend = BackendHttp(self.backend_base_url)
        self.clear_session()

        self.console = None
        self.world_airports_controller = None

    def clear_session(self) -> None:
        self.username = ""
        self.player_id = 0

        self.route = []
        self.opened_airports = []
        self.progress_index = 0
        self.completed = False

        self.current_airport_point = None
        self.current_airport_data = {}

    def is_logged_in(self) -> bool:
        return self.username != ""

    def has_active_save(self) -> bool:
        return len(self.route) > 0

    def login(self, username: str) -> bool:
        username = username.strip()

        if username == "":
            return False

        login_data = self.backend.post_json(
            "/login",
            {
                "username": username,
            },
        )

        if not login_data:
            return False

        self._apply_login_data(login_data)
        self._sync_runtime_state()
        return True

    def start_new_game(self) -> bool:
        if not self.is_logged_in():
            return False

        start_data = self.backend.post_json(
            "/start",
            {
                "username": self.username,
            },
        )

        if not start_data:
            return False

        self.route = list(start_data.get("route", []))
        self.progress_index = int(start_data.get("progress_index", 0))
        self.completed = bool(start_data.get("completed", False))
        self.opened_airports = []

        self.current_airport_point = None
        self.current_airport_data = {}

        self._sync_runtime_state()
        return True

    def logout(self) -> None:
        self.clear_session()

    def _apply_login_data(self, login_data: dict) -> None:
        self.player_id = int(login_data.get("player_id", 0))
        self.username = login_data.get("username", "")
        self.progress_index = int(login_data.get("progress_index", 0))
        self.completed = bool(login_data.get("completed", False))
        self.opened_airports = list(login_data.get("opened_airports", []))

        route_codes = list(login_data.get("route", []))
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

        self.current_airport_point = None
        self.current_airport_data = {}

    def register_console(self, console) -> None:
        self.console = console
        self.refresh_console_idle()

    def register_world_airports_controller(self, controller) -> None:
        self.world_airports_controller = controller
        self._refresh_world_airports()
        self._move_proxy_to_checkpoint()
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

    def get_checkpoint_airport_point_node(self):
        if self.world_airports_controller is None:
            return None

        return self.world_airports_controller.get_checkpoint_airport_point_node(
            self.opened_airports
        )

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

        previous_completed = self.completed

        self.progress_index = int(update_data.get("progress_index", self.progress_index))
        self.completed = bool(update_data.get("completed", False))
        self.opened_airports = list(update_data.get("opened_airports", self.opened_airports))

        self.current_airport_point = None
        self.current_airport_data = {}

        self._refresh_world_airports()
        self._move_proxy_to_checkpoint()

        if self.console is not None:
            self.console.show_airport_info(
                full_airport_data,
                self.progress_index,
                self.completed,
                self.get_next_airport(),
                self.get_next_airport_display_coordinates(),
            )

        if self.completed and not previous_completed:
            self._go_to_ending()

    def refresh_console_idle(self) -> None:
        if self.console is None:
            return

        self.console.show_idle_navigation(
            self.get_next_airport(),
            self.get_next_airport_display_coordinates(),
            self.completed,
        )

    def _sync_runtime_state(self) -> None:
        self._refresh_world_airports()
        self._move_proxy_to_checkpoint()
        self.refresh_console_idle()

    def _refresh_world_airports(self) -> None:
        if self.world_airports_controller is None:
            return

        self.world_airports_controller.assign_route(self.route)
        self.world_airports_controller.refresh_visual_states(
            self.progress_index,
            self.opened_airports,
            self.completed,
        )

    def _move_proxy_to_checkpoint(self) -> None:
        checkpoint_node = self.get_checkpoint_airport_point_node()
        if checkpoint_node is None:
            return

        proxy_cube = self.get_node(self.proxy_cube_node_path)
        if proxy_cube is None:
            return

        checkpoint_position = checkpoint_node.global_position
        current_position = proxy_cube.global_position

        current_position.x = checkpoint_position.x
        current_position.z = checkpoint_position.z
        proxy_cube.global_position = current_position

        proxy_script = proxy_cube.get_pyscript()
        if proxy_script is not None and hasattr(proxy_script, "reset_motion"):
            proxy_script.reset_motion()

    def _go_to_ending(self) -> None:
        self.input.set_mouse_mode(0)
        self.get_tree().change_scene_to_file(self.ending_scene_path)

    def _show_console_error(self, message: str) -> None:
        print(f"[GameData] {message}")

        if self.console is not None:
            self.console.show_error(message)