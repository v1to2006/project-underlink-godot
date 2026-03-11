from py4godot import gdclass
from py4godot.classes.Node3D import Node3D
from py4godot.classes.Label3D import Label3D


@gdclass
class OldPcConsole(Node3D):
    def _ready(self) -> None:
        game_data_node = self.get_node("/root/GameData")
        self.game_data = game_data_node.get_pyscript()

        self.title_label: Label3D = self.get_node("TitleLabel3D")
        self.status_label: Label3D = self.get_node("StatusLabel3D")
        self.info_label: Label3D = self.get_node("InfoLabel3D")
        self.action_label: Label3D = self.get_node("ActionLabel3D")
        self.hint_label: Label3D = self.get_node("HintLabel3D")

        self.type_speed = 60.0
        self.type_timer = 0.0
        self.type_index = 0
        self.is_typing = False
        self.full_info_text = ""

        self.scan_frames = [
            "SCANNING.",
            "SCANNING..",
            "SCANNING...",
            "CALIBRATING.",
            "CALIBRATING..",
            "LOCKING TARGET...",
        ]
        self.scan_frame_index = 0
        self.scan_frame_timer = 0.0
        self.scan_frame_duration = 0.35
        self.scan_total_timer = 0.0
        self.scan_total_duration = 2.4
        self.is_scanning = False
        self.pending_next_airport = {}
        self.pending_next_coords = {}

        self.console_state = "idle"

        self.game_data.register_console(self)

        self._clear_all_labels()
        self._set_idle_text()

    def _process(self, delta: float) -> None:
        self._process_typing(delta)
        self._process_scanning(delta)

    def interact(self) -> None:
        if self.console_state == "airport_found":
            self.action_label.text = ""
            self.hint_label.text = "Connecting..."
            self.game_data.establish_connection()
            return

        if self.console_state == "scan_ready":
            self._start_scan_sequence()
            return

    def show_idle_navigation(self, next_airport: dict, coords: dict, completed: bool) -> None:
        if self.console_state == "airport_found":
            return

        if self.is_scanning:
            return

        if self.is_typing:
            return

        self.console_state = "idle"

        if completed:
            self.title_label.text = "TERMINAL"
            self.status_label.text = "Expedition complete"
            self.info_label.text = "No further airport targets."
            self.action_label.text = ""
            self.hint_label.text = ""
            return

        airport_name = next_airport.get("name", "Unknown Airport")
        icao_code = next_airport.get("icao_code", "UNKNOWN")
        display_x = coords.get("x", "---")
        display_y = coords.get("y", "---")

        self.title_label.text = "TERMINAL"
        self.status_label.text = f"Next airport: {airport_name}"
        self.info_label.text = (
            f"ICAO: {icao_code}\n"
            f"X: {display_x}\n"
            f"Y: {display_y}"
        )
        self.action_label.text = ""
        self.hint_label.text = "Navigate to target airport"

    def show_airport_found(self, airport_data: dict) -> None:
        airport_name = airport_data.get("name", "Unknown Airport")
        icao_code = airport_data.get("icao_code", "UNKNOWN")
        country_code = airport_data.get("country_code", "")

        self._stop_typing()
        self._stop_scanning()

        self.console_state = "airport_found"

        self.title_label.text = "AIRPORT DETECTED"
        self.status_label.text = airport_name
        self.info_label.text = (
            f"ICAO: {icao_code}\n"
            f"Country: {country_code}\n"
            f"Status: Awaiting terminal link"
        )
        self.action_label.text = "Press E to establish connection"
        self.hint_label.text = "Terminal link available"

    def show_airport_info(
        self,
        airport_info: dict,
        progress_index: int,
        completed: bool,
        next_airport: dict,
        next_coords: dict,
    ) -> None:
        airport_name = airport_info.get("name", "Unknown Airport")
        icao_code = airport_info.get("icao_code", "UNKNOWN")
        airport_type = airport_info.get("type", "")
        country_code = airport_info.get("country_code", "")
        country_name = airport_info.get("country_name", "")
        municipality = airport_info.get("municipality", "")
        scheduled_service = airport_info.get("scheduled_service", "")
        elevation_ft = airport_info.get("elevation_ft", "")
        latitude_deg = airport_info.get("latitude_deg", "")
        longitude_deg = airport_info.get("longitude_deg", "")

        survivors_text = "437" if completed else "0"

        self._stop_typing()
        self._stop_scanning()

        self.pending_next_airport = next_airport
        self.pending_next_coords = next_coords

        self.console_state = "report"

        self.title_label.text = "CONNECTION ESTABLISHED"
        self.status_label.text = f"{airport_name} ({icao_code})"

        pretty_text = (
            f"Type: {airport_type}\n"
            f"Country: {country_name} ({country_code})\n"
            f"Municipality: {municipality}\n"
            f"Scheduled Service: {scheduled_service}\n"
            f"Elevation: {elevation_ft} ft\n"
            f"Latitude: {latitude_deg}\n"
            f"Longitude: {longitude_deg}\n"
            f"\n"
            f"Progress: {progress_index}/5\n"
            f"Survivors found: {survivors_text}"
        )

        self._start_typing(pretty_text)

        self.action_label.text = ""
        self.hint_label.text = "Connection complete"

    def show_error(self, message: str) -> None:
        self._stop_typing()
        self._stop_scanning()

        self.console_state = "error"

        self.title_label.text = "ERROR"
        self.status_label.text = message
        self.info_label.text = ""
        self.action_label.text = ""
        self.hint_label.text = ""

    def _process_typing(self, delta: float) -> None:
        if not self.is_typing:
            return

        self.type_timer += delta * self.type_speed

        target_index = int(self.type_timer)
        if target_index > len(self.full_info_text):
            target_index = len(self.full_info_text)

        if target_index != self.type_index:
            self.type_index = target_index
            self.info_label.text = self.full_info_text[:self.type_index]

        if self.type_index >= len(self.full_info_text):
            self.is_typing = False

            if self.console_state == "report":
                if self.pending_next_airport:
                    self.console_state = "scan_ready"
                    self.action_label.text = "Press E to scan for nearby airport"
                    self.hint_label.text = "Route update available"
                else:
                    self.console_state = "idle"
                    self.action_label.text = ""
                    self.hint_label.text = "Expedition complete"

    def _process_scanning(self, delta: float) -> None:
        if not self.is_scanning:
            return

        self.scan_total_timer += delta
        self.scan_frame_timer += delta

        if self.scan_frame_timer >= self.scan_frame_duration:
            self.scan_frame_timer = 0.0
            self.scan_frame_index += 1

            if self.scan_frame_index >= len(self.scan_frames):
                self.scan_frame_index = 0

            self.info_label.text = self.scan_frames[self.scan_frame_index]

        if self.scan_total_timer >= self.scan_total_duration:
            self._finish_scan_sequence()

    def _start_scan_sequence(self) -> None:
        if not self.pending_next_airport:
            return

        self._stop_typing()

        self.console_state = "scan_anim"
        self.is_scanning = True
        self.scan_frame_index = 0
        self.scan_frame_timer = 0.0
        self.scan_total_timer = 0.0

        self.title_label.text = "AIRPORT SCAN"
        self.status_label.text = "Searching nearby airport..."
        self.info_label.text = self.scan_frames[0]
        self.action_label.text = ""
        self.hint_label.text = "Please wait"

    def _finish_scan_sequence(self) -> None:
        self._stop_scanning()

        next_airport = self.pending_next_airport
        next_coords = self.pending_next_coords

        airport_name = next_airport.get("name", "Unknown Airport")
        icao_code = next_airport.get("icao_code", "UNKNOWN")
        display_x = next_coords.get("x", "---")
        display_y = next_coords.get("y", "---")

        self.console_state = "idle"
        self.pending_next_airport = {}
        self.pending_next_coords = {}

        self.title_label.text = "SCAN COMPLETE"
        self.status_label.text = f"Next airport: {airport_name}"
        self.info_label.text = (
            f"ICAO: {icao_code}\n"
            f"X: {display_x}\n"
            f"Y: {display_y}"
        )
        self.action_label.text = ""
        self.hint_label.text = "Navigate to new target"

    def _start_typing(self, text: str) -> None:
        self.full_info_text = text
        self.type_timer = 0.0
        self.type_index = 0
        self.is_typing = True
        self.info_label.text = ""

    def _stop_typing(self) -> None:
        self.is_typing = False
        self.type_timer = 0.0
        self.type_index = 0
        self.full_info_text = ""

    def _stop_scanning(self) -> None:
        self.is_scanning = False
        self.scan_frame_index = 0
        self.scan_frame_timer = 0.0
        self.scan_total_timer = 0.0

    def _clear_all_labels(self) -> None:
        self.title_label.text = ""
        self.status_label.text = ""
        self.info_label.text = ""
        self.action_label.text = ""
        self.hint_label.text = ""

    def _set_idle_text(self) -> None:
        self.show_idle_navigation({}, {}, False)