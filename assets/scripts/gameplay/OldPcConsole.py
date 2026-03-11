from py4godot import gdclass
from py4godot.classes.Node3D import Node3D
from py4godot.classes.Label3D import Label3D


@gdclass
class OldPcConsole(Node3D):
    def _ready(self) -> None:
        self.title_label: Label3D = self.get_node("TitleLabel3D")
        self.status_label: Label3D = self.get_node("StatusLabel3D")
        self.info_label: Label3D = self.get_node("InfoLabel3D")
        self.action_label: Label3D = self.get_node("ActionLabel3D")

        GameData.register_console(self)

        self._set_idle_text()

    def interact(self) -> None:
        GameData.establish_connection()

    def show_airport_found(self, airport_data: dict) -> None:
        airport_name = airport_data.get("name", "Unknown Airport")
        icao_code = airport_data.get("icao_code", "UNKNOWN")

        self.title_label.text = "AIRPORT FOUND"
        self.status_label.text = f"{airport_name}"
        self.info_label.text = f"ICAO: {icao_code}"
        self.action_label.text = "Press E to establish connection"

    def show_airport_info(self, airport_info: dict, progress_index: int, completed: bool) -> None:
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

        self.title_label.text = "CONNECTION ESTABLISHED"
        self.status_label.text = f"{airport_name} ({icao_code})"

        self.info_label.text = (
            f"Type: {airport_type}\n"
            f"Country: {country_name} ({country_code})\n"
            f"Municipality: {municipality}\n"
            f"Scheduled: {scheduled_service}\n"
            f"Elevation: {elevation_ft}\n"
            f"Lat: {latitude_deg}\n"
            f"Lon: {longitude_deg}\n"
            f"Progress: {progress_index}/5\n"
            f"Survivors found: {survivors_text}"
        )

        self.action_label.text = "Await further expedition orders"

    def show_error(self, message: str) -> None:
        self.title_label.text = "ERROR"
        self.status_label.text = message
        self.info_label.text = ""
        self.action_label.text = ""

    def _set_idle_text(self) -> None:
        self.title_label.text = "DEEP DRIFT TERMINAL"
        self.status_label.text = "Awaiting airport contact"
        self.info_label.text = ""
        self.action_label.text = ""