import math
from py4godot import gdclass
from py4godot.classes.Camera3D import Camera3D
from py4godot.classes.Node3D import Node3D

@gdclass
class MapCameraFollow(Camera3D):
	def _ready(self) -> None:
		self.anchor: Node3D = self.get_node("/root/Expedition/ProxyCube/MapAnchor")
		self.set_current(True)

	def _process(self, delta: float) -> None:
		target_transform = self.anchor.global_transform
		target_rotation = target_transform.basis.get_euler()

		target_rotation.x = math.radians(-90)
		target_rotation.y = 0
		target_rotation.z = 0

		target_transform.basis = target_transform.basis.from_euler(target_rotation)
		self.global_transform = target_transform