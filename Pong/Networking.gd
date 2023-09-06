extends Node

signal dataReceived

@export var pathCar:NodePath
@export var pathCarRigid:NodePath


var car
var carRigid

var socket
var thread
var activeThread = true

var newVel = 0

func _ready():
	car = get_node(pathCar)
	carRigid = get_node(pathCarRigid)
	socket = PacketPeerUDP.new()
	socket.connect_to_host("127.0.0.1", 9001)
	
	thread = Thread.new()
	thread.start(self._thread, Thread.PRIORITY_HIGH)

func _thread():
	while self.activeThread:
		socket.put_var("Ciao")
		if socket.get_available_packet_count() > 0:
			var data = socket.get_packet()
			var spb = StreamPeerBuffer.new()
			spb.data_array = data
			var vel = spb.get_double() 
			var steer =  spb.get_double()
			var acc = spb.get_double()
			print(vel," - ", steer," - ", acc)
			emit_signal("dataReceived",vel, steer, acc)
			#car.rot_dir = (steer/30) * -1
			#car.veloLocal.x = vel
			
			#carRigid.steer = ((steer/30) * -1) * 0.4
			#carRigid.forcee = (vel/!0) * 150
			

func _process(delta):
	
	
	pass
