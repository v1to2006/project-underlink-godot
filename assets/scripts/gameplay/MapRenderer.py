from py4godot import gdclass
from py4godot.classes.MeshInstance3D import MeshInstance3D
from py4godot.classes.SubViewport import SubViewport
from py4godot.classes.Camera3D import Camera3D
from py4godot.classes.StandardMaterial3D import StandardMaterial3D

@gdclass
class MapRenderer(MeshInstance3D):

	def _ready(self) -> None:
		viewport: SubViewport = self.get_node("/root/Expedition/ProxyCube/SubViewport")
		camera: Camera3D = self.get_node("/root/Expedition/ProxyCube/SubViewport/Camera3D")

		camera.set_current(True)

		material: StandardMaterial3D = StandardMaterial3D.new()
		material.albedo_texture = viewport.get_texture()

		self.material_override = material
