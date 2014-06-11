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
State = enum(IDLE=1, DISPATCHED=2, RETURNING=3)
Direction = enum(UP=1, DOWN=2)
Doors =	enum(CLOSED=1, OPENED=2)

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

	def open_door(self):
		"""Opens door for passengers"""
		self.doors = Doors.OPENED
		self.remove_floor_button(self.cur_floor)

	def close_door(self):
		"""Closes elevator door and continues moving"""
		self.doors = Doors.CLOSED

	def set_idle(self):
		self.state = State.IDLE
		self.reset_floor_list()

	def deliver(self):
		self.state = State.RETURNING

	def dispatch(self):
		self.state = State.DISPATCHED

	"""Call list manipulations & handling"""

	def check_button(self, floor):
		"""check if button is pressed on current floor"""
		return floor in self.floor_list

	def has_button_push(self):
		if self.floor_list:
			return True
		elif not self.floor_list:
			return False

	def get_highest_call(self):
		"""returns the highest floor requested."""
		return max(self.floor_list)

	def check_idle(self):
		"""sets the elevator's idle status"""
		if not self.has_button_push() and self.cur_floor == self.default_floor:
			self.set_idle()
		return self.state == State.IDLE

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

	def elevator_command(self, elevator):
		"""Elevator State Handling"""
		if elevator.state == State.IDLE and elevator.cur_floor == self.lobby:
			if elevator.has_button_push():
				elevator.state = State.DISPATCHED
			else:
				elevator.state = State.IDLE
		### error state - elevator should not be idle unless at lobby ###
		elif elevator.state == State.IDLE and elevator.cur_floor != self.lobby:
			elevator.state = State.RETURNING
			elevator.reset_floor_list()

	def run_elevators(self):
		for elevator in self.elevator_bank:
			execute_command(elevator)

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
	return

if __name__ == "__main__":
	main()