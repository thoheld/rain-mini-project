import curses

def display_colors(stdscr):
	
	curses.start_color()
	curses.use_default_colors()

	# initialize color pairs
	for i in range(1, 256):
		curses.init_pair(i, i, -1)  # -1 for default background color

	# terminal dimensions
	height, width = stdscr.getmaxyx()

	x = 0
	y = 0
	for i in range(1, 257):
		if x*4 >= width-4:
			x = 0
			y += 1
		
		# Display the color code and color
		stdscr.addstr(y*2, x*4, str(i), curses.color_pair(i))
		x+=1

	stdscr.refresh()
	stdscr.getch()

curses.wrapper(display_colors)
