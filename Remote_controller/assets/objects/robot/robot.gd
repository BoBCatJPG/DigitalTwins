extends Node3D


var server := UDPServer.new()
var lidar_server := UDPServer.new()
var turtlebot_position: Vector3 = Vector3.ZERO
var threadReceive = true
var new_pos
var last_position
var obstacle
var vertices:PackedVector3Array=[360]
var obstacle_scene=preload("res://objects/Lidar obstacle/lidarobstacle.tscn")
var obstacle_vett=[]
var turtle_theta
var obstacle_dict = {}
# Called when the node enters the scene tree for the first time.

var lidarThread = null
var exitThread = false
func _ready():
	$RealPose.text="RealPose: <NULL>"
	server.listen(9002)
	lidar_server.listen(9003)
	lidarThread = Thread.new()
	var err = lidarThread.start(threadLidarFunc)
	print("Errore? ", err)

func _exit_tree():
	threadReceive = false
	exitThread = true

func _physics_process(delta):
	_receive_pos()
	#_receive_lidar()

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
		$RealPose.text="RealPose: "+str(turtlebot_position, turtle_theta)


func threadLidarFunc():
	print("Inizio thread")
	while not exitThread:
		_receive_lidar()
	print("Chiudo thread")
		
func _receive_lidar():
	lidar_server.poll()
	if lidar_server.is_connection_available():
		var peer: PacketPeerUDP = lidar_server.take_connection()
		var packet = peer.get_packet()

		var angles = []
		for i in range(360):
			angles.append(deg_to_rad(i))
			
		var robot_rotation = rotation.y

# Decodifica i dati ricevuti (360 float values)
		for i in range(360):
			var distance = packet.decode_float(i * 4)
# Ignora le letture di Lidar troppo lontane (imposta una soglia)
			if distance> 0 and distance < 0.3:  # Soglia in millimetri (1 metro)
				turtle_theta = turtle_theta if turtle_theta!= null else 0
				var angle = angles[i] + turtle_theta
				

# Verifica se un ostacolo già esiste in base all'angolo
				if not obstacle_dict.has(i):
					var x = (distance ) * cos(angle) + $VirtualRobot.global_position.x  # Calcola la posizione lungo l'asse X
					var z = (distance ) * sin(angle)*-1 + $VirtualRobot.global_position.z # Calcola la posizione lungo l'asse Y
					var y = $VirtualRobot.global_transform.origin.y
					
# Se non esiste, crea un nuovo ostacolo e aggiungilo alla scena
					var new_obstacle = obstacle_scene.instantiate()
					
					add_child(new_obstacle)
					new_obstacle.global_position = Vector3(x, y, z)
					obstacle_dict[i] = new_obstacle
				else:
					var x = ((distance ) * cos(angle)) + $VirtualRobot.global_position.x  # Calcola la posizione lungo l'asse X
					var z = ((distance ) * sin(angle)*-1) + $VirtualRobot.global_position.z# Calcola la posizione lungo l'asse Y
					var y = $VirtualRobot.global_transform.origin.y
				# Se esiste, aggiorna la sua posizione
					obstacle_dict[i].global_position = Vector3(x, y, z)
				obstacle_dict[i].id_angle = i
				obstacle_dict[i].distance = distance
				obstacle_dict[i].active()
			else:
				# Se il Lidar non rileva un ostacolo, rimuovi l'ostacolo se esiste
				if obstacle_dict.has(i):
					obstacle_dict[i].deactive() 
					#obstacle_dict[i].queue_free()
			#		obstacle_dict[i] = null





