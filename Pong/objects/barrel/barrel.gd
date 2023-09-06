extends RigidBody2D
class_name Barrel

signal hitted

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func _on_hitted():
	if $TimerExplosion.is_stopped():
		$TimerExplosion.start()

func _on_timer_explosion_timeout():
	queue_free()
