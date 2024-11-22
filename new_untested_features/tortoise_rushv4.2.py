import curses
import time
import random
import argparse
import csv
from datetime import datetime

# Define characters
TORTOISE = "🐢"
BOMB = "💣"
BOOM = "BOOOOOOM!"

# Tortoise names
NAMES = ["Angelo", "Giacomo", "SALSALSAL", "Ludo", "Arianna", "Matteo", "nonba","Mancini", "G B ", "Quaglia", "Dash", "Zoom", "Swift", "Blaze", "Thunder", "Rocket", "Comet", "SERSE"]

def save_results(results):
    """Save race results to a CSV file."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"race_results_{timestamp}.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Position", "Tortoise Name", "Exploded"])
        writer.writerows(results)
    print(f"Results saved to {filename}")

def main(stdscr, num_tortoises):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(False)  # Non-blocking input
    stdscr.clear()

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Gold
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Silver
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Bronze
    for i in range(4, 8):
        curses.init_pair(i, i, curses.COLOR_BLACK)

    # Terminal dimensions
    height, width = stdscr.getmaxyx()

    # Ensure enough vertical space for tortoises
    if height < num_tortoises + 5:
        raise ValueError("The terminal height is too small for the number of tortoises.")

    # Initialize tortoises
    tortoises = [
        {
            "name": NAMES[i % len(NAMES)] + f" {i+1}",
            "x": 0,
            "y": 2 + i * 2,
            "speed": random.uniform(0.1, 0.5),
            "acceleration": random.uniform(-0.05, 0.05),
            "color": random.randint(4, 7),
            "exploded": False,
            "bomb_x": None,
            "bomb_timer": None,
            "finished": False,
            "position": None
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

    # Race parameters
    finish_line = width - 10
    frame_counter = 0
    positions = []
    num_exploded = 0

    # Race loop
    while len(positions) < num_tortoises - num_exploded:
        stdscr.clear()

        # Draw the track
        for i in range(num_tortoises):
            stdscr.addstr(2 + i * 2, 0, "-" * width)
            stdscr.addstr(2 + i * 2 + 1, finish_line, "|")

        for tortoise in tortoises:
            if tortoise["finished"]: #or tortoise["exploded"]:
                # Show the tortoise's finish position
                if tortoise["position"] is not None:
                    stdscr.addstr(tortoise["y"], finish_line + 2, f"{tortoise['position']}!")
                continue

            # Bomb logic
            if random.random() < 0.0005 and tortoise["bomb_x"] is None:  # Reduced bomb probability
                tortoise["bomb_x"] = int(tortoise["x"]) + 12
                tortoise["bomb_timer"] = 3

            if tortoise["bomb_x"] is not None and tortoise["exploded"] == False:
                if frame_counter % 10 == 0 and tortoise["bomb_timer"] > 0:
                    tortoise["bomb_timer"] -= 1
                if tortoise["bomb_timer"] > 0:
                    #stdscr.addstr(tortoise["y"], tortoise["bomb_x"], BOMB)
                    #stdscr.addstr(tortoise["y"], tortoise["bomb_x"] + 2, f"{tortoise['bomb_timer']}")
                    stdscr.addstr(tortoise["y"], int(tortoise["x"]) + 10, BOMB)
                    stdscr.addstr(tortoise["y"], int(tortoise["x"]) + 8, f"{tortoise['bomb_timer']}")
                    tortoise["bomb_x"] = int(tortoise["x"])
                else:
                    stdscr.addstr(tortoise["y"], tortoise["bomb_x"], BOOM, curses.A_BOLD)
                    tortoise["exploded"] = True
                    num_exploded += 1
                    #tortoise["bomb_x"] = None
                    continue


            # Update tortoise position
            tortoise["speed"] = max(0.1, tortoise["speed"] + tortoise["acceleration"])

            # Randomly change acceleration
            if random.random() < 0.2:  # 20% chance per frame
                #tortoise["acceleration"] = random.uniform(-0.05, 0.05)
                tortoise["acceleration"] = random.uniform(-0.05, 0.02)

            # Update position
            tortoise["x"] += tortoise["speed"]

            # Check if the tortoise has reached the finish line
            if tortoise["x"] >= finish_line:
                tortoise["finished"] = True
                tortoise["position"] = len(positions) + 1
                positions.append((tortoise["position"], tortoise["name"], "Yes" if tortoise["exploded"] else "No"))

            # Draw the tortoise and its name
            x = int(tortoise["x"])
            y = tortoise["y"]
            color_pair = curses.color_pair(tortoise["color"])
            if tortoise["exploded"] == True:
                stdscr.addstr(tortoise["y"], tortoise["bomb_x"], BOOM, curses.A_BOLD)
            else:
                stdscr.addstr(y, 0, f"{tortoise['name']:<10}", color_pair)  # Print name
            try:
                stdscr.addstr(y, x + 12, TORTOISE, color_pair)  # Print tortoise
            except curses.error:
                pass  # Ignore out-of-bound errors

        # Refresh the screen to show updates
        stdscr.refresh()
        frame_counter += 1
        time.sleep(0.075)

    # Wait for 3 seconds before showing results
    time.sleep(3)
    stdscr.clear()

    # Display final results
    positions.sort(key=lambda x: x[0])
    stdscr.addstr(0, width // 2 - 10, "Final Results", curses.A_BOLD)
    for i, (pos, name, exploded) in enumerate(positions):
        color = curses.color_pair(1 if pos == 1 else 2 if pos == 2 else 3 if pos == 3 else 0)
        stdscr.addstr(2 + i, width // 2 - 15, f"{pos}. {name} {'(Exploded)' if exploded == 'Yes' else ''}", color)
    stdscr.refresh()

    # Save results to CSV
    save_results(positions)
    time.sleep(1)
    stdscr.getch()

# Command-line argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tortoise race animation!")
    parser.add_argument("--num_tortoises", type=int, default=5, help="Number of tortoises in the race (default: 5)")
    args = parser.parse_args()

    try:
        curses.wrapper(main, args.num_tortoises)
    except ValueError as e:
        print(str(e))

