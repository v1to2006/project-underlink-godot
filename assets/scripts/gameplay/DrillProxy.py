import math
from py4godot import gdclass
from py4godot.classes.Node3D import Node3D
from py4godot.classes.PhysicsRayQueryParameters3D import PhysicsRayQueryParameters3D
from py4godot.classes.core import Vector3

@gdclass
class DrillProxy(Node3D):
    move_speed: float = 4.0
    turn_speed_degrees: float = 60.0
    crash_height_margin: float = 0.2

    move_dir: int = 0
    turn_dir: int = 0
    dead: bool = False

    def press_button(self, action_name: str) -> None:
        if self.dead:
            return

        if action_name == "forward":
            self.move_dir = 0 if self.move_dir == 1 else 1

        elif action_name == "backward":
            self.move_dir = 0 if self.move_dir == -1 else -1

        elif action_name == "left":
            self.turn_dir = 0 if self.turn_dir == -1 else -1

        elif action_name == "right":
            self.turn_dir = 0 if self.turn_dir == 1 else 1

    def _physics_process(self, delta: float) -> None:
        if self.dead:
            return

        # rotate
        if self.turn_dir != 0:
            target_rotation = self.rotation
            target_rotation.y += math.radians(self.turn_speed_degrees) * self.turn_dir * delta
            self.rotation = target_rotation

        # move
        if self.move_dir != 0:
            forward = -self.global_transform.basis.z.normalized()
            move_offset = forward * self.move_speed * self.move_dir * delta
            next_pos = self.global_position + move_offset

            if self._hits_terrain(next_pos):
                self._die()
                return

            self.global_position = next_pos

    def _hits_terrain(self, world_pos) -> bool:
        space_state = self.get_world_3d().direct_space_state

        ray_from = world_pos + Vector3.new3(0, 100, 0)
        ray_to = world_pos + Vector3.new3(0, -100, 0)

        query = PhysicsRayQueryParameters3D.create(ray_from, ray_to)
        result = space_state.intersect_ray(query)

        if not result:
            return False

        if not result.has("position"):
            return False

        hit_pos = result["position"]
        terrain_height = hit_pos.y

        return world_pos.y <= terrain_height + self.crash_height_margin

    def _die(self) -> None:
        self.dead = True
        self.move_dir = 0
        self.turn_dir = 0
        print("GAME OVER: drill hit terrain")