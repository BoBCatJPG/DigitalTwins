extends CharacterBody3D



# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")
@export var steer_speed:float = 4.0
@onready var navAgent = $NavigationAgent3D
@onready var navTimer = $NavTimer
var socket: PacketPeerUDP
var TURTLEBOT_IP = "127.0.0.1"
var TURTLEBOTR_IP = "192.168.70.109"
const TURTLEBOT_PORT = 9001
var next_position=Vector3.ZERO
var turtlebot_position: Vector3 = Vector3.ZERO
var hasReceivedPosition = false
var last_sent_position: Vector3  # Memorizza l'ultima posizione inviata al TurtleBot
var firstChange = true
var nav_path_goal_position:Vector3
var linearVelocityLength: float
var angle
func _ready():
	print(rotation_degrees.y)
	print(deg_to_rad(rotation.y))
	print(TURTLEBOTR_IP)
	socket = PacketPeerUDP.new()
	$VirtualPose.text="Virtual Pose: "+str(global_position)
	var result = socket.connect_to_host(TURTLEBOTR_IP, TURTLEBOT_PORT)
	if result == OK:
		print("Connessione al TurtleBot stabilita.")
	else:
		print("Errore durante la connessione al TurtleBot:", result)
	

func _physics_process(delta):
	if navAgent.is_navigation_finished():
		return
	
	
	var direction:Vector3 = global_transform.origin.direction_to(navAgent.get_next_path_position()).normalized()*0.15
	var steered_velocity:Vector3 = (direction-velocity)*delta*steer_speed
	var new_agent_velocity:Vector3 = velocity +steered_velocity
	navAgent.set_velocity(new_agent_velocity)
	
	
	_send_data(global_transform.origin,velocity,0)
	move_and_slide()
	
	$VirtualPose.text="Virtual Pose: "+str(global_position)
	
	#if hasReceivedPosition:
			# Esegui il movimento solo se hai ricevuto nuovi dati di posizione
			#global_position = turtlebot_position
			#hasReceivedPosition = false  

func setTargetPosition(new_pos:Vector3):
	navAgent.set_target_position(new_pos)

func _on_target_position_on_click(newPosition):
	firstChange = false
	nav_path_goal_position = newPosition
	setTargetPosition(newPosition)

func _on_navigation_agent_3d_velocity_computed(safe_velocity):
	
	#if safe_velocity.length()<=0.4:
	velocity = safe_velocity
	rotation.y = atan2(velocity.x, velocity.z)


func _on_nav_timer_timeout():
	if firstChange : return
	setTargetPosition(nav_path_goal_position)
	
	

func _send_data(pos: Vector3,vel,flag):
	var packed_array: PackedFloat32Array = PackedFloat32Array()
	packed_array.resize(5)
	packed_array.set(0, pos.x*1000)
	angle=deg_to_rad(rotation_degrees.y)-deg_to_rad(90)
	packed_array.set(1, angle)
	packed_array.set(2, pos.z*-1000)
	packed_array.set(3, vel.length()*1000)
	if flag==1:
		packed_array.set(4,1.0)
	else:
		packed_array.set(4,0.0)
	print(angle)
	socket.put_packet(packed_array.to_byte_array())
	

func _on_button_pressed():
	var reset_pos=global_position
	_send_data(reset_pos,velocity,1)
	print("pose reset...",reset_pos.x*1000,",",reset_pos.z*1000,",",angle)
	

