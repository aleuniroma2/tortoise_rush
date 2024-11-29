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
            "name": NAMES[i % len(NAMES)],  # Ensure unique names
            "x": 0,
            "y": 2 + i * 2,  # Start positions with spacing between tracks
            "speed": 0.1, #random.uniform(0.1, 0.2),
            "acceleration": 0, #random.uniform(-0.05, 0.05),
            "color": random.randint(1, num_colors),
            "finished": False,  # Track if the tortoise has finished the race
            "dispayed": False,
            "numberedfinished": 0
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

    finished_tortoises = []
    first_finish_time = None

    # Step 4: Start the race
    while len(finished_tortoises) < num_tortoises:
        # Clear the screen for the next frame
        stdscr.clear()

        # Draw the track
        for i in range(num_tortoises):
            stdscr.addstr(2 + i * 2, 0, "-" * width)  # Track line
            stdscr.addstr(2 + i * 2 + 1, finish_line, "|")  # Finish line

        # Update each tortoise
        for tortoise in tortoises:
            if tortoise["finished"]:
                y = tortoise["y"]
                color_pair = curses.color_pair(tortoise["color"])
                stdscr.addstr(y, 0, f"{tortoise['name']:<10}", color_pair)  # Print name
                if tortoise["dispayed"] == False:
                    stdscr.addstr(y, finish_line, f"{len(finished_tortoises) }" +" " + f"{tortoise['name']:<5}", curses.A_BOLD)  # Print position in white
                    tortoise["dispayed"] = True
                    tortoise["numberedfinished"] = len(finished_tortoises) 
                else:
                    stdscr.addstr(y, finish_line, f"{tortoise['numberedfinished']}" +" " + f"{tortoise['name']:<5}", curses.A_BOLD)
                continue

            # Update speed with acceleration
            tortoise["speed"] = max(0, tortoise["speed"] + tortoise["acceleration"])

            # Randomly change acceleration
            if random.random() < 0.2:  # 20% chance per frame
                tortoise["acceleration"] = random.uniform(-0.05, 0.025)

            # Update position
            tortoise["x"] += tortoise["speed"]

            # Check if the tortoise has reached the finish line
            if tortoise["x"] >= finish_line:
                tortoise["finished"] = True
                finished_tortoises.append(tortoise)
                if first_finish_time is None:
                    first_finish_time = time.time()
                continue

            # Draw the tortoise and its name
            x = int(tortoise["x"])
            y = tortoise["y"]
            color_pair = curses.color_pair(tortoise["color"])
            stdscr.addstr(y, 0, f"{tortoise['name']:<10}", color_pair)  # Print name
            try:
                stdscr.addstr(y, x + 12, TORTOISE, color_pair)  # Print tortoise
            except curses.error:
                pass  # Ignore out-of-bound errors

        # Display the timeout timer
        if first_finish_time:
            elapsed_time = time.time() - first_finish_time
            remaining_time = max(0, 60 - elapsed_time)
            stdscr.addstr(0, width // 2 - 10, f"Time left: {remaining_time:.2f} seconds", curses.A_BOLD)

        # Refresh the screen to show updates
        stdscr.refresh()

        # Control the frame rate
        time.sleep(0.075)

        # Check for timeout
        if first_finish_time and time.time() - first_finish_time >= 60:
            break

    # Mark remaining tortoises as not finished
    for tortoise in tortoises:
        if not tortoise["finished"]:
            tortoise["finished"] = True
            finished_tortoises.append(tortoise)

    # Declare the results
    stdscr.clear()
    stdscr.addstr(height // 2 - len(finished_tortoises) // 2 - 6, width // 2 - 10, "Race Results:", curses.A_BOLD)

    # Podium heights
    podium_heights = [10, 7, 5]

    # Draw podium
    base_width = width // 8
    spacing = 2  # Spacing between columns
    center_x =8 + width // 2 - base_width - spacing  # Shift the podium to the left
    base_y = height // 2 + max(podium_heights) // 2

    # Define colors for the podium
    GOLD = 3
    SILVER = 7
    BRONZE = 6

    positions = [
        {"label": "2°", "x_offset": -(base_width + spacing), "height": podium_heights[1], "color": SILVER, "name": finished_tortoises[1]['name'] if len(finished_tortoises) > 1 else ""},
        {"label": "1°", "x_offset": 0, "height": podium_heights[0], "color": GOLD, "name": finished_tortoises[0]['name'] if len(finished_tortoises) > 0 else ""},
        {"label": "3°", "x_offset": base_width + spacing, "height": podium_heights[2], "color": BRONZE, "name": finished_tortoises[2]['name'] if len(finished_tortoises) > 2 else ""},
    ]

    # Draw each podium column
    for pos in positions:
        col_x = center_x + pos["x_offset"]
        col_y = base_y - pos["height"]

        for row in range(pos["height"]):
            for col in range(base_width):
                stdscr.addch(col_y + row, col_x + col, " ", curses.color_pair(pos["color"]) | curses.A_REVERSE)

        stdscr.addstr(col_y - 1, col_x + base_width // 2 - len(pos["label"]) // 2, pos["label"], curses.A_BOLD)
        if pos["name"]:
            stdscr.addstr(col_y - 2, col_x + base_width // 2 - len(pos["name"]) // 2, pos["name"], curses.A_BOLD)

    # Title

    # Display the rest of the results
    for idx, tortoise in enumerate(finished_tortoises[3:]):
        stdscr.addstr(base_y + idx + 1, width // 2 - 10, f"{idx + 4}. {tortoise['name']}", curses.A_BOLD)

    stdscr.refresh()
    stdscr.getch()

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