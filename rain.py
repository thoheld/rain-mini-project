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
	drop_count = width//6
	# if color given
	if (len(sys.argv) >= 2):
		colorscheme = sys.argv[1]
	# if speed given
	if (len(sys.argv) >= 3):
		speed = float(sys.argv[2])
	# if drop_count given
	if (len(sys.argv) >= 4):
		drop_count = int(sys.argv[3])
	Drop.colorscheme = colorscheme

	new_drop = 14 # when to spawn new drop
	while True:
		
		if (len(drops) < drop_count): # max number of drops
			if (new_drop == 14):
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
		# change spaces to *
		if random_int == 32:
			random_int += 10
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
			self.color_printer(stdscr, char_matrix, [15, 45, 33, 27, 20, 16])
		
		elif (self.colorscheme == "red"):
			self.color_printer(stdscr, char_matrix, [15, 196, 160, 124, 52, 16])
		
		elif (self.colorscheme == "gina"):
			self.color_printer(stdscr, char_matrix, [15, 129, 92, 57, 237, 16])

		elif (self.colorscheme == "orange"):
			self.color_printer(stdscr, char_matrix, [15, 226, 214, 166, 9, 16])

		elif (self.colorscheme == "green"):
			self.color_printer(stdscr, char_matrix, [15, 46, 2, 34, 22, 16])
		
		elif (self.colorscheme == "grey" or self.colorscheme == "gray"):
			self.color_printer(stdscr, char_matrix, [15, 252, 245, 241, 237, 16])
		
		elif (self.colorscheme == "rainbow"):
			self.color_printer(stdscr, char_matrix, [196, 9, 226, 46, 21, 16])
		
		elif (self.colorscheme == "rose"):
			self.color_printer(stdscr, char_matrix, [15, 13, 201, 199, 89, 16])
		
		elif (self.colorscheme == "pinklemonade"):
			self.color_printer(stdscr, char_matrix, [15, 207, 219, 217, 220, 16])
		
		elif (self.colorscheme == "nebula"):
			self.color_printer(stdscr, char_matrix, [15, 49, 39, 63, 93, 16])
		
		elif (self.colorscheme == "dawn"):
			self.color_printer(stdscr, char_matrix, [15, 196, 199, 93, 21, 16])

	# print drop updates given a set of colors
	def color_printer(self, stdscr, char_matrix, colors):
		# add new head
		if (self.y < Drop.screen_height and self.y >= 0): 
			stdscr.addch(self.y, self.x, char_matrix[self.y][self.x], curses.color_pair(colors[0]))
		# section 2
		if (self.y-1 < Drop.screen_height and self.y-1 >= 0): 
			stdscr.addch(self.y-1, self.x, char_matrix[self.y-1][self.x], curses.color_pair(colors[1]))
		# section 3
		if (self.y-3 < Drop.screen_height and self.y-3 >= 0): 
			stdscr.addch(self.y-3, self.x, char_matrix[self.y-3][self.x], curses.color_pair(colors[2]))
		# section 3
		if (self.y-7 < Drop.screen_height and self.y-7 >= 0): 
			stdscr.addch(self.y-7, self.x, char_matrix[self.y-7][self.x], curses.color_pair(colors[3]))
		# section 4
		if (self.y-15 < Drop.screen_height and self.y-15 >= 0): 
			stdscr.addch(self.y-15, self.x, char_matrix[self.y-15][self.x], curses.color_pair(colors[4]))
		# erase end of tail
		if (self.y-23 < Drop.screen_height and self.y-23 >= 0):
			stdscr.addch(self.y-23, self.x, char_matrix[self.y-23][self.x], curses.color_pair(colors[5]))


if __name__ == "__main__":
	curses.wrapper(main)
