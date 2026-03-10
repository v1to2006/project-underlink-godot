import math
from py4godot import gdclass
from py4godot.classes.CharacterBody3D import CharacterBody3D
from py4godot.classes.Input import Input
from py4godot.classes.InputEvent import InputEvent
from py4godot.classes.InputEventMouseMotion import InputEventMouseMotion
from py4godot.classes.Node3D import Node3D

@gdclass
class PlayerMotion(CharacterBody3D):
    speed: float = 3.0
    movement_smoothness: float = 10.0
    mouse_sensitivity: float = 0.0025
    gravity: float = 10.0

    def _ready(self) -> None:
        self.input: Input = Input.instance()
        self.head: Node3D = self.get_node("CameraPivot")
        self._pitch: float = 0.0
        self.input.set_mouse_mode(2)

    def _unhandled_input(self, event: InputEvent) -> None:
        self._handle_view(event)

    def _physics_process(self, delta: float) -> None:
        self._handle_motion(delta)
        self._apply_gravity(delta)
        self._handle_cursor()
        self.move_and_slide()

    def _handle_motion(self, delta: float) -> None:
        input_vector = self.input.get_vector(
            "move_left",
            "move_right",
            "move_back",
            "move_forward"
        )

        basis = self.global_transform.basis
        direction = (basis.x * input_vector.x) + (-basis.z * input_vector.y)

        if direction.length() > 0.0:
            direction = direction.normalized()

        target_velocity_x = direction.x * self.speed
        target_velocity_z = direction.z * self.speed

        current_velocity = self.velocity
        current_velocity.x = self._lerp(current_velocity.x, target_velocity_x, self.movement_smoothness * delta)
        current_velocity.z = self._lerp(current_velocity.z, target_velocity_z, self.movement_smoothness * delta)

        self.velocity = current_velocity

    def _handle_view(self, event: InputEvent) -> None:
        if not isinstance(event, InputEventMouseMotion):
            return

        self.rotate_y(-event.relative.x * self.mouse_sensitivity)

        self._pitch -= event.relative.y * self.mouse_sensitivity
        self._pitch = max(min(self._pitch, math.radians(90)), math.radians(-90))

        head_rotation = self.head.rotation
        head_rotation.x = self._pitch
        self.head.rotation = head_rotation

    def _handle_cursor(self) -> None:
        if self.input.is_action_just_pressed("ui_cancel"):
            self.input.set_mouse_mode(0)

    def _apply_gravity(self, delta: float) -> None:
        current_velocity = self.velocity
        current_velocity.y -= self.gravity * delta
        self.velocity = current_velocity

    def _lerp(self, a: float, b: float, t: float) -> float:
        if t < 0.0:
            t = 0.0
        if t > 1.0:
            t = 1.0
        return a + (b - a) * t