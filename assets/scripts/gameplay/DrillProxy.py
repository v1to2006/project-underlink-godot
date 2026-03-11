import math
from py4godot import gdclass
from py4godot.classes.CharacterBody3D import CharacterBody3D


@gdclass
class DrillProxy(CharacterBody3D):
    max_move_speed: float = 4.0
    move_acceleration: float = 3.5
    move_deceleration: float = 2.5

    max_turn_speed_degrees: float = 60.0
    turn_acceleration_degrees: float = 140.0
    turn_deceleration_degrees: float = 120.0

    crash_manager_node_path: str = "/root/Expedition/CrashManager"

    def _ready(self) -> None:
        self.dead: bool = False

        self.hold_forward: bool = False
        self.hold_backward: bool = False
        self.hold_left: bool = False
        self.hold_right: bool = False

        self.current_move_speed: float = 0.0
        self.current_turn_speed_degrees: float = 0.0

        crash_manager_node = self.get_node(self.crash_manager_node_path)
        self.crash_manager = crash_manager_node.get_pyscript()

    def start_button(self, action_name: str) -> None:
        if self.dead:
            return

        if action_name == "forward":
            self.hold_forward = True
        elif action_name == "backward":
            self.hold_backward = True
        elif action_name == "left":
            self.hold_left = True
        elif action_name == "right":
            self.hold_right = True

    def stop_button(self, action_name: str) -> None:
        if action_name == "forward":
            self.hold_forward = False
        elif action_name == "backward":
            self.hold_backward = False
        elif action_name == "left":
            self.hold_left = False
        elif action_name == "right":
            self.hold_right = False

    def _physics_process(self, delta: float) -> None:
        if self.dead:
            return

        self._update_rotation(delta)
        self._update_movement(delta)

    def _update_movement(self, delta: float) -> None:
        move_input = 0

        if self.hold_forward and not self.hold_backward:
            move_input = 1
        elif self.hold_backward and not self.hold_forward:
            move_input = -1

        target_speed = self.max_move_speed * move_input

        if move_input != 0:
            self.current_move_speed = self._move_toward(
                self.current_move_speed,
                target_speed,
                self.move_acceleration * delta,
            )
        else:
            self.current_move_speed = self._move_toward(
                self.current_move_speed,
                0.0,
                self.move_deceleration * delta,
            )

        if self.current_move_speed == 0.0:
            self.velocity = self.velocity * 0.0
            return

        forward = -self.global_transform.basis.z.normalized()
        self.velocity = forward * self.current_move_speed

        collision = self.move_and_collide(self.velocity * delta)

        if collision is not None:
            self._die()

    def _update_rotation(self, delta: float) -> None:
        turn_input = 0

        if self.hold_right and not self.hold_left:
            turn_input = -1
        elif self.hold_left and not self.hold_right:
            turn_input = 1

        target_turn_speed = self.max_turn_speed_degrees * turn_input

        if turn_input != 0:
            self.current_turn_speed_degrees = self._move_toward(
                self.current_turn_speed_degrees,
                target_turn_speed,
                self.turn_acceleration_degrees * delta,
            )
        else:
            self.current_turn_speed_degrees = self._move_toward(
                self.current_turn_speed_degrees,
                0.0,
                self.turn_deceleration_degrees * delta,
            )

        if self.current_turn_speed_degrees != 0.0:
            target_rotation = self.rotation
            target_rotation.y += math.radians(self.current_turn_speed_degrees) * delta
            self.rotation = target_rotation

    def _die(self) -> None:
        if self.dead:
            return

        self.dead = True
        self.reset_motion()

        if self.crash_manager is not None:
            self.crash_manager.start_crash_sequence()

    def _move_toward(self, current: float, target: float, step: float) -> float:
        if current < target:
            current += step
            if current > target:
                current = target
        elif current > target:
            current -= step
            if current < target:
                current = target

        return current

    def reset_motion(self) -> None:
        self.hold_forward = False
        self.hold_backward = False
        self.hold_left = False
        self.hold_right = False

        self.current_move_speed = 0.0
        self.current_turn_speed_degrees = 0.0
        self.velocity = self.velocity * 0.0