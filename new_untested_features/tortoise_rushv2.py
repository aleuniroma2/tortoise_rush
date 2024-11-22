import curses
import time
import random
import argparse

# Define the tortoise character
TORTOISE = "🐢"

def main(stdscr, num_tortoises):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(False)  # Wait for user input during the "READY, STEADY, GO!" phase
    stdscr.clear()

    # Initialize colors
    curses.start_color()
    num_colors = min(7, curses.COLORS - 1)  # Limit to 7 colors for compatibility
    for i in range(1, num_colors + 1):
        curses.init_pair(i, i, curses.COLOR_BLACK)

    # Terminal dimensions
    height, width = stdscr.getmaxyx()

    # Ensure enough vertical space for tortoises
    if height < num_tortoises + 5:
        raise ValueError("The terminal height is too small for the number of tortoises.")

    # Display READY, STEADY, GO!
    stdscr.addstr(height // 2 - 2, width // 2 - 6, "READY!", curses.A_BOLD)
    stdscr.refresh()
    time.sleep(1)
    stdscr.addstr(height // 2 - 1, width // 2 - 7, "STEADY!", curses.A_BOLD)
    stdscr.refresh()
    time.sleep(1)
    stdscr.addstr(height // 2, width // 2 - 4, "GO!", curses.A_BOLD)
    stdscr.refresh()
    time.sleep(1)
    stdscr.clear()
    stdscr.refresh()

    # Create tortoises with random initial speeds and accelerations
    tortoises = [
        {
            "x": 0,  # All tortoises start at the leftmost position
            "y": i,  # Vertical position for each tortoise
            "speed": random.uniform(0.1, 0.5),
            "acceleration": random.uniform(-0.02, 0.02),
            "color": random.randint(1, num_colors),
        }
        for i in range(num_tortoises)
    ]

    stdscr.nodelay(True)  # Make getch() non-blocking for the race

    while True:
        # Clear the screen for the next frame
        stdscr.clear()

        # Update each tortoise's position
        for tortoise in tortoises:
            # Update speed with acceleration, and ensure speed stays positive
            tortoise["speed"] = max(0.1, tortoise["speed"] + tortoise["acceleration"])
            
            # Randomly change acceleration over time
            if random.random() < 0.1:  # 10% chance per frame to change acceleration
                tortoise["acceleration"] = random.uniform(-0.02, 0.02)

            # Update position based on speed
            tortoise["x"] += tortoise["speed"]

            # Draw the tortoise
            x = int(tortoise["x"])
            y = tortoise["y"]
            color_pair = curses.color_pair(tortoise["color"])
            try:
                stdscr.addstr(y, x % width, TORTOISE, color_pair)  # Wrap around the screen width
            except curses.error:
                pass  # Ignore out-of-bound drawing errors

        # Refresh the screen to show updates
        stdscr.refresh()

        # Break the loop if a key is pressed
        if stdscr.getch() != -1:
            break

        # Control the frame rate
        time.sleep(0.1)

# Command-line argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tortoise race animation!")
    parser.add_argument(
        "--num_tortoises", type=int, default=5, help="Number of tortoises in the race (default: 5)"
    )
    args = parser.parse_args()

    try:
        curses.wrapper(main, args.num_tortoises)
    except ValueError as e:
        print(str(e))

