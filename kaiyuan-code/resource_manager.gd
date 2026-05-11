# 开元筑城纪 — 核心资源管理
extends Node

# 资源定义
var gold: int = 1000
var population: int = 0
var power: int = 60
var water: int = 60
var happiness: int = 80
var trade_value: int = 0
var culture: int = 0
var era: int = 0
var tax_rate: float = 0.1

# 建筑列表
var buildings: Array = []
var selected_building_type: String = "house"

# 建筑类型定义
const BUILDING_DATA = {
	"house":    {"cost":80,  "pop":10, "power":-2, "water":-3, "happiness":2,  "color":"8899cc"},
	"shop":     {"cost":150, "pop":5,  "power":-3, "water":-2, "happiness":3,  "gold_per_sec":0.5, "color":"ffaa44"},
	"factory":  {"cost":250, "pop":8,  "power":-5, "water":-5, "happiness":-8, "gold_per_sec":1.5, "color":"888888"},
	"power":    {"cost":400, "power":35, "happiness":-3, "color":"44aaff"},
	"water":    {"cost":350, "power":-2, "water":30, "happiness":2,  "color":"44ccff"},
	"park":     {"cost":120, "happiness":12, "color":"44cc44"},
	"road":     {"cost":30,  "happiness":1,  "color":"554433"},
	"pagoda":   {"cost":600, "pop":20, "unlock_pop":3000, "trade":5,   "happiness":8,  "color":"cc4444"},
	"temple":   {"cost":800, "pop":15, "unlock_pop":5000, "trade":10,  "happiness":10, "color":"dd8844"},
	"palace":   {"cost":2000,"pop":50, "unlock_pop":10000,"trade":20,  "happiness":15, "color":"ffcc00"},
	"port":     {"cost":1500,"pop":30, "unlock_trade":100,"trade":30,  "gold_per_sec":3, "color":"4488aa"},
}

signal resources_changed

func can_afford(type: String) -> bool:
	return gold >= BUILDING_DATA[type]["cost"]

func can_place(type: String) -> bool:
	var bt = BUILDING_DATA[type]
	if bt.has("unlock_pop") and population < bt["unlock_pop"]: return false
	if bt.has("unlock_trade") and trade_value < bt["unlock_trade"]: return false
	if power + bt.get("power", 0) < 0: return false
	if water + bt.get("water", 0) < 0: return false
	return can_afford(type)

func place_building(type: String, position: Vector3) -> bool:
	if not can_place(type): return false

	var bt = BUILDING_DATA[type]
	gold -= bt["cost"]
	population += bt.get("pop", 0)
	power += bt.get("power", 0)
	water += bt.get("water", 0)
	happiness += bt.get("happiness", 0)
	trade_value += bt.get("trade", 0)

	# 时代检测
	if population >= 10000: era = 2
	elif population >= 5000: era = 1

	var building = {
		"type": type,
		"position": position,
		"gold_per_sec": bt.get("gold_per_sec", 0)
	}
	buildings.append(building)
	resources_changed.emit()
	return true

func demolish_at(position: Vector3):
	for i in range(buildings.size() - 1, -1, -1):
		var b = buildings[i]
		if b["position"].distance_to(position) < 1.0:
			var bt = BUILDING_DATA[b["type"]]
			gold += int(bt["cost"] * 0.3)
			population -= bt.get("pop", 0)
			power -= bt.get("power", 0)
			water -= bt.get("water", 0)
			happiness -= bt.get("happiness", 0)
			trade_value -= bt.get("trade", 0)
			buildings.remove_at(i)
			resources_changed.emit()
			return

func _process(delta):
	# 经济循环
	var income: float = population * tax_rate * 0.01
	for b in buildings:
		income += b.get("gold_per_sec", 0) * delta
	gold += int(income)
