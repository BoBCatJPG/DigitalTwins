extends Node3D


var server := UDPServer.new()
var lidar_server := UDPServer.new()
var turtlebot_position: Vector3 = Vector3.ZERO
var threadReceive = true
var new_pos
var last_position
var obstacle
var vertices:PackedVector3Array=[360]
@onready var ostacolo_reale=$ostacolo
var obstacle_scene=load("res://lidarobstacle.tscn")
var obstacle_vett=[]
var turtle_theta

# Called when the node enters the scene tree for the first time.
func _ready():
	$RealPose.text="RealPose: <NULL>"
	server.listen(9002)
	lidar_server.listen(9003)
	var obstacle_scene=preload("res://lidarobstacle.tscn")
	
	for i in range(360):
		obstacle=obstacle_scene.instantiate()
		obstacle_vett.append(obstacle)
		add_child(obstacle)
		obstacle.position=Vector3(0,0.25,-2)
		
		
	
func _exit_tree():
	threadReceive = false

func _physics_process(delta):
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
		turtlebot_position.z=packet.decode_float(4)/-1000
		turtle_theta=packet.decode_float(8)
		$Ghost.global_position = turtlebot_position
		$Ghost.rotation.y=$VirtualRobot.rotation.y
		$RealPose.text="RealPose: "+str(turtlebot_position)
'''
func _receive_lidar():
	lidar_server.poll()
	if lidar_server.is_connection_available():
		var peer: PacketPeerUDP = lidar_server.take_connection()
		var packet = peer.get_packet()

		# Decodifica i dati ricevuti (360 float values)
		for i in range(360):
			var distance = packet.decode_float(i * 4)
		# Ignora le letture di Lidar troppo lontane (imposta una soglia)
			if distance > 0.0 and distance<1:  # Soglia in millimetri (1 metro)
				var angle = deg_to_rad(i)  # Converti l'angolo in radianti
				var x = distance * cos(angle)  # Calcola la posizione lungo l'asse X
				var z = distance * sin(angle)*-1  # Calcola la posizione lungo l'asse Y
				var y = 0.20
				new_pos=Vector3(x,y,z)
				# Add the new vertex to the list
				#vertices.push_back(Vector3(x, y, z))
				if(last_position!=new_pos):
					last_position=new_pos
					obstacle=obstacle_scene.instantiate()
					obstacle.position=Vector3(x, y, z)
					add_child(obstacle)
'''
func _receive_lidar():
	lidar_server.poll()
	if lidar_server.is_connection_available():
		var peer: PacketPeerUDP = lidar_server.take_connection()
		var packet = peer.get_packet()
		
		var angles = []
		for i in range(360):
			angles.append(deg_to_rad(i))
		# Decodifica i dati ricevuti (360 float values)
		for i in range(360):
			var distance = packet.decode_float(i * 4)
		# Ignora le letture di Lidar troppo lontane (imposta una soglia)
			#if distance > 0.0 and distance<=2.5:  # Soglia in millimetri (1 metro)
			var angle = angles[i]  # Converti l'angolo in radianti
			var x = distance * cos(angle+turtle_theta)+global_position.x  #Calcola la posizione lungo l'asse X
			var z = distance * sin(angle+turtle_theta)*-1+global_position.z  # Calcola la posizione lungo l'asse Y
			var y = 0.25
			#x += global_position.x
			#y += global_position.y
			#z += global_position.z
			obstacle_vett[i].position=Vector3(x,y,z)
			





func _on_reset_obstacle_pressed():
	for i in range(360):
		obstacle_vett[i].position=Vector3(0,0.25,-2)
	
