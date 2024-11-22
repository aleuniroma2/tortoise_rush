import curses
import time
import random
import argparse

# Define the tortoise character
TORTOISE = "🐢"
BOMB = "💣"
BOOM = "BOOOOOOM!"

# List of example tortoise names
NAMES = ["Angelo", "Giacomo", "Arianna", "Matteo", "Nonba", "Mancini", "G B", "Quaglia", "Dash", "Zoom"]

def main(stdscr, num_tortoises):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(False)  # Wait for user input
    stdscr.clear()

    # Initialize colors
    curses.start_color()
    num_colors = min(7, curses.COLORS - 1)
    for i in range(1, num_colors + 1):
        curses.init_pair(i, i, curses.COLOR_BLACK)

    # Terminal dimensions
    height, width = stdscr.getmaxyx()

    # Ensure enough vertical space for tortoises
    if height < num_tortoises + 5:
        raise ValueError("The terminal height is too small for the number of tortoises.")

    # Assign unique names and positions for the tortoises
    tortoises = [
        {
            "name": NAMES[i % len(NAMES)] + f" {i+1}",
            "x": 0,
            "y": 2 + i * 2,
            "speed": random.uniform(0.1, 0.5),
            "acceleration": random.uniform(-0.05, 0.05),
            "color": random.randint(1, num_colors),
            "exploded": False,  # Track if tortoise has exploded
            "bomb_x": None,  # Bomb position
            "bomb_timer": None  # Timer for bomb countdown
        }
        for i in range(num_tortoises)
    ]

    # Display static tortoises with "Choose your fighter!!" prompt
    for tortoise in tortoises:
        y = tortoise["y"]
        name_display = f"{tortoise['name']:<10}"
        stdscr.addstr(y, 0, name_display)  # Print tortoise name
        stdscr.addstr(y, 12, TORTOISE, curses.color_pair(tortoise["color"]))  # Print tortoise

    stdscr.addstr(height - 2, width // 2 - 10, "Choose your fighter!!", curses.A_BOLD)
    stdscr.addstr(height - 1, width // 2 - 15, "Press any key to start the race!", curses.A_BOLD)
    stdscr.refresh()

    # Wait for a keystroke to start the race
    stdscr.getch()

    # Display "READY, STEADY, GO!" sequence
    stdscr.clear()
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

    # Race parameters
    finish_line = width - 10
    winner = None
    frame_counter = 0  # Frame counter for time tracking

    # Start the race
    while not winner:
        # Clear the screen for the next frame
        stdscr.clear()

        # Draw the track
        for i in range(num_tortoises):
            stdscr.addstr(2 + i * 2, 0, "-" * width)  # Track line
            stdscr.addstr(2 + i * 2 + 1, finish_line, "|")  # Finish line

        # Update each tortoise
        for tortoise in tortoises:
            if tortoise["exploded"]:  # Skip exploded tortoises
                stdscr.addstr(tortoise["y"], tortoise["bomb_x"], BOOM, curses.A_BOLD)
                continue

            # Randomly place a bomb with a small chance
            if random.random() < 0.001 and tortoise["bomb_x"] is None:
                tortoise["bomb_x"] = int(tortoise["x"]) + 12
                tortoise["bomb_timer"] = 3  # Timer starts at 3 seconds

            # Handle bomb countdown
            if tortoise["bomb_x"] is not None:
                if frame_counter % 10 == 0 and tortoise["bomb_timer"] > 0:  # Decrease timer every second
                    tortoise["bomb_timer"] -= 1

                if tortoise["bomb_timer"] > 0:
                    # Display bomb and timer
                    stdscr.addstr(tortoise["y"], tortoise["bomb_x"], BOMB, curses.A_BOLD)
                    stdscr.addstr(tortoise["y"], tortoise["bomb_x"] + 2, f"{tortoise['bomb_timer']}")
                else:
                    # Bomb explodes
                    stdscr.addstr(tortoise["y"], tortoise["bomb_x"], BOOM, curses.A_BOLD)
                    tortoise["exploded"] = True
                    continue

            # Update tortoise speed and position
            tortoise["speed"] = max(0.1, tortoise["speed"] + tortoise["acceleration"])
            if random.random() < 0.2:  # Randomly adjust acceleration
                tortoise["acceleration"] = random.uniform(-0.05, 0.02)
            tortoise["x"] += tortoise["speed"]

            # Check if the tortoise has reached the finish line
            if tortoise["x"] >= finish_line:
                winner = tortoise
                break

            # Draw the tortoise
            x = int(tortoise["x"])
            y = tortoise["y"]
            color_pair = curses.color_pair(tortoise["color"])
            stdscr.addstr(y, 0, f"{tortoise['name']:<10}", color_pair)  # Print name
            stdscr.addstr(y, x + 12, TORTOISE, color_pair)  # Print tortoise

        # Refresh the screen
        stdscr.refresh()
        frame_counter += 1
        time.sleep(0.075)  # Control frame rate

    # Declare the winner
    stdscr.clear()
    if winner:
        stdscr.addstr(
            height // 2, 
            width // 2 - len(winner["name"]) - 10, 
            f"The winner is: {winner['name']}!", 
            curses.A_BOLD
            )
    else:
        stdscr.addstr(height // 2, width // 2 - 10, "All tortoises exploded! No winner.", curses.A_BOLD)
    stdscr.refresh()
    time.sleep(3)

# Command-line argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tortoise race animation!")
    parser.add_argument("--num_tortoises", type=int, default=5, help="Number of tortoises in the race (default: 5)")
    args = parser.parse_args()

    try:
        curses.wrapper(main, args.num_tortoises)
    except ValueError as e:
        print(str(e))

