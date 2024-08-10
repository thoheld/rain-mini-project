import curses
import random
import time

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
	
	new_drop = 7
	while True:
		
		if (len(drops) < 16): # max of 16 drops
			if new_drop == 7:
				drops.append(Drop())
				new_drop = 0
			
		# update all drops
		for drop in drops:
			if (drop.y == height + 17):
				drop.reset()
			drop.update_drop(stdscr, char_matrix)
		stdscr.refresh()

		# delay
		key = stdscr.getch() # quit?
		time.sleep(.05)

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
		#colors = [ 15, 45, 44, 39, 39, 38, 38, 38, 33, 33, 33, 27, 27, 27, 27, 27 ]
		
		# add new head
		if (self.y < Drop.screen_height and self.y >= 0): 
			stdscr.addch(self.y, self.x, char_matrix[self.y][self.x], curses.color_pair(15))
		# update last head
		if (self.y-1 < Drop.screen_height and self.y-1 >= 0): 
			stdscr.addch(self.y-1, self.x, char_matrix[self.y-1][self.x], curses.color_pair(45))
		# erase end of tail
		if (self.y-17 < Drop.screen_height and self.y-17 >= 0):
			stdscr.addch(self.y-17, self.x, char_matrix[self.y-17][self.x], curses.color_pair(16))
		


if __name__ == "__main__":
	curses.wrapper(main)
