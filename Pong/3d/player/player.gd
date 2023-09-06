extends CharacterBody3D


@export var potenzaMotore = 500.0
@export var rotationSpeed = 5
@export var friction = -50

var rot_dir = 0
var acceleration = Vector3.ZERO
var veloLocal = Vector3.ZERO


# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")


func checkInput():
	rot_dir = Input.get_axis("left", "right")
	acceleration = Vector3.ZERO
	if Input.is_action_pressed("forward"):
		acceleration = Vector3(potenzaMotore , 0 , 0)
		
func applyFriction(delta):
	if acceleration == Vector3.ZERO and veloLocal.length() < 5:
		veloLocal = Vector3.ZERO
	var fritcionForce = veloLocal * friction * delta
	acceleration += fritcionForce

func rotatePlayer(delta):
	self.rotation -= Vector3(0, delta * rot_dir * rotationSpeed, 0)
	
func _physics_process(delta):
	# Add the gravity.
	if not is_on_floor():
		velocity.y -= gravity * delta
		
	checkInput()
	applyFriction(delta)
	rotatePlayer(delta)
	veloLocal += acceleration * delta
	velocity = veloLocal.rotated(Vector3(0,1,0), self.rotation.y)

	move_and_slide()


func _on_networking_data_received(vel, steer, acc):
	rot_dir = (steer/30) * -1
	veloLocal.x = vel
