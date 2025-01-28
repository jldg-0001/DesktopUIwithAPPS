from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import time
import random

class ParkingQueue:
    def __init__(self, root):
        self.queue = []  # Main queue for vehicles
        self.image_map = {}  # Map vehicle identifiers to images
        self.in_count = 0  # Counter for vehicles arriving
        self.out_count = 0  # Counter for vehicles departing

        # Set window dimensions
        window_width = 850
        window_height = 875
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        root.title("Parking Garage - Queue")
        root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Input frame
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=3)

        self.input_label = tk.Label(self.input_frame, text="Enter Vehicle:", font=("Press Start 2P", 6, "bold"))
        self.input_label.grid(row=0, column=0, padx=10)

        self.input_entry = tk.Entry(self.input_frame, width=30, bg="lightyellow", font=("Courier New", 8))
        self.input_entry.grid(row=0, column=1, padx=10)

        self.add_button = tk.Button(self.input_frame, text="Arrival", font=("Press Start 2P", 6, "bold"),
                                    fg="white", bg="green", command=self.add_to_queue)
        self.add_button.grid(row=0, column=2, padx=5)

        self.remove_button = tk.Button(self.input_frame, text="Departure", font=("Press Start 2P", 6, "bold"),
                                       fg="white", bg="red", command=self.remove_from_queue)
        self.remove_button.grid(row=0, column=3, padx=5)

        # Counter frame
        self.counter_frame = tk.Frame(root)
        self.counter_frame.pack(pady=3)

        self.in_label = tk.Label(self.counter_frame, text="Arrived: 0", font=("Press Start 2P", 6, "bold"), fg="green")
        self.in_label.grid(row=0, column=0, padx=20)

        self.out_label = tk.Label(self.counter_frame, text="Departed: 0", font=("Press Start 2P", 6, "bold"), fg="red")
        self.out_label.grid(row=0, column=1, padx=20)

        # Canvas for visualization
        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.pack(pady=3)

        self.background_image = self.load_and_resize_image("bgcanva.png", 800, 800)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw", tags="background")

        self.images = [
            self.load_and_resize_image(f"car{i}.png", 45) for i in range(1, 9)
        ]

        self.queue_x = 400
        self.queue_y_start = 700
        self.queue_y_offset = 60

    def load_and_resize_image(self, filepath, target_height):
        with Image.open(filepath) as img:
            original_width, original_height = img.size
            scale = target_height / original_height
            new_width = int(original_width * scale)
            resized_img = img.resize((new_width, target_height), Image.LANCZOS)
            return ImageTk.PhotoImage(resized_img)

    def add_to_queue(self):
        value = self.input_entry.get()

        if not value.strip():
            messagebox.showerror("Input Error", "Please enter a vehicle.")
            return

        if not value.isalnum():
            messagebox.showerror("Error", "Only letters and numbers are allowed.")
            return

        if len(self.queue) >= 10:
            messagebox.showerror("Error", "Parking Garage is full. Maximum 10 vehicles allowed.")
            return

        if value in self.queue:
            messagebox.showerror("Error", f"Vehicle {value} already exists in the parking garage.")
            return

        image = random.choice(self.images)
        self.image_map[value] = image
        self.queue.append(value)
        self.input_entry.delete(0, tk.END)

        self.in_count += 1
        self.in_label.config(text=f"Arrived: {self.in_count}")

        self.update_visualization()

    def remove_from_queue(self):
        if not self.queue:
            messagebox.showerror("Error", "Parking Garage is empty.")
            return

        departing_vehicle = self.queue.pop(0)

        self.out_count += 1
        self.out_label.config(text=f"Departed: {self.out_count}")

        del self.image_map[departing_vehicle]

        self.update_visualization()
        messagebox.showinfo("Departure", f"Vehicle {departing_vehicle} has left the parking garage.")

    def update_visualization(self):
        self.canvas.delete("vehicle")

        y = self.queue_y_start
        for value in self.queue:
            image = self.image_map[value]
            self.canvas.create_image(self.queue_x, y, image=image, tags="vehicle")
            y -= self.queue_y_offset

# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = ParkingQueue(root)
    root.mainloop()
