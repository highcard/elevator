"""
Elevator.py elevator bank/passenger Simulator:
Models an bank of elevators in a building that respond to passengers.
WORK-IN-PROGRESS
"""

import time
import os
import sys

################ 
# GLOBAL ENUMERATIONS	- Yeah, I know that Enums is supported in 3.4, but this works in 2.7
################ 

def enum(**enums):
    return type('Enum', (), enums)
State = enum(IDLE="IDLE", RESPONDING="RESPONDING", RETURNING="RETURNING")
Direction = enum(DOWN="DOWN", UP="UP")
Doors =	enum(CLOSED="CLOSED", OPENED="OPEN")

################ 
# Elevator 
################ 

class Elevator(object):
	def __init__(self, parent, id_num, cur_floor, default_floor):
		#Initialize class attributes
		self.id_num = id_num
		self.cur_floor = cur_floor
		self.default_floor = default_floor
		self.state = State.IDLE
		self.direction = Direction.UP
		self.doors = Doors.CLOSED
		self.up_queue = [] #initialize empty list of floor requests
		self.down_queue = []
		self.button_lights = []
		self.passenger_list = []

	"""Floor List Manipulations & Utility Functions"""

	def reset_floor_queues(self):
		"""resets the floor queues"""
		self.up_queue = [] #initialize empty list of floor requests
		self.down_queue = [] #initialize empty list of floor requests
		self.button_lights = [] #initialize empty list of floor requests

	def press_floor_button(self, floor):
		"""adds a floor button request"""
		if floor == self.cur_floor:
			if self.direction == Direction.UP and not floor in self.up_queue:
				self.up_queue.append(floor)
			elif self.direction == Direction.DOWN and not floor in self.down_queue:
				self.down_queue.append(floor)
		elif floor < self.cur_floor and not floor in self.down_queue:
			self.down_queue.append(floor)
		elif floor > self.cur_floor and not floor in self.up_queue:
			self.up_queue.append(floor)

	def remove_floor_button(self, floor):
		"""removes a floor button request"""
		if floor in self.up_queue:
			self.up_queue.remove(floor)
		if floor in self.down_queue:
			self.down_queue.remove(floor)

	"""Elevator movements & state-changes"""

	def move_up(self):
		"""moves elevator in the down direction"""
		self.cur_floor += 1
		
	def move_down(self):
		"""moves elevator in the down direction"""
		self.cur_floor -= 1

	def switch_direction(self):
		if self.direction == Direction.UP:
			self.direction = Direction.DOWN
		elif self.direction == Direction.DOWN:
			self.direction = Direction.UP

	def move(self):
		if self.direction == Direction.UP:
			self.move_up()
		elif self.direction == Direction.DOWN:
			self.move_down()
	
	def open_door(self):
		"""Opens door for passengers"""
		self.doors = Doors.OPENED

	def close_door(self):
		"""Closes elevator door and continues moving"""
		self.doors = Doors.CLOSED

	"""RETURNING list manipulations & handling"""

	def has_call(self):
		if self.up_queue or self.down_queue:
			return True
		else:
			return False

	def get_farthest_call(self):
		"""returns the farthest floor requested in the direction of travel."""
		if self.has_call():
			if self.direction == Direction.UP and self.up_queue:
				return max(self.up_queue)
			elif self.direction == Direction.UP and not self.up_queue:
				return min(self.down_queue)
			elif self.direction == Direction.DOWN and self.down_queue:
				return min(self.down_queue)
			elif self.direction == Direction.DOWN and self.up_queue:
				return max(self.up_queue)

	"""STATE HANDLING"""

	def idling_action(self):
		"""action for idle state"""
		if self.has_call():
			if self.up_queue:
				self.direction = Direction.UP
			elif self.down_queue:
				self.direction = Direction.DOWN
			self.state = State.RESPONDING
			self.responding_action()

	def responding_action(self):
		"""action for responding state"""
		if self.has_call():
			if self.direction == Direction.UP and self.cur_floor in self.up_queue:
				self.open_door()
				self.up_queue.remove(self.cur_floor)
			elif self.direction == Direction.DOWN and self.cur_floor in self.down_queue:
				self.open_door()
				self.down_queue.remove(self.cur_floor)
			else:
				self.set_direction()
				self.move()
		elif not self.has_call():
			self.state = State.RETURNING
			self.returning_action()

	def returning_action(self):
		""" action for returning to lobby state"""
		if self.has_call():
			self.state = State.RESPONDING
			self.responding_action()
		elif not self.has_call():
			if self.cur_floor > self.default_floor:
				self.direction = Direction.DOWN
				self.move()
			elif self.cur_floor < self.default_floor:
				self.direction = Direction.UP
				self.move()
			elif self.cur_floor == self.default_floor:
				self.state = State.IDLE

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

	def set_direction(self):
		if self.has_call():
			if self.get_farthest_call() == None:
				self.switch_direction()
			elif self.direction == Direction.UP and self.get_farthest_call() < self.cur_floor:
				self.switch_direction()
			elif self.direction == Direction.DOWN and self.get_farthest_call() > self.cur_floor:
				self.switch_direction()

################ 
# Building 
################ 

class Building(object):
	def __init__(self, min_floor, max_floor, lobby, num_elevators):
		#Initialize Class Variables
		self.min_floor = min_floor
		self.max_floor = max_floor
		self.lobby = lobby
		self.elevator_bank = [Elevator(self, i, self.lobby, self.lobby) for i in range(0, num_elevators)]
		self.floors = [Floor(i) for i in range(min_floor, max_floor + 1)]
		self.frame = 0
		self.passenger_count = 0
		self.roster = []

	def next_frame(self):
		"""Increments the next frame in the execution loop"""
		self.frame += 1
		print( "Frame #:  {}".format(str(self.frame)))

	def is_frame(self, target_frame):
		"""Checks the target_frame against the current frame and returns true on a match"""
		if self.frame == target_frame:
			return True
		else:
			return False

	def add_passenger(self, start_floor, dest_floor):
		p = Passenger(self.floors[start_floor], dest_floor, self.passenger_count)
		self.floors[start_floor].waiting_room.append(p)
		self.roster.append(p)
		self.passenger_count += 1

	def step_elevatorbank(self):
		for e in self.elevator_bank:
			e.execute_state()
			e.set_direction()

	def step_passengers(self):
		for p in self.roster:
			p.check_location()

	def update_display(self):
		os.system('cls')
		w = 60
		for e in self.elevator_bank:
			print( "=" * w )
			print( "Elevator: {}".format(str(e.id_num)))
			print( "=" * w )
			print( "Floor:         {}".format(str(e.cur_floor)))
			print( "Doors:         {}".format(str(e.doors)))
			print( "State:         {}".format(e.state))
			print( "UP Queue:      {}".format(str(e.up_queue)))
			print( "DOWN Queue:    {}".format(str(e.down_queue)))
			print( "Direction:     {}".format(str(e.direction)))
			print( "=" * w )
		print( "Floor  #     UP  DOWN       Passengers Waiting")
		print( '-' * w)
		for f in self.floors:
			sys.stdout.write("fl.#   "+str(f.floor_number) + "  ")
			sys.stdout.write("[{down}/{up}] ".format(down=f.call_button_down, up=f.call_button_up))
			sys.stdout.write("waiting:" + "; ".join(["#"+str(p.sk) + " to "+str(p.dest_floor) for p in f.waiting_room]) +"\n")
			sys.stdout.write("-" * w +"\n")

	def run(self):
		while(True):
			self.step_elevatorbank()
			self.step_passengers()
			self.update_display()
			self.next_frame()
			time.sleep(1)

################ 
# Floor
################ 

class Floor(object):
	def __init__(self, floor_number):
		self.floor_number = floor_number
		self.call_button_up = False
		self.call_button_down = False
		self.waiting_room = []
		self.on_floor = []

################ 
# Passenger 
################ 

class Passenger(object):
	def __init__(self, location, dest_floor, sk):
		self.location = location
		self.dest_floor = dest_floor
		self.sk = sk

	def check_location(self):
		if type(self.location) is Elevator:
			pass
		elif type(self.location) is Floor:
			if self.has_destination():
				self.check_destination()

	def has_destination(self):
		if self.dest_floor is not None:
			return True
		elif self.dest_floor is None:
			return False

	def check_destination(self):
		if self.location.floor_number == self.dest_floor:
			self.dest_floor == None
		elif self.location.floor_number < self.dest_floor:
			self.location.call_button_up = True
		elif self.location.floor_number > self.dest_floor:
			self.location.call_button_down = True

################ 
# Main Function
################ 

def main():
	b = Building(0, 14, 1, 2)
	for i in range(0, 14, 5):
		b.elevator_bank[0].press_floor_button(i)
	for i in range(4, 14, 3):
		b.elevator_bank[1].press_floor_button(i)
	b.add_passenger(1, 0)
	b.add_passenger(0, 10)
	b.add_passenger(10, 0)
	b.add_passenger(5, 8)
	b.add_passenger(5, 3)
	b.update_display()
	time.sleep(1)
	b.run()

if __name__ == "__main__":
	main()