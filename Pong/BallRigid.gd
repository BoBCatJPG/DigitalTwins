extends RigidBody2D


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


func _integrate_forces(state):
	var direction = Input.get_axis("left", "right")
	if direction:
		apply_central_impulse(Vector2(direction,0))

