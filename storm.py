import curses
import random
import time
import sys

def main(stdscr):	

	curses.curs_set(0) # hide cursor
	stdscr.nodelay(1)
	stdscr.clear() # clear stdscr

	# init colors
	curses.start_color()
	curses.use_default_colors()
	for i in range(1, 256):
		curses.init_pair(i, i, curses.COLOR_BLACK)
	
	height, width = stdscr.getmaxyx()
	Drop.screen_height = height
	Drop.screen_width = width

	# create randomized char matrix for screen
	char_matrix = [] # [row][col]
	for row in range(height):
		char_matrix.append(generate_chars(width))

	drops = []
	
	# default settings
	colorscheme = "blue"
	speed = 0.075
	drop_count = width//10
	# if color given
	if (len(sys.argv) >= 2):
		colorscheme = sys.argv[1]
	# if drop_count given
	if (len(sys.argv) >= 3):
		drop_count = int(sys.argv[2])
	if (len(sys.argv) >= 4):
		speed = float(sys.argv[3])
	Drop.colorscheme = colorscheme

	spawn_drop = drop_count//2 # when to spawn new drop
	new_drop = drop_count//2 # when to spawn new drop
	while True:
		
		if (len(drops) < drop_count): # max number of drops
			if new_drop == spawn_drop:
				drops.append(Drop())
				new_drop = 0
			
		# update all drops
		for drop in drops:
			if (drop.y == height + 23):
				drop.reset()
			drop.update_drop(stdscr, char_matrix)
		stdscr.refresh()

		# delay
		key = stdscr.getch() # quit?
		time.sleep(speed)

		# move all drops
		for drop in drops:
			drop.y += 1

		if key == ord('q'):
			break

		new_drop += 1

	return


# generate random array of chars
def generate_chars(length):
	new_chars = []
	for i in range(length):
		random_int = random.randint(0x0020, 0x007E) # random char
		new_chars.append(chr(random_int))
	
	return new_chars



class Drop:
	
	screen_width = -1
	screen_height = -1
	colorscheme = ""

	# create now drop
	def __init__(self):
		self.y = 0
		self.x = random.randint(1, Drop.screen_width-2)
	
	# reset drop, randomize location, chars
	def reset(self):
		self.y = 0
		self.x = random.randint(1, Drop.screen_width-2)
	
	# print drop to stdscr
	def update_drop(self, stdscr, char_matrix):
		
		if (self.colorscheme == "blue"):
			#colors = [ 15, 45, 44, 39, 39, 38, 38, 38, 33, 33, 33, 27, 27, 27, 27, 27 ]
			
			# add new head
			if (self.y < Drop.screen_height and self.y >= 0): 
				stdscr.addch(self.y, self.x, char_matrix[self.y][self.x], curses.color_pair(15))
			
			# section 2 (45)
			if (self.y-1 < Drop.screen_height and self.y-1 >= 0): 
				stdscr.addch(self.y-1, self.x, char_matrix[self.y-1][self.x], curses.color_pair(45))
			
			# section 3
			if (self.y-3 < Drop.screen_height and self.y-3 >= 0): 
				stdscr.addch(self.y-3, self.x, char_matrix[self.y-3][self.x], curses.color_pair(33))
			
			# section 3
			if (self.y-7 < Drop.screen_height and self.y-7 >= 0): 
				stdscr.addch(self.y-7, self.x, char_matrix[self.y-7][self.x], curses.color_pair(27))
		
			# section 4
			if (self.y-15 < Drop.screen_height and self.y-15 >= 0): 
				stdscr.addch(self.y-15, self.x, char_matrix[self.y-15][self.x], curses.color_pair(20))
			
			# erase end of tail
			if (self.y-23 < Drop.screen_height and self.y-23 >= 0):
				stdscr.addch(self.y-23, self.x, char_matrix[self.y-23][self.x], curses.color_pair(16))
		


if __name__ == "__main__":
	curses.wrapper(main)
