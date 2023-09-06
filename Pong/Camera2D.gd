extends Camera2D

@export var target: NodePath = NodePath("")

var targetReference = null
# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	targetReference = get_node_or_null(target)
	if targetReference:
		self.global_position = targetReference.global_position
	pass
