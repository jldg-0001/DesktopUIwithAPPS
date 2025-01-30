import tkinter as tk
import random
import time
from PIL import Image, ImageTk


class TowerOfHanoiApp:
    def __init__(self, master):
        self.master = master
        self.center_window(800, 600)  # Center the window
        self.master.title("Towers of Hanoi")
        self.master.resizable(False, False)  # Fixed window size

        # Load background images
        self.home_bg_image = Image.open("hanoibg.png")  # Home background
        self.home_bg_photo = ImageTk.PhotoImage(self.home_bg_image.resize((800, 600), Image.Resampling.LANCZOS))

        self.game_bg_image = Image.open("hanoisecondbg.png")  # Game background
        self.game_bg_photo = ImageTk.PhotoImage(self.game_bg_image.resize((800, 600), Image.Resampling.LANCZOS))

        # Set the initial background image
        self.bg_label = tk.Label(master, image=self.home_bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Add buttons for choosing sorted or unsorted disks
        self.selection_frame = tk.Frame(master, bg="#f9efd2")
        self.selection_frame.pack(side="bottom", pady=105)

        sorted_button = tk.Button(
            self.selection_frame,
            text="Sorted Disks",
            font=("Arial", 12),
            bg="#f89a2e",
            command=lambda: self.setup_disks(sorted_disks=True),
        )
        sorted_button.pack(side="left", padx=20)

        unsorted_button = tk.Button(
            self.selection_frame,
            text="Unsorted Disks",
            font=("Arial", 12),
            bg="#f89a2e",
            command=lambda: self.setup_disks(sorted_disks=False),
        )
        unsorted_button.pack(side="left", padx=20)

        # Buttons frame (hidden initially)
        self.buttons_frame = tk.Frame(self.master, bg="#fff2e7")
        self.buttons_frame.pack(side="bottom", pady=20)
        self.buttons_frame.pack_forget()  # Hide initially

        # Back button
        self.back_button = tk.Button(
            self.buttons_frame,
            text="Back",
            font=("Arial", 12),
            bg="#f89a2e",
            command=self.back_to_home,
        )
        self.back_button.pack(side="left", padx=50)

        # Solve button
        self.solve_button = tk.Button(
            self.buttons_frame,
            text="Solve",
            font=("Arial", 12),
            bg="#f89a2e",
            state="disabled",
            command=self.solve,
        )
        self.solve_button.pack(side="left", padx=50)

        # Redo button
        self.redo_button = tk.Button(
            self.buttons_frame,
            text="Redo",
            font=("Arial", 12),
            bg="#f89a2e",
            state="disabled",
            command=self.redo,
        )
        self.redo_button.pack(side="left", padx=50)

        # Status frame for moves and time
        self.status_frame = tk.Frame(master, bg="#fff2e7")
        self.moves_label = tk.Label(self.status_frame, text="Moves: 0", font=("Arial", 12), bg="#fff2e7")
        self.moves_label.pack(side="left", padx=50, pady=12)

        self.time_label = tk.Label(self.status_frame, text="Time: 0s", font=("Arial", 12), bg="#fff2e7")
        self.time_label.pack(side="right", padx=50, pady=12)

        # Initialize placeholders for canvas and game variables
        self.canvas = None
        self.poles = {0: [], 1: [], 2: []}
        self.disk_widths = [50, 100, 125, 150, 180]
        self.disk_height = 20
        self.disk_color = ["#f85525", "#1d98ba", "#7d9e3e", "#fec14a", "#01204e"]
        self.pole_positions = [200, 400, 600]
        self.moves = 0
        self.start_time = None
        self.timer_running = False

    def center_window(self, width, height):
        """Centers the Tkinter window on the screen."""
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def setup_disks(self, sorted_disks):
        """Sets up the disks based on user selection."""
        self.moves = 0
        self.start_time = None  # Reset the start time
        self.timer_running = False  # Stop any running timer
        self.update_status()

        num_disks = len(self.disk_widths)
        if sorted_disks:
            self.poles[0] = list(range(num_disks, 0, -1))
        else:
            self.poles[0] = random.sample(range(1, num_disks + 1), num_disks)

        self.poles[1], self.poles[2] = [], []

        # Change background image to game page background
        self.bg_label.config(image=self.game_bg_photo)

        # Create canvas if not already created
        if not self.canvas:
            self.canvas = tk.Canvas(self.master, highlightthickness=0, bg="#fff2e7")
            self.canvas.place(x=0, y=80, width=800, height=400)

        self.draw_poles_and_disks()
        self.selection_frame.pack_forget()  # Hide the selection frame after selection

        # Show buttons frame and enable buttons
        self.buttons_frame.pack(side="bottom", pady=20)
        self.solve_button.config(state="normal")
        self.redo_button.config(state="normal")
        self.redo_button.pack(side="right", padx=65, pady=12)
        self.back_button.config(state="normal")
        self.back_button.pack(side="right", padx=65, pady=12)


        # Show Status frame
        self.status_frame.pack(pady=(5, 0))

        # Generate the sequence of moves for solving the puzzle
        self.steps = []
        self.generate_hanoi_steps(len(self.poles[0]), 0, 2, 1)

    def update_time(self):
        """Periodically updates the time elapsed."""
        if self.timer_running and self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            self.time_label.config(text=f"Time: {elapsed_time}s")
            self.master.after(1000, self.update_time)

    def draw_poles_and_disks(self):
        """Draws poles and disks on the canvas."""
        self.canvas.delete("all")

        pole_base = 380  # Base position for poles
        pole_height = 100  # Top position for poles
        for x in self.pole_positions:
            self.canvas.create_line(x, pole_base, x, pole_height, width=5, fill="#472808")

        # Draw disks
        self.disks = {}
        for pole_index in range(3):
            self.disks[pole_index] = []
            for i, disk in enumerate(self.poles[pole_index]):
                width = self.disk_widths[disk - 1]
                disk_rect = self.canvas.create_rectangle(
                    self.pole_positions[pole_index] - width // 2,
                    pole_base - (i + 1) * self.disk_height,
                    self.pole_positions[pole_index] + width // 2,
                    pole_base - i * self.disk_height,
                    fill=self.disk_color[disk - 1],
                )
                self.disks[pole_index].append(disk_rect)

    def move_disk(self, from_pole, to_pole):
        """Moves a disk from one pole to another and animates it."""
        disk = self.poles[from_pole].pop()
        self.poles[to_pole].append(disk)

        disk_rect = self.disks[from_pole].pop()
        dx = self.pole_positions[to_pole] - self.pole_positions[from_pole]
        self.canvas.move(disk_rect, dx, 0)
        self.disks[to_pole].append(disk_rect)

        # Update disk position
        for i, disk in enumerate(self.poles[to_pole]):
            width = self.disk_widths[disk - 1]
            self.canvas.coords(
                self.disks[to_pole][i],
                self.pole_positions[to_pole] - width // 2,
                380 - (i + 1) * self.disk_height,
                self.pole_positions[to_pole] + width // 2,
                380 - i * self.disk_height,
            )
        self.master.update()

        # Update moves
        self.moves += 1
        self.update_status()

    def solve(self):
        """Starts solving the Tower of Hanoi with respect to sorted or unsorted starting order."""
        self.draw_poles_and_disks()

        # Start the timer
        self.start_time = time.time()
        self.timer_running = True
        self.update_time()

        # Solve in sorted order regardless of initial order
        self.hanoi(len(self.poles[0]), 0, 2, 1)

        # Stop the timer once solved
        self.timer_running = False

    def hanoi(self, n, from_pole, to_pole, aux_pole):
        """Solves the Tower of Hanoi while ensuring Pole 3 is sorted."""
        if n == 1:
            self.move_disk(from_pole, to_pole)  # Just move the disk normally
            time.sleep(0.5)
            return

        # Move n-1 disks to auxiliary pole
        self.hanoi(n - 1, from_pole, aux_pole, to_pole)

        # Move the nth (largest) disk to destination
        self.move_disk(from_pole, to_pole)
        time.sleep(0.5)

        # Move n-1 disks from auxiliary pole to destination
        self.hanoi(n - 1, aux_pole, to_pole, from_pole)

    def generate_hanoi_steps(self, n, from_pole, to_pole, aux_pole):
        """Generate the sequence of moves for solving the Tower of Hanoi."""
        if n == 1:
            self.steps.append((from_pole, to_pole))
            return
        self.generate_hanoi_steps(n - 1, from_pole, aux_pole, to_pole)
        self.steps.append((from_pole, to_pole))
        self.generate_hanoi_steps(n - 1, aux_pole, to_pole, from_pole)

    def update_status(self):
        """Updates the move counter."""
        self.moves_label.config(text=f"Moves: {self.moves}")

    def back_to_home(self):
        """Resets the game and brings the user back to the main page."""
        # Remove the canvas if it exists
        if self.canvas:
            self.canvas.destroy()
            self.canvas = None

        # Reset poles and moves
        self.poles = {0: [], 1: [], 2: []}
        self.moves = 0
        self.start_time = None  # Reset start time
        self.timer_running = False  # Stop the timer
        self.update_status()

        # Reset to home screen
        self.selection_frame.pack(side="bottom", pady=105)
        self.bg_label.config(image=self.home_bg_photo)
        self.buttons_frame.pack_forget()  # Hide the buttons frame
        self.status_frame.pack_forget()  # Hide the status frame

    def redo(self):
        """Repeats the action of solving the Tower of Hanoi."""
        self.poles[0] = list(range(5, 0, -1))
        self.poles[1], self.poles[2] = [], []
        self.moves = 0
        self.update_status()
        self.draw_poles_and_disks()
        self.hanoi(len(self.poles[0]), 0, 2, 1)


# Main window
root = tk.Tk()
app = TowerOfHanoiApp(root)
root.mainloop()
