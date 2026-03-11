from py4godot import gdclass
from py4godot.classes.Camera3D import Camera3D
from py4godot.classes.RayCast3D import RayCast3D

@gdclass
class PlayerInteractor(Camera3D):
	def _ready(self) -> None:
		self.interact_ray: RayCast3D = self.get_node("InteractRay")
		self.held_button_script = None

	def _unhandled_input(self, event) -> None:
		if event.is_action_pressed("interact"):
			self._start_interaction()

		if event.is_action_released("interact"):
			self._stop_interaction()

	def _start_interaction(self) -> None:
		button_script = self._get_interactable_script_from_raycast()
		if button_script is None:
			return

		if hasattr(button_script, "begin_hold"):
			button_script.begin_hold()
			self.held_button_script = button_script
			return

		if hasattr(button_script, "interact"):
			button_script.interact()

	def _stop_interaction(self) -> None:
		if self.held_button_script is None:
			return

		if hasattr(self.held_button_script, "end_hold"):
			self.held_button_script.end_hold()

		self.held_button_script = None

	def _get_interactable_script_from_raycast(self):
		if self.interact_ray is None:
			print("PlayerInteractor: InteractRay not found")
			return None

		self.interact_ray.force_raycast_update()

		if not self.interact_ray.is_colliding():
			return None

		node = self.interact_ray.get_collider()
		if node is None:
			return None

		for i in range(5):
			script = node.get_pyscript()
			if script is not None:
				if hasattr(script, "begin_hold") or hasattr(script, "interact"):
					return script

			node = node.get_parent()
			if node is None:
				return None

		return None
