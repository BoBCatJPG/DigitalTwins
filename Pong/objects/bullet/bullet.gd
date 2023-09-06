extends Area2D

class_name Bullet



@export var speed = 100
# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func _physics_process(delta):
	global_position += speed * delta * transform.x


func _on_body_entered(body):
	if body is Barrel:
		var angl = self.global_position.angle_to_point(body.global_position)
		var impulse = Vector2( speed * cos(angl), speed * sin(angl))
		body.apply_central_impulse(impulse)
		body.emit_signal("hitted")
		queue_free()
	pass # Replace with function body.


func _on_visible_on_screen_notifier_2d_screen_exited():
	print("Fuori")
	queue_free()
	pass # Replace with function body.
