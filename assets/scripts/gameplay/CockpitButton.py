from py4godot import gdclass
from py4godot.classes.Area3D import Area3D
from py4godot.classes.Node3D import Node3D

@gdclass
class CockpitButton(Area3D):
    action_name: str = ""
    drill_node_path: str = "/root/Expedition/ProxyCube"

    def interact(self) -> None:
        if self.drill_node_path == "":
            print("CockpitButton: drill_node_path is empty")
            return

        drill_node = self.get_node(self.drill_node_path)
        if drill_node is None:
            print("CockpitButton: drill node not found")
            return

        drill_script = drill_node.get_pyscript()
        if drill_script is None:
            print("CockpitButton: drill node has no python script")
            return

        if hasattr(drill_script, "press_button"):
            drill_script.press_button(self.action_name)