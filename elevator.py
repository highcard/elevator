"""
Elevator.py elevator bank/passenger Simulator:
Models an bank of elevators in a building that respond to passengers.
WORK-IN-PROGRESS
"""

################ 
# GLOBAL ENUMERATIONS	- Yeah, I know that Enums is supported in 3.4, but this works in 2.7
################ 

def enum(**enums):
    return type('Enum', (), enums)
State = enum(IDLE=0, RESPONDING=1, RETURNING=2)
Direction = enum(DOWN=0, UP=1)
Doors =	enum(CLOSED=0, OPENED=1)

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
		self.direction = Direction.UP
		self.floor_list = [] #initialize empty list of floor requests
		self.doors = Doors.CLOSED
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
		self.direction = Direction.UP
		self.cur_floor += 1
		
	def move_down(self):
		"""moves elevator in the down direction"""
		self.direction = Direction.DOWN
		self.cur_floor -= 1

	def move(self):
		if self.direction == Direction.UP:
			self.move_up()
		elif self.direction == Direction.DOWN:
			self.move_down()
	
	def open_door(self):
		"""Opens door for passengers"""
		self.doors = Doors.OPENED
		self.remove_floor_button(self.cur_floor)

	def close_door(self):
		"""Closes elevator door and continues moving"""
		self.doors = Doors.CLOSED

	"""RETURNING list manipulations & handling"""

	def has_call(self):
		if self.floor_list:
			return True
		elif not self.floor_list:
			return False

	def get_farthest_call(self):
		"""returns the farthest floor requested in the direction of travel."""
		if self.has_call():
			if self.direction == Direction.UP:
				return max(self.floor_list)
			elif self.direction == Direction.DOWN:
				return min(self.floor_list)

	"""State-based actions"""

	def idling_action(self):
		"""action for idle state"""
		if self.has_call():
			self.state = State.RESPONDING

	def returning_action(self):
		"""action for returning state"""
		if self.cur_floor in self.floor_list:
			self.open_door()
		else:
			self.move()

	def responding_action(self):
		"""action for responding state"""
		if self.get_farthest_call() == self.cur_floor:
			self.open_door()
		else:
			self.move()

	def execute_state(self):
		"""execute next state-based action"""
		if self.doors == Doors.OPENED:
			self.doors = Doors.CLOSED
		elif self.doors == Doors.CLOSED:
			if self.state == State.IDLE:
				self.idling_action()
			elif self.state == State.RESPONDING:
				self.responding_action()
			elif self.state == State.RETURNING:
				self.returning_action()

	def set_state(self):
		if self.has_call() and self.direction == Direction.UP and self.state != State.RETURNING:
			if self.get_farthest_call() < self.cur_floor:
				self.direction = Direction.DOWN
				self.state = State.RETURNING
			elif self.get_farthest_call() >= self.cur_floor:
				self.state = State.RESPONDING
		elif self.has_call() and self.direction == Direction.DOWN and self.state != State.RETURNING:
			if self.get_farthest_call() > self.cur_floor:
				self.direction = Direction.UP
				self.state = State.RETURNING
			elif self.get_farthest_call() <= self.cur_floor:
				self.state = State.RESPONDING
		elif self.has_call() and self.cur_floor == self.default_floor and self.state == State.RETURNING:
			if not self.cur_floor in self.floor_list:
				self.state = State.RESPONDING
		elif not self.has_call() and self.cur_floor == self.default_floor:
			self.direction = Direction.UP
			self.state = State.IDLE
		elif not self.has_call() and self.cur_floor > self.default_floor:
			self.direction = Direction.DOWN
			self.state = State.RETURNING
		elif not self.has_call() and self.cur_floor < self.default_floor:
			self.direction = Direction.UP
			self.state = State.RETURNING

	def run_elevator(self):
		self.execute_state()
		self.set_state()
		print "Floor: %s; Doors: %s; State: %s; Buttons: %s" % (self.cur_floor, self.doors, self.state, self.floor_list) #debug for main function


################ 
# Building 
################ 

class Building(object):
	def __init__(self, min_floor, max_floor, lobby, num_elevators):
		#Initialize Class Variables
		self.min_floor = min_floor
		self.max_floor = max_floor
		self.lobby = lobby
		self.elevator_bank = [Elevator(self, i, self.lobby, self.lobby, State.IDLE) for i in range(0, num_elevators)]
		self.floors = [Floor(i) for i in range(min_floor, max_floor + 1)]

	def add_passenger(self, start_floor, dest_floor):
		p = Passenger(start_floor, dest_floor)
		self.floors[start_floor].append(p)

	def call_all_floors(self):
		for floor in self.floors:
			floor.call_elevators()

	def run(self):
		while(True):
			for e in self.elevator_bank:
				e.run_elevator()
			if e.state == State.IDLE:
				break

################ 
# Floor
################ 

class Floor(object):
	def __init__(self, floor_number):
		self.floor_number = floor_number
		self.call_button_up = False
		self.call_button_down = False
		self.waiting = []

	def call_elevators(self):
		for passenger in waiting:
			if self.floor_number < passenger.dest_floor:
				self.call_button_up = True
			elif self.floor_number > passenger.dest_floor:
				self.call_button_down = True

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
	print ""
	print "Simulating Building Parameters:"
	print "==============================="
	print "Lowest Floor: 0"
	print "Highest Floor: 10"
	print "Lobby Floor: 1"
	print "Number of Elevators: 1"
	print "Buttons Pressed: 0, 3, 6, 9"
	b = Building(0, 10, 1, 1)
	for i in range(0, 10, 3):
		b.elevator_bank[0].press_floor_button(i)
	b.elevator_bank[0].press_floor_button(1)
	b.run()

if __name__ == "__main__":
	main()