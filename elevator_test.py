from elevator import *

m = Elevator(0, 10, 1, 1, True)
l = [2, 5, 6, 10]
for floor in l:
	m.press_floor_button(floor)
m.print_floor_buttons()
m.run()
print m.get_highest_call()