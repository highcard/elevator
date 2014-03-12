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
		self.floor_list = [False for floor in range(min_floor, max_floor + 1)] #initialize all floors buttons to off
		
	"""Elevator movements"""

	def move(self):
		"""moves elevator in current direction"""
		self.moving = True
		up = self.direction
		if self.cur_floor >= self.max_floor or self.cur_floor <= self.min_floor:
			self.moving = False
			self.switch_direction()
		elif self.cur_floor < self.max_floor or self.cur_floor > self.min_floor:
			self.cur_floor = self.cur_floor + (1 if up else -1)
			print "moved to floor %s" % self.cur_floor #debug
		
	def switch_direction(self):
		"""changes the direction of the elevator True = up / False = down"""
		self.direction = not self.direction

	def up(self):
		""" points the elevator up"""
		self.direction = True

	def down(self):
		""" points the elevator down"""
		self.direction = False

	def stop(self):
		""" stops the elevator from moving"""
		self.moving = False

	def open_door(self):
		"""stops elevator and opens door for passengers"""
		self.stop()
		self.floor_list[self.cur_floor] = False

	"""Floor List Manipulations & Utility Functions"""

	def reset_floor_list(self):
		"""resets the floor list"""
		for i in range(self.min_floor, len(self.floor_list)):
			self.floor_list[i] = False

	def press_floor_button(self, floor):
		"""adds a floor button request"""
		if self.button_in_range(floor):
			self.floor_list[floor] = True

	def remove_floor_button(self, floor):
		"""removes a floor button request"""
		if self.button_in_range(floor):
			self.floor_list[floor] = False

	def check_button(self, floor):
		"""check if button is pressed on current floor"""
		if self.button_in_range(floor):
			return self.floor_list[floor]

	def button_in_range(self, floor):
		"""check if floor is in the range"""
		return floor in range(self.min_floor, self.max_floor + 1)

	def has_button_push(self):
		return True in self.floor_list

	def get_highest_call(self):
		"""returns the highest floor requested"""
		if True in self.floor_list:
			return self.max_floor - self.floor_list[::-1].index(True)
		else:
			return None

	"""action loops"""

	def run(self):
		"""elevator business logic loop"""
		