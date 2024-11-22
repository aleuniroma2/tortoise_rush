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
    stdscr.nodelay(True)  # Non-blocking input
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
            "speed": random.uniform(0.5, 1.5),
            "acceleration": random.uniform(-0.05, 0.05),
            "color": random.randint(1, num_colors),
            "exploded": False  # Tracks if the tortoise is out of the race
        }
        for i in range(num_tortoises)
    ]

    # Step 1: Display static tortoises with "Choose your fighter!!" prompt
    for tortoise in tortoises:
        y = tortoise["y"]
        stdscr.addstr(y, 0, f"{tortoise['name']:<10}")  # Print tortoise name
        stdscr.addstr(y, 12, TORTOISE, curses.color_pair(tortoise["color"]))  # Print tortoise
    
    stdscr.addstr(height - 2, width // 2 - 10, "Choose your fighter!!", curses.A_BOLD)
    stdscr.addstr(height - 1, width // 2 - 15, "Press any key to start the race!", curses.A_BOLD)
    stdscr.refresh()

    # Step 2: Wait for a keystroke to start the race
    stdscr.getch()

    # Step 3: Display "READY, STEADY, GO!" sequence
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

    # Define the finish line
    finish_line = width - 10

    winner = None
    bombs = {}  # Tracks bombs and their timers
    frame_counter = 0  # Track frames for bomb timer updates
    total_exploded = 0  # Track the number of exploded tortoises

    # Step 4: Start the race
    while not winner:
        # Clear the screen for the next frame
        stdscr.clear()

        # Draw the track
        for i in range(num_tortoises):
            stdscr.addstr(2 + i * 2, 0, "-" * width)  # Track line
            stdscr.addstr(2 + i * 2 + 1, finish_line, "|")  # Finish line

        # Update each tortoise
        for tortoise in tortoises:
            # Skip exploded tortoises
            if tortoise["exploded"]:
                total_exploded += 1
                continue

            # Randomly place a bomb with a small chance
            if random.random() < 0.02 and tortoise["name"] not in bombs:
                bombs[tortoise["name"]] = {"timer": 3, "x": int(tortoise["x"]) + 12}

            # Handle bomb countdown (1 second every 10 frames)
            if tortoise["name"] in bombs:
                bomb = bombs[tortoise["name"]]
                if frame_counter % 10 == 0 and bomb["timer"] > 0:  # Decrease every 1 second (10 frames)
                    bomb["timer"] -= 1

                if bomb["timer"] > 0:
                    stdscr.addstr(tortoise["y"], bomb["x"], BOMB, curses.A_BOLD)
                    stdscr.addstr(tortoise["y"], bomb["x"] + 2, f"{bomb['timer']}")
                else:
                    # Bomb explodes
                    stdscr.addstr(tortoise["y"], bomb["x"], BOOM, curses.A_BOLD)
                    tortoise["exploded"] = True
                    del bombs[tortoise["name"]]
                    continue

            # Update speed with acceleration
            tortoise["speed"] = max(0.1, tortoise["speed"] + tortoise["acceleration"])

            # Randomly change acceleration
            if random.random() < 0.1:
                tortoise["acceleration"] = random.uniform(-0.05, 0.05)

            # Update position
            tortoise["x"] += tortoise["speed"]

            # Check if the tortoise has reached the finish line
            if tortoise["x"] >= finish_line:
                winner = tortoise
                break

            # Draw the tortoise and its name
            x = int(tortoise["x"])
            y = tortoise["y"]
            color_pair = curses.color_pair(tortoise["color"])
            stdscr.addstr(y, 0, f"{tortoise['name']:<10}", color_pair)  # Print name
            try:
                stdscr.addstr(y, x + 12, TORTOISE, color_pair)  # Print tortoise
            except curses.error:
                pass  # Ignore out-of-bound errors

        # Refresh the screen to show updates
        stdscr.refresh()

        # Increment the frame counter
        frame_counter += 1

        # End the race if all tortoises have exploded
        if total_exploded == num_tortoises:
            winner = None
            break

        # Control the frame rate
        time.sleep(0.1)

    # Declare the winner or no winner if all exploded
    stdscr.clear()
    if winner:
        stdscr.addstr(
            height // 2,
            width // 2 - len(winner["name"]) - 10,
            f"The winner is: {winner['name']}!",
            curses.A_BOLD,
        )
    else:
        stdscr.addstr(height // 2, width // 2 - 10, "All tortoises exploded! No winner.", curses.A_BOLD)

    stdscr.refresh()
    time.sleep(2)

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

