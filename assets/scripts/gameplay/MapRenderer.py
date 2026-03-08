from py4godot import gdclass
from py4godot.classes.core import Vector3
from py4godot.classes.MeshInstance3D import MeshInstance3D
from py4godot.classes.SubViewport import SubViewport
from py4godot.classes.Camera3D import Camera3D
from py4godot.classes.StandardMaterial3D import StandardMaterial3D

@gdclass
class MapRenderer(MeshInstance3D):
	def _ready(self) -> None:
		viewport: SubViewport = self.get_node("/root/Expedition/ProxyCube/MapAnchor/SubViewport")
		camera: Camera3D = self.get_node("/root/Expedition/ProxyCube/MapAnchor/SubViewport/Camera3D")

		camera.set_current(True)
		viewport.set_update_mode(3)

		material: StandardMaterial3D = StandardMaterial3D.new()
		material.albedo_texture = viewport.get_texture()
		material.shading_mode = 0
		material.texture_repeat = False

		material.uv1_scale = Vector3.new3(1, 1, 1)
		material.uv1_offset = Vector3.new3(0, 0, 0)

		self.material_override = material