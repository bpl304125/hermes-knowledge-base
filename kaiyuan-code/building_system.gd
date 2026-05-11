# 开元筑城纪 — 建造系统
extends Node3D

@onready var resource_manager = $ResourceManager
@onready var camera = $Camera3D
@onready var ground = $Ground

var building_scenes = {}
var current_mode: String = "house"
var is_placing: bool = false
var preview_mesh: MeshInstance3D

func _ready():
	_build_preview()
	resource_manager.resources_changed.connect(_on_resources_changed)

func _build_preview():
	preview_mesh = MeshInstance3D.new()
	preview_mesh.mesh = BoxMesh.new()
	preview_mesh.material_override = StandardMaterial3D.new()
	preview_mesh.material_override.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	preview_mesh.material_override.albedo_color = Color(1, 1, 1, 0.5)
	add_child(preview_mesh)
	preview_mesh.visible = false

func _input(event):
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		if current_mode == "demolish":
			_try_demolish(event.position)
		else:
			_try_place(event.position)
	elif event is InputEventMouseMotion:
		_update_preview(event.position)

func _try_place(screen_pos: Vector2):
	var result = _raycast_ground(screen_pos)
	if result.is_empty(): return
	var snap_pos = Vector3(round(result.position.x), 0, round(result.position.z))
	resource_manager.place_building(current_mode, snap_pos)
	_spawn_building_visual(current_mode, snap_pos)

func _try_demolish(screen_pos: Vector2):
	var result = _raycast_ground(screen_pos)
	if result.is_empty(): return
	var snap_pos = Vector3(round(result.position.x), 0, round(result.position.z))
	resource_manager.demolish_at(snap_pos)
	_remove_building_visual(snap_pos)

func _raycast_ground(screen_pos: Vector2) -> Dictionary:
	var space_state = get_world_3d().direct_space_state
	var from = camera.project_ray_origin(screen_pos)
	var to = from + camera.project_ray_normal(screen_pos) * 1000
	var query = PhysicsRayQueryParameters3D.create(from, to)
	query.collide_with_bodies = true
	return space_state.intersect_ray(query)

func _update_preview(screen_pos: Vector2):
	if current_mode == "demolish": return
	var result = _raycast_ground(screen_pos)
	if result.is_empty():
		preview_mesh.visible = false; return
	var snap = Vector3(round(result.position.x), 0, round(result.position.z))
	preview_mesh.position = snap + Vector3(0, 0.5, 0)
	preview_mesh.visible = true
	preview_mesh.material_override.albedo_color = Color.GREEN if resource_manager.can_place(current_mode) else Color.RED

func _spawn_building_visual(type: String, pos: Vector3):
	var box = MeshInstance3D.new()
	box.mesh = BoxMesh.new()
	if type == "road":
		box.scale = Vector3(1, 0.05, 1)
	else:
		box.scale = Vector3(0.8, 1.0, 0.8)
	box.material_override = StandardMaterial3D.new()
	box.material_override.albedo_color = Color(randf()*0.3+0.5, randf()*0.3+0.3, randf()*0.3+0.5)
	box.position = pos + Vector3(0, 0.5, 0)
	add_child(box)

func _remove_building_visual(pos: Vector3):
	for child in get_children():
		if child is MeshInstance3D and child.position.distance_to(pos) < 1.0:
			child.queue_free()

func _on_resources_changed():
	pass # UI更新由HUD处理
