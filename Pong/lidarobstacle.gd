extends CharacterBody3D

var id_angle = 0
var distance = 0

func _process(delta):
	return
	if visible:
		if distance > 0.3 and distance < 0.5:
			print("Sono il cazzillo dell'angolo ", id_angle, " distanza ", distance)

func deactive():
	visible = false
	$CollisionShape3D.disabled = true

func active():
	visible = true
	$CollisionShape3D.disabled = false
