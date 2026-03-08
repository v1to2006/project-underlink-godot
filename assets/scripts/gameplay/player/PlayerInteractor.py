from py4godot import gdclass
from py4godot.classes.Camera3D import Camera3D
from py4godot.classes.PhysicsRayQueryParameters3D import PhysicsRayQueryParameters3D

@gdclass
class PlayerInteractor(Camera3D):
    interact_distance: float = 3.0

    def _unhandled_input(self, event) -> None:
        if event.is_action_pressed("interact"):
            self.try_interact()

    def try_interact(self) -> None:
        from_pos = self.global_position
        forward = -self.global_transform.basis.z.normalized()
        to_pos = from_pos + forward * self.interact_distance

        space_state = self.get_world_3d().direct_space_state
        query = PhysicsRayQueryParameters3D.create(from_pos, to_pos)
        result = space_state.intersect_ray(query)

        if not result:
            return

        if not result.has("collider"):
            return

        collider = result["collider"]
        if collider is None:
            return

        collider_script = collider.get_pyscript()
        if collider_script is not None:
            if hasattr(collider_script, "interact"):
                collider_script.interact()
                return

        parent = collider.get_parent()
        if parent is None:
            return

        parent_script = parent.get_pyscript()
        if parent_script is not None:
            if hasattr(parent_script, "interact"):
                parent_script.interact()
                return