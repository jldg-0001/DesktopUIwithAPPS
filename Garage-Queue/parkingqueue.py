from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import time
import random


class ParkingQueue:
    def __init__(self, root):
        self.queue1 = []  # Main queue for vehicles
        self.queue2 = []
        self.image_map = {}  # Map vehicle identifiers to images
        self.in_count = 0  # Counter for vehicles arriving
        self.out_count = 0  # Counter for vehicles departing
        self.animation_in_progress = False

        # Set window dimensions
        window_width = 850
        window_height = 875
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        root.title("Parking Garage - Queue")
        root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Set Main Window Icon
        main_icon = Image.open("iconcar.ico")  # Replace with your .ico file
        root.iconphoto(True, ImageTk.PhotoImage(main_icon))

        # Input frame
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=3)

        self.input_label = tk.Label(self.input_frame, text="Enter Vehicle:", font=("Press Start 2P", 6, "bold"))
        self.input_label.grid(row=0, column=0, padx=10)

        self.input_entry = tk.Entry(self.input_frame, width=30, bg="lightyellow", font=("Courier New", 8))
        self.input_entry.grid(row=0, column=1, padx=10)

        self.add_button = tk.Button(self.input_frame, text="Arrival", font=("Press Start 2P", 6, "bold"),
                                    fg="white", bg="green", command=self.add_to_queue1)
        self.add_button.grid(row=0, column=2, padx=5)

        self.remove_button = tk.Button(self.input_frame, text="Departure", font=("Press Start 2P", 6, "bold"),
                                       fg="white", bg="red", command=self.remove_from_queue1)
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

        self.background_image = self.load_and_resize_image("bgcanvaq.png", 803)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw", tags="background")

        self.images = [
            self.load_and_resize_image(f"car{i}.png", 45) for i in range(1, 9)
        ]

        # Load and resize rectangle images for Queue 1 and Queue 2
        self.queue1_rect_image = self.load_and_resize_image("entext.png", 110)

        self.queue1_x = 400
        self.text_x = 225
        self.queue_y_start = 700
        self.queue_y_offset = 60
        self.rectangle_y = 20

        # Add a black rectangle at the topmost part of the canvas, aligned with stack 1
        self.topmost_rect_queue1 = self.canvas.create_rectangle(
            self.queue1_x - 50,  # Left side of the rectangle
            0,  # Top side of the rectangle (very top of the canvas)
            self.queue1_x + 50,  # Right side of the rectangle
            25,  # Bottom side (just below the top part of the canvas)
            fill="black",  # Black color for the rectangle
            tags="queue_rect"  # Same tag as the other stack rectangles for layering
        )

        # Add a black rectangle at the topmost part of the canvas, aligned with stack 2
        self.topmost_rect_queue2 = self.canvas.create_rectangle(
            self.queue1_x - 50,  # Left side of the rectangle, aligned with stack 2
            760,  # Top side of the rectangle (same as stack 1, very top of the canvas)
            self.queue1_x + 50,  # Right side of the rectangle
            800,  # Bottom side (same position as stack 1)
            fill="black",  # Black color for the rectangle
            tags="queue_rect"  # Same tag as the other stack rectangles for layering
        )

        # If you need the rectangles to always be on the topmost layer:
        self.canvas.tag_raise(self.topmost_rect_queue1)
        self.canvas.tag_raise(self.topmost_rect_queue2)

        # Add rectangle objects to canvas with tags
        self.queue1_rect = self.canvas.create_image(self.queue1_x, self.rectangle_y + 100, image=self.queue1_rect_image,
                                                    anchor="s", tags="queue_rect")

        # Draw labels for the stacks (always on top of the vehicles)
        self.canvas.create_text(self.text_x, self.queue_y_start + 80, text="Parking Garage",
                                font=("Press Start 2P", 10, "bold"), fill="white", tags="queue")

        # Load and resize the image for the exit button
        self.exit_icon = self.load_and_resize_image("exiticon.png", 35)  # Adjust size as needed

        # Exit Button with image
        self.exit_button = tk.Button(root, image=self.exit_icon, command=root.quit, borderwidth=0, bg="white")
        self.exit_button.place(x=789, y=10)

    def load_and_resize_image(self, filepath, target_height):
        with Image.open(filepath) as img:
            original_width, original_height = img.size
            scale = target_height / original_height
            new_width = int(original_width * scale)
            resized_img = img.resize((new_width, target_height), Image.LANCZOS)
            return ImageTk.PhotoImage(resized_img)

    def disable_entry_with_message(self, message="Processing..."):
        """Disable the entry and display a message."""
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, message)
        self.input_entry.config(state="disabled", disabledforeground="gray", disabledbackground="lightgray")

    def enable_entry(self):
        """Re-enable the entry and clear the message."""
        self.input_entry.config(state="normal")
        self.input_entry.delete(0, tk.END)
        self.input_entry.config(disabledforeground="black", disabledbackground="white")

    def update_visualization1(self):
        """Update the canvas visualization of stacks without clearing the background."""
        # Redraw only the stack images and vehicle images, without clearing the background
        # Ensure the background is at the bottom (and doesn't get deleted)

        # No need to delete the entire canvas, just clear and redraw the vehicles and stacks
        self.canvas.delete("queue")  # Remove only stack-related images
        self.canvas.delete("vehicle")  # Remove only vehicle images

        # Redraw the background (only once)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw", tags="background")

        # Draw Stack 1
        y = self.queue_y_start
        for value in self.queue1:
            self._draw_image(self.queue1_x, y, value)
            y -= self.queue_y_offset


        # Redraw rectangle images for the stacks (always on top of the vehicles)
        self.queue1_rect = self.canvas.create_image(self.queue1_x, self.rectangle_y + 100,
                                                    image=self.queue1_rect_image, anchor="s", tags="queue")

        # Draw labels for the stacks (always on top of the vehicles)
        self.canvas.create_text(self.text_x, self.queue_y_start + 80, text="Parking Garage",
                                font=("Press Start 2P", 10, "bold"), fill="white", tags="text")

        # Send the background to the back
        self.canvas.tag_lower("background")

    def animate_image(self, x, start_y, end_y, image, direction="down"):
        """Animate an image moving from start_y to end_y, ensuring no duplicate vehicles overlap."""
        # Create the vehicle image with a unique tag
        img = self.canvas.create_image(x, start_y, image=image, tags="vehicle")

        # Ensure the initial layering is correct
        self.canvas.tag_lower("background")  # Background always at the bottom
        self.canvas.tag_raise("vehicle")  # Vehicles should be above the background
        self.canvas.tag_raise("queue_rect")  # Stack rectangles at the top

        # Animation loop
        y = start_y
        step = -5 if direction == "up" else 5

        while (direction == "down" and y < end_y) or (direction == "up" and y > end_y):
            # Before moving the new vehicle, delete any overlapping vehicles from previous frames
            self.delete_overlapping(x, y, img)

            # Move the current image
            self.canvas.move(img, 0, step)
            self.canvas.update()

            # Ensure the layering is preserved
            self.canvas.tag_lower("background")
            self.canvas.tag_raise("vehicle")
            self.canvas.tag_raise("queue_rect")

            y += step
            time.sleep(0.02)  # Pause for smooth animation

        # Ensure the final position is correct
        self.canvas.move(img, 0, end_y - y)
        self.canvas.tag_lower("background")
        self.canvas.tag_raise("vehicle")
        self.canvas.tag_raise("queue_rect")

    def update_visualization2(self):
        """Update the canvas visualization of stacks without clearing the background."""
        # Remove previous vehicles and labels
        self.canvas.delete("vehicle")  # Remove vehicle images
        self.canvas.delete("label")  # Remove vehicle labels

        # Draw Stack 1 with labels
        y = self.queue_y_start
        for value in self.queue1:
            self._draw_image(self.queue1_x, y, value)
            y -= self.queue_y_offset

        # Redraw rectangles and labels for stacks
        self.queue1_rect = self.canvas.create_image(self.queue1_x, self.rectangle_y + 100,
                                                    image=self.queue1_rect_image, anchor="s", tags="queue")
        self.canvas.create_text(self.text_x, self.queue_y_start + 80, text="Parking Garage",
                                font=("Press Start 2P", 10, "bold"), fill="white", tags="queue")

        # Ensure background stays at the bottom
        self.canvas.tag_lower("background")

    def delete_overlapping(self, x, y, current_img):
        """Delete only vehicle images that overlap, keeping the background and rectangles intact."""
        # Find all items overlapping the given coordinates (x, y)
        overlapping_items = self.canvas.find_overlapping(x - 25, y - 25, x + 25, y + 25)

        for item in overlapping_items:
            # Only delete items that are vehicles and are not the current vehicle
            if "vehicle" in self.canvas.gettags(item) and item != current_img:
                self.canvas.delete(item)

    def _draw_image(self, x, y, value):
        """Draw an image and a customized label associated with the given value."""
        # Remove old rectangles and labels for this value if they exist
        self.canvas.delete(f"label_bg_{value}")
        self.canvas.delete(f"label_{value}")

        # Draw the vehicle image
        image = self.image_map.get(value)
        if image:
            self.canvas.create_image(x, y, image=image, tags=(f"vehicle_{value}", "vehicle"))

        # Define label text and style
        label_text = value
        font_size = 10  # Font size for label
        font = ("Courier New", font_size, "bold")
        label_padding = 5  # Padding around the text
        extra_spacing = 20  # Additional space between the rectangle and the vehicle image
        fill_color = "#FFF2CC"  # Label background color
        border_color = "#000000"  # Label border color

        # Measure text width and height dynamically
        text_id = self.canvas.create_text(0, 0, text=label_text, font=font, anchor="nw")
        bbox = self.canvas.bbox(text_id)  # Get the bounding box of the text
        self.canvas.delete(text_id)  # Remove temporary text object
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate label rectangle dimensions based on text size and padding
        rect_x1 = x - text_width - 2 * label_padding - extra_spacing  # Move rectangle to the left
        rect_x2 = x - extra_spacing  # Adjust the right edge accordingly
        rect_y1 = y - text_height // 2 - label_padding
        rect_y2 = rect_y1 + text_height + 2 * label_padding

        # Draw the label background (rectangle)
        self.canvas.create_rectangle(
            rect_x1,
            rect_y1,
            rect_x2,
            rect_y2,
            fill=fill_color,
            outline=border_color,
            tags=(f"label_bg_{value}", "label_bg"),
        )

        # Draw the label text, aligned to the right within the rectangle
        self.canvas.create_text(
            rect_x2 - label_padding,  # Position text at the right edge of the rectangle
            (rect_y1 + rect_y2) / 2,  # Vertically center the text
            text=label_text,
            font=font,
            fill="black",
            anchor="e",  # Align text to the right within the rectangle
            tags=(f"label_{value}", "label"),
        )

    def set_layering(self):
        """Ensure permanent layering: background at bottom, vehicles/text in the middle, rectangles on top."""
        self.canvas.tag_lower("background")  # Background always at the bottom
        self.canvas.tag_raise("vehicle")  # Vehicles above the background
        self.canvas.tag_raise("text")  # Text above vehicles
        self.canvas.tag_raise("queue_rect")  # Rectangles always on top

    def add_to_queue1(self):
        value = self.input_entry.get()

        if not value.strip():
            messagebox.showerror("Input Error", "Please enter a vehicle.")
            return

        if not value.isalnum():
            messagebox.showerror("Error", "Only letters and numbers are allowed.")
            return

        if len(self.queue1) >= 10:
            messagebox.showerror("Error", "Parking Garage is full. Maximum 10 vehicles allowed.")
            return

        if value in self.queue1:
            messagebox.showerror("Error", f"Vehicle {value} already exists in the parking garage.")
            return

        image = random.choice(self.images)
        self.image_map[value] = image
        self.queue1.append(value)
        self.input_entry.delete(0, tk.END)

        # Disable buttons and start animation
        self.animation_in_progress = True
        self.add_button.config(state="disabled")
        self.remove_button.config(state="disabled")
        self.disable_entry_with_message()  # Disable input field with message

        # Animate the image falling into its position
        end_y = self.queue_y_start - (len(self.queue1) - 1) * self.queue_y_offset
        self.animate_image(self.queue1_x, 0, end_y, image)

        # Re-enable buttons after animation
        self.animation_in_progress = False
        self.add_button.config(state="normal")
        self.remove_button.config(state="normal")
        self.enable_entry()

        self.in_count += 1
        self.in_label.config(text=f"Arrived: {self.in_count}")

        self.update_visualization1()
        self.set_layering()

    def remove_from_queue1(self):
        """Remove a specific value from Stack1 and handle Stack2."""
        target = self.input_entry.get()

        # Check if no input
        if not target.strip():
            messagebox.showerror("Input Error", "Please enter a vehicle.")
            return

        # Check if input is valid (letters and numbers only)
        if not target.isalnum():
            messagebox.showerror("Error", "Only letters and numbers are allowed.")
            return

        # Check if target exists in stack1
        if target not in self.queue1:
            messagebox.showerror("Error", f"Vehicle {target} is not found in the parking slot.")
            return

        # Only allow removal if the entered vehicle matches the first slot
        if target != self.queue1[0]:
            messagebox.showerror("Error", "Only the first vehicle in the parking garage can be removed.")
            return

        # Only allow removal of the first vehicle
        target = self.queue1[0]

        # Disable buttons and start animation
        self.animation_in_progress = True
        self.add_button.config(state="disabled")
        self.remove_button.config(state="disabled")
        self.disable_entry_with_message()  # Disable input field with message

        # Animate the target car leaving downward
        start_y = self.queue_y_start
        end_y = start_y + 100  # Move downward
        self.animate_image(self.queue1_x, start_y, end_y, self.image_map[target], direction="down")
        messagebox.showinfo("Notice", f"Vehicle {target} has left the parking garage.")

        # Remove the target from queue1
        self.queue1.pop(0)

        # Animate the rest of the cars moving up
        y = self.queue_y_start
        for value in self.queue1:
            self.animate_image(self.queue1_x, y + self.queue_y_offset, y, self.image_map[value], direction="down")
            y -= self.queue_y_offset

        # Re-enable buttons after animation
        self.animation_in_progress = False
        self.add_button.config(state="normal")
        self.remove_button.config(state="normal")
        self.enable_entry()  # Re-enable input field

        # Update the counters
        self.out_count += 1
        self.out_label.config(text=f"Vehicles Out: {self.out_count}")

        self.update_visualization2()

        # Delete the target car's image and label from stack1
        self.canvas.delete(f"vehicle_{target}")
        self.canvas.delete(f"label_{target}")
        self.canvas.delete(f"label_bg_{target}")

        self.update_visualization1()
        self.set_layering()


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = ParkingQueue(root)
    root.mainloop()
