import curses
import time
import random
import argparse

# Define the tortoise character
TORTOISE = "🐢"

# List of example tortoise names
NAMES = ["Angelo", "Giacomo", "SALSALSAL", "Ludo", "Arianna", "Matteo", "Giulia", "samuuu", "nonba","Mancini", "G B ", "Quaglia", "Giorgia", "Daniela", "Bea", "Anastasia", "Ivan", "Luca", "SERSE"]

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
            "name": NAMES[i % len(NAMES)] + f" {i+1}",  # Ensure unique names
            "x": 0,
            "y": 2 + i * 2,  # Start positions with spacing between tracks
            "speed": random.uniform(0.1, 0.5),
            #"speed": random.uniform(0.5, 1.5),
            "acceleration": random.uniform(-0.05, 0.05),
            "color": random.randint(1, num_colors),
        }
        for i in range(num_tortoises)
    ]

    # Step 1: Display static tortoises with "Choose your fighter!!" prompt
    for tortoise in tortoises:
        y = tortoise["y"]
        name_display = f"{tortoise['name']:<10}"
        stdscr.addstr(y, 0, name_display)  # Print tortoise name
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
    finish_line = width - 10  # Leave some space for visibility

    winner = None

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
            # Update speed with acceleration
            tortoise["speed"] = max(0.1, tortoise["speed"] + tortoise["acceleration"])

            # Randomly change acceleration
            if random.random() < 0.2:  # 20% chance per frame
                #tortoise["acceleration"] = random.uniform(-0.05, 0.05)
                tortoise["acceleration"] = random.uniform(-0.05, 0.02)

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

        # Control the frame rate
        #time.sleep(0.05)
        time.sleep(0.075)

    # Declare the winner
    stdscr.clear()
    if winner:
        stdscr.addstr(
            height // 2,
            width // 2 - len(winner["name"]) - 10,
            f"The winner is: {winner['name']}!",
            curses.A_BOLD,
        )
    else:
        stdscr.addstr(height // 2, width // 2 - 10, "Race interrupted!", curses.A_BOLD)
    stdscr.refresh()
    time.sleep(3)

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

