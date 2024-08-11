import curses
import random
import time
import sys
import math

def main(stdscr):	

	speed = .1
	# if speed given
	if (len(sys.argv) >= 2):
		speed = float(sys.argv[1])
	
	curses.curs_set(0) # hide cursor
	stdscr.nodelay(1)
	stdscr.clear() # clear stdscr

	# init colors
	curses.start_color()
	curses.use_default_colors()
	for i in range(1, 256):
		curses.init_pair(i, i, curses.COLOR_BLACK)
	
	height, width = stdscr.getmaxyx()
	Star.screen_height = height
	Star.screen_width = width
	Comet.screen_height = height
	Comet.screen_width = width
	Comet.screen_speed = speed
	
	# create randomized char matrix for screen
	char_matrix = [] # [row][col]
	for row in range(height):
		char_matrix.append(generate_chars(width))

	stars = []
	for i in range(1000):
		stars.append(Star())
	
	comet_chance = speed/6
	comet_chance_updated = comet_chance
	while True:
		for star in stars:
			star.update(stdscr)
	
		stdscr.refresh()	
		delay = 0
		if random.random() < comet_chance_updated:
			comet_chance_updated = comet_chance
			delay = Comet().animate(stdscr, char_matrix, stars)
		else:
			comet_chance_updated = comet_chance_updated + (speed/30)
		time.sleep(speed-delay)
	
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



class Star:
	
	screen_width = -1
	screen_height = -1

	# create new star
	def __init__(self):
		while True:
			# generate random point
			self.x = float(random.uniform((-1 * Star.screen_width), Star.screen_width))/2
			self.y = float(random.uniform((-1 * Star.screen_height), Star.screen_height))/2
			radius = math.sqrt((self.x*self.x) + (self.y*self.y))
			# check that point falls within circle
			if (radius <= Star.screen_height/2 and radius > Star.screen_height/3.2):
				break
		colors = [247, 247, 247, 247, 247, 247, 247, 101, 101, 101, 101, 23, 23]
		#colors = [15, 15, 15, 15, 15, 15, 15, 229, 229, 229, 229, 159, 159]
		self.color = colors[random.randint(0, 12)]
	
	
	# reset drop, randomize location, chars
	def reset(self):
		return
		# idk if i need this

	# print star to stdscr
	def update(self, stdscr):
		# erase
		converted_y = int((self.y * 6) + (2.9 * Star.screen_height))
		converted_x = int((self.x * 12) + (.5 * Star.screen_width))
		if ( (converted_y < Star.screen_height-1 and converted_y >= 1) and (converted_x < Star.screen_width-1 and converted_x >= 1) ):
			self.color_printer(stdscr, 16, converted_y, converted_x)
		# rotate
		radius = math.sqrt((self.x*self.x) + (self.y*self.y))
		angle = math.atan2(self.y, self.x)
		degrees = (math.degrees(angle) + 1) % 360
		angle = math.radians(degrees)
		self.y = radius * math.sin(angle)
		self.x = radius * math.cos(angle)
		# print
		converted_y = int((self.y * 6) + (2.9 * Star.screen_height))
		converted_x = int((self.x * 12) + (.5 * Star.screen_width))
		if ( (converted_y < Star.screen_height-1 and converted_y >= 1) and (converted_x < Star.screen_width-1 and converted_x >= 1) ):
			self.color_printer(stdscr, self.color, converted_y, converted_x)

	# print star with color
	def color_printer(self, stdscr, color, y, x):
		#converted_y = int((self.y * 6) + (2.9 * Star.screen_height))
		#converted_x = int((self.x * 12) + (.5 * Star.screen_width))
		#if ( (converted_y < Star.screen_height-1 and converted_y >= 1) and (converted_x < Star.screen_width-1 and converted_x >= 1) ): 
		stdscr.addch(y, x, "+", curses.color_pair(color))


class Comet:
	
	screen_width = -1
	screen_height = -1
	speed_screen = -1

	def __init__(self):
		# generate random point
		self.y = float(random.randint(1, Star.screen_height-1))
		self.x = float(random.randint(1, Star.screen_width-1))
		self.slope = random.uniform(-1,1)
		directions = [-1, 1]
		self.direction = directions[random.randint(0, 1)]
		self.length = random.randint(10, 30)
		self.speed = random.uniform(0.005, 0.025)
		color_options = []
		color_options.append([15, 15, 159, 14, 51, 16])
		color_options.append([15, 15, 195, 255, 253, 16])
		color_options.append([15, 229, 226, 219, 207, 16])
		color_options.append([15, 195, 193, 155, 46, 16])
		self.colors = color_options[random.randint(0, 0)]
	
	def update(self):
		self.y = self.y + (self.direction * math.sin(math.atan(self.slope * self.direction)))
		self.x = self.x + (self.direction * math.cos(math.atan(self.slope * self.direction)))

	def animate(self, stdscr, char_matrix, stars):
		total_time = 0.0
		for i in range(int(self.length + 30)):
			self.color_printer(stdscr, char_matrix, i)
			stdscr.refresh()
			time.sleep(self.speed)
			self.update()
			total_time = total_time + self.speed
			if total_time >= Comet.screen_speed:
				total_time = 0
				for star in stars:
					star.update(stdscr)
				stdscr.refresh()
		return total_time

	def color_printer(self, stdscr, char_matrix, iteration):
		
		# add new head
		y = self.y
		x = self.x
		if (y < Comet.screen_height-1 and y >= 1 and x < Comet.screen_width-1 and x >= 1 and iteration < self.length):
			stdscr.addch(round(y), round(x), char_matrix[round(y)][round(x)], curses.color_pair(self.colors[0]))
	
		# section 2
		for i in range(2):
			y = y - (self.direction * math.sin(math.atan(self.slope * self.direction)))
			x = x - (self.direction * math.cos(math.atan(self.slope * self.direction)))
		if (y < Comet.screen_height-1 and y >= 1 and x < Comet.screen_width-1 and x >= 1 and iteration - 2 < self.length):
			stdscr.addch(round(y), round(x), char_matrix[round(y)][round(x)], curses.color_pair(self.colors[1]))

		# section 3
		for i in range(4):
			y = y - (self.direction * math.sin(math.atan(self.slope * self.direction)))
			x = x - (self.direction * math.cos(math.atan(self.slope * self.direction)))
		if (y < Comet.screen_height-1 and y >= 1 and x < Comet.screen_width-1 and x >= 1 and iteration - 6 < self.length):
			stdscr.addch(round(y), round(x), char_matrix[round(y)][round(x)], curses.color_pair(self.colors[2]))

		# section 4
		for i in range(8):
			y = y - (self.direction * math.sin(math.atan(self.slope * self.direction)))
			x = x - (self.direction * math.cos(math.atan(self.slope * self.direction)))
		if (y < Comet.screen_height-1 and y >= 1 and x < Comet.screen_width-1 and x >= 1 and iteration - 14 < self.length):
			stdscr.addch(round(y), round(x), char_matrix[round(y)][round(x)], curses.color_pair(self.colors[3]))

		# section 5
		for i in range(16):
			y = y - (self.direction * math.sin(math.atan(self.slope * self.direction)))
			x = x - (self.direction * math.cos(math.atan(self.slope * self.direction)))
		if (y < Comet.screen_height-1 and y >= 1 and x < Comet.screen_width-1 and x >= 1):
			stdscr.addch(round(y), round(x), char_matrix[round(y)][round(x)], curses.color_pair(self.colors[4]))
		
		# clear
		if (y < Comet.screen_height-1 and y >= 1 and x < Comet.screen_width-1 and x >= 1):
			stdscr.addch(round(y), round(x), char_matrix[round(y)][round(x)], curses.color_pair(self.colors[5]))
		


if __name__ == "__main__":
	curses.wrapper(main)
