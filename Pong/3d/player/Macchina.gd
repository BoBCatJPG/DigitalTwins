extends VehicleBody3D




# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


func _physics_process(delta):
	#steering = Input.get_axis("right", "left") * 0.4
	#engine_force = Input.get_axis("break", "forward") * 150
	pass




func _on_networking_data_received(vel, steer, acc):
	steering = steer * 0.4
	engine_force = vel* 150
	pass # Replace with function body.
