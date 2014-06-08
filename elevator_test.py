from elevator import *

CMD_LIST = {
	
}

class ElevatorTest(object):
	def __init__(self, elevator):
		self.e = elevator

	"""Display functions"""

	def print_stats(self):
		"""prints object attributes"""
		attrs = vars(self.e)
		print "===Elevator STATS==="
		print ', \n'.join("%s: %s" % item for item in attrs.items())

	def print_floor_buttons(self):
		"""prints floor button values"""
		for i in range(self.e.min_floor, self.e.max_floor + 1):
			print "%s: %s" % (i, self.e.check_button(i))
			

m = Elevator(0, 10, 1, 1, True)
test = ElevatorTest(m)
test.print_stats()