import curses

def display_colors(stdscr):
	curses.start_color()
	curses.use_default_colors()

	# Initialize color pairs
	for i in range(1, 256):
		curses.init_pair(i, i, -1)  # -1 for default background color

	# Get terminal dimensions
	max_y, max_x = stdscr.getmaxyx()

	# Define the grid size
	cols = 8
	rows = 32

	# Ensure enough space is available
	if max_y < rows or max_x < cols * 8:
		stdscr.addstr(0, 0, "Terminal window is too small!")
		stdscr.refresh()
		stdscr.getch()
		return

	# Display colors in a grid (now in columns)
	for i in range(rows):
		for j in range(cols):
			color_index = j * rows + i + 1
			if color_index <= 256:
				# Display the color code and color
				stdscr.addstr(i, j * 8, f"{color_index:3}", curses.color_pair(color_index))

	stdscr.refresh()
	stdscr.getch()

curses.wrapper(display_colors)
