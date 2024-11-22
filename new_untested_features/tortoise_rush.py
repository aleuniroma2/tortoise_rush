import curses
import time
import random

# Define the tortoise character (using emojis for fun, if your terminal supports it)
TORTOISE = "🐢"

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)  # Make getch() non-blocking
    stdscr.clear()

    # Terminal dimensions
    height, width = stdscr.getmaxyx()

    # Create tortoises with random speeds and positions
    num_tortoises = 5
    tortoises = [
        {"x": random.randint(0, width // 4), "y": random.randint(0, height - 1), "speed": random.uniform(0.1, 0.5)}
        for _ in range(num_tortoises)
    ]

    start_time = time.time()

    while True:
        # Clear the screen for the next frame
        stdscr.clear()

        # Update each tortoise's position
        for tortoise in tortoises:
            tortoise["x"] += tortoise["speed"]
            if tortoise["x"] > width:
                tortoise["x"] = 0  # Loop back to the start
            
            # Draw the tortoise at its new position
            x = int(tortoise["x"])
            y = tortoise["y"]
            stdscr.addstr(y, x, TORTOISE)

        # Refresh the screen to show updates
        stdscr.refresh()

        # Break the loop if a key is pressed
        if stdscr.getch() != -1:
            break

        # Control the frame rate
        time.sleep(0.1)

# Start the curses application
curses.wrapper(main)

