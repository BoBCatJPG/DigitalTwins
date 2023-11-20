extends Node3D

@onready var Start_button=$GUI/Menu/VBoxContainer/Start_button
@onready var Starting_point_button=$GUI/Menu/VBoxContainer/Starting_point_button
var hasconnected=false

func _ready():
	$Robot/VirtualRobot.semaforo=false
	set_process_input(true)
	Start_button.connect("pressed",_on_Start_button_pressed)
	Starting_point_button.connect("pressed",_on_Starting_point_button_pressed)
	$TargetPosition.hide()
	$TargetPosition.semaforo_menu=false
	$Robot.semaforo_starting_point=false
	
func _on_back_to_main_menu_pressed():
	$Robot/VirtualRobot.semaforo=false
	$TargetPosition.hide()
	$TargetPosition.semaforo_menu=false
	$TargetPosition.global_position=Vector3(0,0,0)
	$Robot.semaforo_starting_point=false
	$GUI.show()
	


func _on_Start_button_pressed():
	
	if not hasconnected:
		print("Controller Started")
		var ip_assigned=$GUI/Menu/VBoxContainer/HBoxContainer/Turtlebotip_input.text
		$Robot/VirtualRobot.TURTLEBOTR_IP=ip_assigned
		print("ip del turtlebot assegnato: ",$Robot/VirtualRobot.TURTLEBOTR_IP)
		$Robot/VirtualRobot.start_socket()
		hasconnected=true

	$Robot/VirtualRobot.semaforo=true
	$GUI.hide()
	$TargetPosition.show()
	$TargetPosition.semaforo_menu=true

func _on_Starting_point_button_pressed():
	$GUI.hide()
	$Robot.semaforo_starting_point=true


