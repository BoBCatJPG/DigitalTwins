extends Node3D


var server := UDPServer.new()
var turtlebot_position: Vector3 = Vector3.ZERO
var threadReceive = true
var thread

# Called when the node enters the scene tree for the first time.
func _ready():
	#thread = Thread.new()
	#thread.start(_receive_data)
	$RealPose.text="RealPose: "+str(turtlebot_position)
	server.listen(9002)
	

func _exit_tree():
	threadReceive = false


func _physics_process(delta):
	server.poll()
	#print("Ricevo")
	if server.is_connection_available():
		var peer: PacketPeerUDP = server.take_connection()
		var packet = peer.get_packet()
		turtlebot_position.x=packet.decode_float(0)/1000
		turtlebot_position.y=$VirtualRobot.global_position.y
		turtlebot_position.z=packet.decode_float(8)/-1000
		$Ghost.global_position = turtlebot_position
		$Ghost.rotation.y=$VirtualRobot.rotation.y
		$RealPose.text="RealPose: "+str(turtlebot_position)
		


func _on_target_position_on_click(newPosition):
		$VirtualRobot._on_target_position_on_click(newPosition)



