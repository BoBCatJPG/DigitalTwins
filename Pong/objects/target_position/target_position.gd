extends Marker3D
signal onClick

const module_mouse : GDScript = preload("res://mouse_module.gd")
var pos = Vector3.ZERO

@onready var ghost = $Ghost

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.
	

func _input(event:InputEvent):
	if Input.is_action_just_pressed("mouse_left_click"):
		var mouse_pos:Vector2 = get_viewport().get_mouse_position()
		var camera:Camera3D = get_viewport().get_camera_3d()
		var camera_ray_coords:Vector3 = module_mouse.get_vector3_from_camera_raycast(camera, mouse_pos)
		if camera_ray_coords == Vector3.ZERO:
			return
		self.global_position = camera_ray_coords
		ghost.global_position = camera_ray_coords
		self.emit_signal("onClick", camera_ray_coords)
		
	if event is InputEventMouseMotion:
		var mouse_pos:Vector2 = get_viewport().get_mouse_position()
		var camera:Camera3D = get_viewport().get_camera_3d()
		var camera_ray_coords:Vector3 = module_mouse.get_vector3_from_camera_raycast(camera, mouse_pos)
		ghost.global_position = camera_ray_coords


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if ghost.global_position == Vector3.ZERO:
		ghost.visible = false
	else:
		ghost.visible = true
	pass
