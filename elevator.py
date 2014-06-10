from types import *

class Elevator(object):
	def __init__(self, id_num, min_floor, max_floor, cur_floor, default_floor, direction):
		## Type Assertions
		assert type(min_floor) is IntType, "is not an integer: %r" % min_floor
		assert type(max_floor) is IntType, 'is not an integer: %r' % max_floor
		assert type(cur_floor) is IntType, 'is not an integer: %r' % cur_floor
		assert type(direction) is BooleanType, 'is not an boolean: %r' % direction

		#Bounds Assertions
		assert min_floor < max_floor, 'invalid min_floor and max_floor values. min: %r, max: %r' % (min_floor, max_floor)
		assert cur_floor >= min_floor and cur_floor <= max_floor, 'cur_floor is out of range: %r' % cur_floor
		
		#Initialize class attributes
		self.id_num = id_num
		self.cur_floor = cur_floor
		self.min_floor = min_floor
		self.max_floor = max_floor
		self.default_floor = default_floor
		self.direction = direction
		self.moving = False
		self.idle = True
		self.floor_list = [False for floor in range(min_floor, max_floor + 1)] #initialize all floors buttons to off
		self.passenger_list = []

	"""Elevator movements"""

	def move(self):
		"""moves elevator in current direction"""
		self.moving = True
		self.idle = False
		up = self.direction
		if self.cur_floor >= self.max_floor or self.cur_floor <= self.min_floor:
			self.moving = False
			self.idle = True
		elif self.cur_floor < self.max_floor or self.cur_floor > self.min_floor:
			self.cur_floor = self.cur_floor + (1 if up else -1)
		
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
		if self.floor_in_range(floor):
			self.floor_list[floor] = True

	def remove_floor_button(self, floor):
		"""removes a floor button request"""
		if self.floor_in_range(floor):
			self.floor_list[floor] = False

	def check_button(self, floor):
		"""check if button is pressed on current floor"""
		if self.floor_in_range(floor):
			return self.floor_list[floor]

	def floor_in_range(self, floor):
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

	def check_idle(self):
		"""sets the elevator's idle status"""
		if not self.has_button_push() and self.cur_floor == self.default_floor:
			self.idle = True
		else:
			self.idle = False
		return self.idle

	def print_stats(self):
		"""prints object attributes"""
		attrs = vars(self)
		print "===Elevator STATS==="
		print ', \n'.join("%s: %s" % item for item in attrs.items())

	"""action loops"""

	def goto_floor(self, target_floor):
		"""sends elevator to a determined floor"""
		if self.floor_in_range(target_floor): #range checking. gotta find a better way to do this...
			if self.cur_floor == target_floor:
				return None
			elif self.cur_floor < target_floor:
				self.up()
				self.move()
				self.goto_floor(target_floor)
			elif self.cur_floor > target_floor:
				self.down()
				self.move()
				self.goto_floor(target_floor)
		elif not self.floor_in_range(target_floor): #error checking
			return None


class Building(object):
	def __init__(self, min_floor, max_floor, lobby, num_elevators):
		self.min_floor = min_floor
		self.max_floor = max_floor
		self.lobby = lobby
		self.elevator_bank = [Elevator(i, self.min_floor, self.max_floor, self.lobby, self.lobby, True) for i in range(0, num_elevators)]
		self.floors = [[] for i in range(min_floor, max_floor + 1)]
		self.call_buttons_up = [False for i in range(min_floor, max_floor + 1)] #initialize call up buttons for each floor
		self.call_buttons_down = [False for i in range(min_floor, max_floor + 1)] #initialize call down buttons for each floor
	
	def list_elevators(self):
		for elevator in self.elevator_bank:
			elevator.print_stats()

	def add_passenger(self, start_floor, dest_floor):
		p = Passenger(start_floor, dest_floor)
		self.floors[start_floor].append(p)

	def call_elevators(self):
		for floor in self.floors:
			for passenger in floor:
				if passenger.start_floor < passenger.dest_floor:
					self.call_buttons_up[passenger.start_floor] = True
				elif passenger.start_floor > passenger.dest_floor:
					self.call_buttons_down[passenger.start_floor] = True


class Passenger(object):
	def __init__(self, start_floor, dest_floor):
		self.start_floor = start_floor
		self.dest_floor = dest_floor


b = Building(0, 10, 1, 5)
p_list = [[4, 8], [8, 2], [3, 9], [4, 2], [0, 8], [1, 8], [3,2]]
for p in p_list:
	b.add_passenger(p[0], p[1])
b.call_elevators()
print "Up: " + str(b.call_buttons_up)
print "Down: " + str(b.call_buttons_down)