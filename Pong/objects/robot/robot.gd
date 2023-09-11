extends Node3D


var server := UDPServer.new()
var lidar_server := UDPServer.new()
var turtlebot_position: Vector3 = Vector3.ZERO
var threadReceive = true
var thread
var object_scene:PackedScene

# Called when the node enters the scene tree for the first time.
func _ready():
	$RealPose.text="RealPose: <NULL>"
	server.listen(9002)
	lidar_server.listen(9002)  # Server per i dati del LiDAR
	
	

func _exit_tree():
	threadReceive = false


func _physics_process(delta):
	$Ghost.rotation.y=$VirtualRobot.rotation.y
	_receive_pos()
	_receive_lidar()
	
		


func _on_target_position_on_click(newPosition):
		$VirtualRobot._on_target_position_on_click(newPosition)
func _receive_pos():
	server.poll()
	if server.is_connection_available():
		var peer: PacketPeerUDP = server.take_connection()
		var packet = peer.get_packet()
		turtlebot_position.x=packet.decode_float(0)/1000
		turtlebot_position.y=$VirtualRobot.global_position.y
		turtlebot_position.z=packet.decode_float(8)/-1000
		$Ghost.global_position = turtlebot_position
		$Ghost.rotation.y=$VirtualRobot.rotation.y
		$RealPose.text="RealPose: "+str(turtlebot_position)
func _receive_lidar():
	# Create a new instance of the object scene
	var object_instance = object_scene.instantiate()
	object_instance.global_position=Vector3(0.30, 0.10, 0)
	# Add the instance to the current scene or another node
	add_child(object_instance)
	
	lidar_server.poll()
	if lidar_server.is_connection_available():
		print("hello")
		var peer: PacketPeerUDP = lidar_server.take_connection()
		var packet = peer.get_packet()
		var distance = packet.decode_float(0)
		print("distance: ", distance)
		
		# Calcola la nuova posizione del cubo rispetto al robot
		var new_position = Vector3(distance, 0.19, 0)  # Supponiamo che il cubo si trovi lungo l'asse X
		new_position += global_transform.origin  # Aggiungi la posizione del robot

		# Istanza il cubo dalla scena del cubo
		
		# Imposta la posizione del cubo
		#cube_instance.global_transform.origin = new_position

		# Aggiungi il cubo come figlio del tuo nodo principale (dove vuoi mostrare i cubi)
		#add_child(cube_instance)
	
	



