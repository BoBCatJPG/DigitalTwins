extends Node3D




func _on_back_to_main_menu_pressed():
	get_tree().change_scene_to_file("res://menu.tscn")


func _on_updatemap_timeout():
	var rid=$NavigationRegion3D.get_region_rid()
	NavigationServer3D.map_force_update(rid)
