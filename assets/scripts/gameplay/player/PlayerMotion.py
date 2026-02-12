import math
from py4godot import gdclass
from py4godot.classes.CharacterBody3D import CharacterBody3D
from py4godot.classes.Input import Input
from py4godot.classes.InputEvent import InputEvent
from py4godot.classes.InputEventMouseMotion import InputEventMouseMotion
from py4godot.classes.Node3D import Node3D

@gdclass
class PlayerMotion(CharacterBody3D):
	speed: float = 10
	mouse_sensitivity: float = 0.0025
	gravity: float = 10

	def _ready(self) -> None:
		self.input: Input = Input.instance()
		self.head: Node3D = self.get_node("CameraPivot")
		self._pitch: float = 0
		self.input.set_mouse_mode(2)
	
	def _unhandled_input(self, event: InputEvent) -> None:
		self._handle_view(event)
	
	def _physics_process(self, delta: float) -> None:
		self._handle_motion()
		self._apply_gravity(delta)
		self._handle_cursor()
	
	def _handle_motion(self):
		input_vector = self.input.get_vector("move_left", "move_right", "move_back", "move_forward")
		global_transform = self.global_transform.basis

		direction = (global_transform.x * input_vector.x) + (-global_transform.z * input_vector.y)

		if direction.length() > 0.0:
			direction = direction.normalized()
		
		new_velocity = self.velocity
		new_velocity.x = direction.x * self.speed
		new_velocity.z = direction.z * self.speed
		self.velocity = new_velocity

		self.move_and_slide()

	def _handle_view(self, event: InputEvent):
		if not isinstance(event, InputEventMouseMotion):
			return

		self.rotate_y(-event.relative.x * self.mouse_sensitivity)

		self._pitch -= event.relative.y * self.mouse_sensitivity
		self._pitch = max(min(self._pitch, math.radians(90)), math.radians(-90))

		target_rotation = self.head.rotation
		target_rotation.x = self._pitch
		self.head.rotation = target_rotation
	
	def _handle_cursor(self):
		if self.input.is_action_just_pressed("ui_cancel"):
			self.input.set_mouse_mode(0)
	
	def _apply_gravity(self, delta: float):
		target_velocity = self.velocity
		target_velocity.y -= self.gravity * delta

		self.velocity = target_velocity