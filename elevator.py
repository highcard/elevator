"""
Elevator.py elevator bank/passenger Simulator:
Models an bank of elevators in a building that respond to passengers.
"""

################ 
# GLOBAL 
################ 

IDLE_STATE = 'idle'
UP_STATE = 'up'
DOWN_STATE = 'down'
MOVE_STATE = 'move'
OPEN_STATE = 'open'

################ 
# Elevator 
################ 

class Elevator(object):
	def __init__(self, parent, id_num, cur_floor, default_floor, state):
		#Initialize class attributes
		self.id_num = id_num
		self.cur_floor = cur_floor
		self.default_floor = default_floor
		self.state = state
		self.floor_list = [] #initialize empty list of floor requests
		self.passenger_list = []

	"""Floor List Manipulations & Utility Functions"""

	def reset_floor_list(self):
		"""resets the floor list"""
		self.floor_list = [] #initialize empty list of floor requests

	def press_floor_button(self, floor):
		"""adds a floor button request"""
		self.floor_list.append(floor)

	def remove_floor_button(self, floor):
		"""removes a floor button request"""
		if floor in self.floor_list:
			self.floor_list.remove(floor)

	"""Elevator movements & state-changes"""

	def move_up(self):
		"""moves elevator in the down direction"""
		self.state = UP_STATE
		self.cur_floor += 1
		
	def move_down(self):
		"""moves elevator in the down direction"""
		self.state = DOWN_STATE
		self.cur_floor -= 1

	def open_door(self):
		"""stops elevator and opens door for passengers"""
		self.state = OPEN_STATE
		self.remove_floor_button(self.cur_floor)

	def set_idle(self):
		self.state = IDLE_STATE

	###refactored above here!!

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

################ 
# Building 
################ 


class Building(object):
	def __init__(self, min_floor, max_floor, lobby, num_elevators):
		#Bounds Assertions
		assert min_floor < max_floor, 'invalid min_floor and max_floor values. min: %r, max: %r' % (min_floor, max_floor)
		#Initialize Class Variables
		self.min_floor = min_floor
		self.max_floor = max_floor
		self.lobby = lobby
		self.elevator_bank = [Elevator(self, i, self.lobby, self.lobby, IDLE_STATE) for i in range(0, num_elevators)]
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

################ 
# Floors
################ 




################ 
# Passenger 
################ 

class Passenger(object):
	def __init__(self, start_floor, dest_floor):
		self.start_floor = start_floor
		self.dest_floor = dest_floor



################ 
# Main Function
################ 

def main():
	b = Building(0, 10, 1, 1)
	e = b.elevator_bank[0]
	e.print_stats()
	e.move_down()
	e.print_stats()
	e.open_door()
	e.print_stats()

if __name__ == "__main__":
	main()
