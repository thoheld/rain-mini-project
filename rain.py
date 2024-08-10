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
	
	Drop.height, Drop.width = stdscr.getmaxyx()
	drops = []
	
	#buffer_win = curses.newwin(Drop.height, Drop.width)

	new_drop = 12
	while True:
		
		#buffer_win.clear()

		if (len(drops) < 16): # max of 16 drops
			if new_drop == 12:
				drops.append(Drop())
				new_drop = 0
			
		stdscr.clear()
		
		# print all drops
		for drop in drops:
			if (drop.y == Drop.height + 16):
				drop.reset()
			drop.print_drop(stdscr)
			#drop.print_drop(buffer_win)
		
		#stdscr.clear()
		stdscr.refresh()
		#buffer_win.refresh()

		# delay
		key = stdscr.getch() # quit?
		time.sleep(.3)

		# move all drops
		for drop in drops:
			drop.y += 1

		if key == ord('q'):
			break

		new_drop += 1

	return



class Drop:
	
	width = -1
	height = -1

	# create now drop
	def __init__(self):
		self.y = 0
		self.x = random.randint(1, Drop.width-2)
		self.chars = self.generate_chars(16)
	
	# reset drop, randomize location, chars
	def reset(self):
		self.y = 0
		self.x = random.randint(1, Drop.width-2)
		self.chars = self.generate_chars(16)
	
	# generate random chars
	def generate_chars(self, length):
		new_chars = []
		for i in range(length):
			random_int = random.randint(0x0020, 0x007E) # random unicode
			new_chars.append(chr(random_int))
		
		return new_chars
	
	# print drop to stdscr
	def print_drop(self, stdscr):
		colors = [ 15, 45, 44, 39, 39, 38, 38, 38, 33, 33, 33, 27, 27, 27, 27, 27 ]
		for i in range(0, len(self.chars)):
			if (self.y - i >= self.height or self.y-i < 0):
				continue
			stdscr.addch(self.y - i, self.x, self.chars[i], curses.color_pair(colors[i]))



if __name__ == "__main__":
	curses.wrapper(main)
