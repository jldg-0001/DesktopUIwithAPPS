import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from PIL import Image, ImageTk, ImageEnhance

# Base folder where all other folders are located
base_folder = os.path.dirname(os.path.abspath(__file__))

# Store running scripts and processes
running_scripts = {}
processes = []

def run_script(folder_name, script_name):
    """Run an external Python script with resources located in its own folder."""
    script_path = os.path.join(base_folder, folder_name, script_name)
    folder_path = os.path.join(base_folder, folder_name)

    if os.path.isfile(script_path):
        if script_name in running_scripts and running_scripts[script_name].poll() is None:
            messagebox.showinfo("Info", f"{script_name} is already running.")
        else:
            try:
                process = subprocess.Popen(['python', script_path], cwd=folder_path)
                processes.append(process)
                running_scripts[script_name] = process  # Track the running process
            except Exception as e:
                messagebox.showerror("Error", f"Could not run {script_name}: {e}")
    else:
        messagebox.showerror("Error", f"Script {script_name} not found at {script_path}!")

# Main window
root = tk.Tk()
root.attributes('-fullscreen', True)
root.title("Main Fullscreen GUI")

# Canvas for placing background image
canvas = tk.Canvas(root, bg="lightblue")
canvas.pack(fill=tk.BOTH, expand=True)

# Load the background image
bg_image_path = os.path.join(base_folder, 'background.png')
bg_image = Image.open(bg_image_path)
bg_image_resized = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
bg_image_tk = ImageTk.PhotoImage(bg_image_resized)
canvas.create_image(0, 0, image=bg_image_tk, anchor="nw")

# List of button images and corresponding script commands
buttons_info = [
    {'image': 'icon1.png', 'script_folder': 'Tic-tac-toe', 'script_name': 'tictactoe.py'},
    {'image': 'icon2.png', 'script_folder': 'Garage-Stacks', 'script_name': 'parkingstacks.py'},
    {'image': 'icon3.png', 'script_folder': 'folder3', 'script_name': 'script3.py'},
    {'image': 'icon4.png', 'script_folder': 'Binary-Traversal', 'script_name': 'binarytraversal.py'},
    {'image': 'icon5.png', 'script_folder': 'Binary-Search', 'script_name': 'binarysearch.py'},
    {'image': 'icon6.png', 'script_folder': 'Hanoi', 'script_name': 'hanoi.py'},
    {'image': 'icon7.png', 'script_folder': 'folder7', 'script_name': 'script7.py'},
]

# Function to create buttons dynamically
def create_button(image_path, folder_name, script_name, x, y):
    """Create a button with a fade effect on hover and link to a script."""
    img = Image.open(image_path)
    img_resized = img.resize((75, 75), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img_resized)

    # Create a faded version of the image
    faded_img = ImageEnhance.Brightness(img_resized).enhance(0.5)
    faded_img_tk = ImageTk.PhotoImage(faded_img)

    button = tk.Button(root, image=img_tk, command=lambda: run_script(folder_name, script_name), borderwidth=0)
    canvas.create_window(x, y, window=button)

    # Add hover effects to fade the button
    button.bind("<Enter>", lambda e: button.config(image=faded_img_tk))
    button.bind("<Leave>", lambda e: button.config(image=img_tk))

    # Store references to avoid garbage collection
    button.image = img_tk
    button.faded_image = faded_img_tk

# Create the buttons in a single column
x_position = 80
y_position = 80
spacing = 100

for button_info in buttons_info:
    create_button(
        os.path.join(base_folder, button_info['image']),
        button_info['script_folder'],
        button_info['script_name'],
        x_position,
        y_position
    )
    y_position += spacing

# Exit button with image
exit_img = Image.open(os.path.join(base_folder, 'shutdown.png'))
exit_img_resized = exit_img.resize((50, 50), Image.Resampling.LANCZOS)
exit_img_tk = ImageTk.PhotoImage(exit_img_resized)
exit_button = tk.Button(root, image=exit_img_tk, command=lambda: on_close(), borderwidth=0)
canvas.create_window(30, root.winfo_screenheight() - 84, window=exit_button)
exit_button.image = exit_img_tk

# Function to close all script windows when the main window is closed
def on_close():
    for process in processes:
        process.terminate()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
