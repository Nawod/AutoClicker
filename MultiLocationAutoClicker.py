import pyautogui
import keyboard
import time
import tkinter as tk
from tkinter import messagebox
import threading
import webbrowser

# Initialize variables
locations = []  # To store coordinates
auto_clicking_active = False  # To track if auto-clicking is active
coordinate_count = 2 
click_delay = 0.5


def select_coordinates():
    """Allow the user to select coordinates on the screen based on user input."""    
    global locations, auto_clicking_active, coordinate_count
    locations = []  # Clear previous coordinates

    # Stop any active clicking
    auto_clicking_active = False
    time.sleep(0.5)  # Small delay to avoid misclicks

    messagebox.showinfo("Selection Mode", f"Click on {coordinate_count} locations to select coordinates.\n Press 'p + c' to confirm each coordinate.")

    while len(locations) < coordinate_count:
        if keyboard.is_pressed("p") and keyboard.is_pressed("c"):
            x, y = pyautogui.position()
            locations.append((x, y))
            if len(locations) != coordinate_count:
                messagebox.showinfo("Location Selected", f"Selected: {x}, {y}")
            time.sleep(0.5)  # Avoid double capturing

    messagebox.showinfo("Coordinates Selected", f"Coordinates selected: {locations} \n Press 'p + r' to begin.")


def auto_click():
    """Loop to auto-click at the selected coordinates."""    
    global auto_clicking_active
    if len(locations) < coordinate_count:
        messagebox.showerror("Error", "You must select enough coordinates first!")
        return

    messagebox.showinfo("Auto-Clicking", "Starting auto-clicking. \nPress 'Esc' to stop.")

    while auto_clicking_active:
        for x, y in locations:
            if not auto_clicking_active:  # Check if the loop should stop
                print("Auto-clicking stopped.")
                return
            pyautogui.click(x, y)
            time.sleep(click_delay)  


def start_auto_clicking():
    """Start the auto-clicking process from the GUI."""    
    global auto_clicking_active
    if not auto_clicking_active:
        auto_clicking_active = True
        threading.Thread(target=auto_click, daemon=True).start()


def stop_auto_clicking():
    """Stop the auto-clicking process."""    
    global auto_clicking_active
    auto_clicking_active = False
    messagebox.showinfo("Auto-Clicking Stopped", "Auto-clicking stopped.")


def on_exit():
    """Exit the program."""    
    root.quit()


def keyboard_listener():
    """Listen for keyboard events to trigger actions."""    
    global auto_clicking_active

    while True:
        if keyboard.is_pressed("p") and keyboard.is_pressed("s"):
            select_coordinates()

        if keyboard.is_pressed("p") and keyboard.is_pressed("r"):
            if not auto_clicking_active:
                start_auto_clicking()

        if keyboard.is_pressed("esc"):
            if auto_clicking_active:
                stop_auto_clicking()
            else:
                print("Exiting the program.")
                root.quit()
                break

        time.sleep(0.1)  # To prevent high CPU usage

#Update the coordinate count based on user input
def update_coordinate_count(): 
    global coordinate_count
    try:
        coordinate_count = int(coordinate_count_entry.get())
        messagebox.showinfo("Updated Count", f"Coordinate count updated to {coordinate_count}.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")

#update click delay
def update_click_delay():   
    global click_delay
    try:
        click_delay = float(delay_count_entry.get())
        messagebox.showinfo("Updated Click Delay", f"Click Delay time updated to {click_delay}.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")

#open website
def open_link(event):
    webbrowser.open("https://www.nawodmadhuwantha.com")


# Set up the tkinter window
root = tk.Tk()
root.title("Multi Location Auto Clicker")
root.geometry("450x620")

# Instructions label
instructions_title = tk.Label(root, text="Instructions", font=("Arial", 16, "bold"), anchor="center")
instructions_title.pack(pady=(15, 0))

instructions_label = tk.Label(root, text="Press 'p + s' to select coordinates.\n\n'p + c' to confirm the coordinates.\n\n'p + r' to run auto-clicking.\n\n'Esc' to stop auto-clicking.", font=("Arial", 12))
instructions_label.pack(pady=10)

# Input box for the number of coordinates
coordinate_count_label = tk.Label(root, text="Enter the number of coordinates to select:")
coordinate_count_label.pack(pady=(25,5))

coordinate_count_frame = tk.Frame(root)
coordinate_count_frame.pack(pady=10)

coordinate_count_entry = tk.Entry(coordinate_count_frame)
coordinate_count_entry.insert(0, "2")
coordinate_count_entry.pack(side="left", padx=5)

update_button = tk.Button(coordinate_count_frame, text="Update", command=update_coordinate_count)
update_button.pack(side="left")

# Input box for the click delay time
delay_count_label = tk.Label(root, text="Enter the delay time between clicks:")
delay_count_label.pack(pady=(15,5))

delay_count_frame = tk.Frame(root)
delay_count_frame.pack(pady=10)

delay_count_entry = tk.Entry(delay_count_frame)
delay_count_entry.insert(0, "0.5")
delay_count_entry.pack(side="left", padx=5)

delay_update_button = tk.Button(delay_count_frame, text="Update", command=update_click_delay)
delay_update_button.pack(side="left")

# Select Coordinates Button
select_button = tk.Button(root, text="Select Coordinates", command=select_coordinates)
select_button.pack(pady=(15,10))

# Start Auto-clicking Button
start_button = tk.Button(root, text="Start Auto-Clicking", command=start_auto_clicking)
start_button.pack(pady=10)

# Create the clickable label
copyright_label = tk.Label(
    root,
    text="©️Nawod Madhuwantha",
    fg="blue",          # Blue text to resemble a hyperlink
    cursor="hand2"      # Change cursor to a hand when hovered
)
copyright_label.pack(pady=(5, 10))

# Bind the label to open the link on click
copyright_label.bind("<Button-1>", open_link)


# Run the tkinter event loop in a separate thread to allow for keyboard listening
keyboard_thread = threading.Thread(target=keyboard_listener, daemon=True)
keyboard_thread.start()

# Run the tkinter event loop
root.mainloop()
