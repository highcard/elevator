from types import *

class Elevator(object):
	def __init__(self, min_floor, max_floor, cur_floor, default_floor, direction):
		## Type Assertions
		assert type(min_floor) is IntType, "is not an integer: %r" % min_floor
		assert type(max_floor) is IntType, 'is not an integer: %r' % max_floor
		assert type(cur_floor) is IntType, 'is not an integer: %r' % cur_floor
		assert type(direction) is BooleanType, 'is not an boolean: %r' % direction

		#Bounds Assertions
		assert min_floor < max_floor, 'invalid min_floor and max_floor values. min: %r, max: %r' % (min_floor, max_floor)
		assert cur_floor >= min_floor and cur_floor <= max_floor, 'cur_floor is out of range: %r' % cur_floor
		
		#Initialize class attributes
		self.cur_floor = cur_floor
		self.min_floor = min_floor
		self.max_floor = max_floor
		self.default_floor = default_floor
		self.direction = direction
		self.moving = False
		self.floor_list = [False for floor in range(min_floor, max_floor)] #initialize all floors buttons to off

	# prints object attributes
	def print_stats(self):
		attrs = vars(self)
		print "===PRINTING STATS==="
		print ', \n'.join("%s: %s" % item for item in attrs.items())

	# moves elevator in current direction
	def move(self):
		self.moving = True
		up = self.direction
		floor = self.cur_floor
		ground = self.min_floor
		roof = self.max_floor

		if floor >= roof or floor <= ground:
			self.moving = False
			self.switch_direction()
		self.cur_floor = self.cur_floor + (1 if up else -1)
		
	# changes the direction of the elevator True = up / False = down
	def switch_direction(self):
		self.direction = not self.direction

	# points the elevator up
	def up(self):
		self.direction = 1

	# points the elevator down
	def down(self):
		self.direction = 0

	# stops the elevator from moving
	def stop(self):
		self.moving = False

	# resets the floor list
	def reset_floor_list(self):
		for floor in self.floor_list:
			floor = False

	# adds a floor button request
	def press_floor_button(self, floor):
		self.floor_list[floor] = True

	# removes a floor button request
	def remove_floor_button(self, floor):
		self.floor_list[floor] = False

	# check if button is pressed on current floor
	def check_button(self, floor):
		return self.floor_list[floor]


myElevator = Elevator(0, 10, 1, 1, True)
myElevator.print_stats()
myElevator.press_floor_button(1)
myElevator.print_stats()
print myElevator.check_button(1)
print myElevator.check_button(2)
myElevator.remove_floor_button(1)
print myElevator.check_button(1)