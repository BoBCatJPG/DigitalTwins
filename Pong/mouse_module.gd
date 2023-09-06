extends RefCounted

static func get_vector3_from_camera_raycast(camera:Camera3D, cam_2d_coords:Vector2) -> Vector3:
	var ray_from:Vector3 = camera.project_ray_origin(cam_2d_coords)
	var ray_to:Vector3 = ray_from + camera.project_ray_normal(cam_2d_coords)* 1000.0
	var ray_params:PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(ray_from, ray_to)
	
	var result : Dictionary = camera.get_world_3d().direct_space_state.intersect_ray(ray_params)
	
	if result :
		return result.position
	else :
		return Vector3.ZERO

