extends CharacterBody2D
class_name Player

@export var potenzaMotore = 500
@export var rotationSpeed = 3
@export var friction = -50
@export var timeShoot : float = 2.0

@export var BulletScene : PackedScene

@onready var cannone = $Cannone
@onready var cannonBarrel = $Cannone/Marker2D

@onready var timerShoot = $FireTimer


var rot_dir = 0
var acceleration = Vector2.ZERO
var veloLocal = Vector2.ZERO

var timerProg = null

func _ready():
	timerProg = Timer.new()
	timerProg.one_shot = true
	add_child(timerProg)

func checkInput():
	cannone.look_at(get_global_mouse_position())
	cannone.rotation_degrees -= 90
	rot_dir = Input.get_axis("left", "right")
	acceleration = Vector2.ZERO
	if Input.is_action_pressed("forward"):
		acceleration = Vector2(potenzaMotore , 0 )
	if Input.is_action_pressed("fire"):
		fire()

func fire():
	if timerProg.is_stopped():
		for i in range(0,1000):
			var auxBullet = BulletScene.instantiate()
			add_sibling(auxBullet) # owner.add_child
			auxBullet.global_transform = cannonBarrel.global_transform
			auxBullet.global_rotation_degrees = cannone.global_rotation_degrees + 90 * (i*.3)
			timerProg.start(timeShoot)

func rotateTank(delta):
	self.rotation += delta * rot_dir * rotationSpeed
	
func applyFriction(delta):
	if acceleration == Vector2.ZERO and veloLocal.length() < 15:
		veloLocal = Vector2.ZERO
	var fritcionForce = veloLocal * friction * delta
	acceleration += fritcionForce

func _physics_process(delta):
	checkInput()
	rotateTank(delta)
	applyFriction(delta)
	veloLocal += acceleration * delta
	velocity = veloLocal.rotated(self.rotation)
	move_and_slide()
