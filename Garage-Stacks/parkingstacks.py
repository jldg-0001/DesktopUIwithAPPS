from PIL import Image, ImageTk  # Import Pillow for image processing
import tkinter as tk
from tkinter import messagebox
import time
import random


class ParkingGarage:
    def __init__(self, root):
        self.stack1 = []  # Main stack for values
        self.stack2 = []  # Secondary stack for temporary storage
        self.image_map = {}  # Maps each input to its associated image
        self.in_count = 0  # Counter for vehicles entering
        self.out_count = 0  # Counter for vehicles exiting
        self.animation_in_progress = False

        # Set window dimensions
        window_width = 850
        window_height = 875
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        # Set up GUI
        root.title("Parking Garage - Stacks")
        root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Set Main Window Icon
        main_icon = Image.open("iconcar.ico")  # Replace with your .ico file
        root.iconphoto(True, ImageTk.PhotoImage(main_icon))

        # Input Frame
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=3)

        self.input_label = tk.Label(self.input_frame, text="Enter Vehicle:", font=("Press Start 2P", 6, "bold"))
        self.input_label.grid(row=0, column=0, padx=10)

        self.input_entry = tk.Entry(self.input_frame, width=30, bg="lightyellow", fg="black", font=(
            "Courier New", 8), relief="groove", bd=1, highlightbackground="yellow", highlightcolor="black",
                                    highlightthickness=1)
        self.input_entry.grid(row=0, column=1, padx=10, )

        self.add_button = tk.Button(self.input_frame, text="Arrival", font=("Press Start 2P", 6, "bold"),
                                    fg="white", bg="green", activebackground="darkgreen",
                                    relief="ridge", bd=3, command=self.add_to_stack1)
        self.add_button.grid(row=0, column=2, padx=5)

        self.remove_button = tk.Button(self.input_frame, text="Departure", font=("Press Start 2P", 6, "bold"),
                                       fg="white", bg="red", activebackground="darkred",
                                       relief="ridge", bd=3, command=self.remove_from_stack1)
        self.remove_button.grid(row=0, column=3, padx=5)

        # Counter Frame
        self.counter_frame = tk.Frame(root)
        self.counter_frame.pack(pady=3)

        self.in_label = tk.Label(self.counter_frame, text="Arrived: 0", font=("Press Start 2P", 6, "bold"), fg="green")
        self.in_label.grid(row=0, column=0, padx=20)

        self.out_label = tk.Label(self.counter_frame, text="Departed: 0", font=("Press Start 2P", 6, "bold"), fg="red")
        self.out_label.grid(row=0, column=1, padx=20 )

        # Canvas for Visualization
        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.pack(pady=3)

        # Load and resize the background image
        self.background_image = self.load_and_resize_background("bgcanva.png", 800, 800)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw", tags="background")

        # Load and resize vehicle images
        self.images = [
            self.load_and_resize_image("car1.png", 45),
            self.load_and_resize_image("car2.png", 45),
            self.load_and_resize_image("car3.png", 45),
            self.load_and_resize_image("car4.png", 45),
            self.load_and_resize_image("car5.png", 45),
            self.load_and_resize_image("car6.png", 45),
            self.load_and_resize_image("car7.png", 45),
            self.load_and_resize_image("car8.png", 45),
        ]

        # Load and resize rectangle images for Stack 1 and Stack 2
        self.stack1_rect_image = self.load_and_resize_image("entext.png", 110)
        self.stack2_rect_image = self.load_and_resize_image("entext.png", 110)

        # Draw rectangle images for stacks
        self.stack1_x = 250  # X-coordinate for Stack 1
        self.stack2_x = 550  # X-coordinate for Stack 2
        self.stack_y_start = 700  # Starting position for the bottom of the stacks
        self.stack_y_offset = 60  # Vertical spacing between images
        self.rectangle_y = 20

        # Add a black rectangle at the topmost part of the canvas, aligned with stack 1
        self.topmost_rect_stack1 = self.canvas.create_rectangle(
            self.stack1_x - 50,  # Left side of the rectangle
            0,  # Top side of the rectangle (very top of the canvas)
            self.stack1_x + 50,  # Right side of the rectangle
            25,  # Bottom side (just below the top part of the canvas)
            fill="black",  # Black color for the rectangle
            tags="stack_rect"  # Same tag as the other stack rectangles for layering
        )

        # Add a black rectangle at the topmost part of the canvas, aligned with stack 2
        self.topmost_rect_stack2 = self.canvas.create_rectangle(
            self.stack2_x - 50,  # Left side of the rectangle, aligned with stack 2
            0,  # Top side of the rectangle (same as stack 1, very top of the canvas)
            self.stack2_x + 50,  # Right side of the rectangle
            25,  # Bottom side (same position as stack 1)
            fill="black",  # Black color for the rectangle
            tags="stack_rect"  # Same tag as the other stack rectangles for layering
        )

        # If you need the rectangles to always be on the topmost layer:
        self.canvas.tag_raise(self.topmost_rect_stack1)
        self.canvas.tag_raise(self.topmost_rect_stack2)

        # Add rectangle objects to canvas with tags
        self.stack1_rect = self.canvas.create_image(self.stack1_x, self.rectangle_y + 100, image=self.stack1_rect_image, anchor="s", tags="stack_rect")
        self.stack2_rect = self.canvas.create_image(self.stack2_x, self.rectangle_y + 100, image=self.stack2_rect_image, anchor="s", tags="stack_rect")

        # Draw labels for the stacks (always on top of the vehicles)
        self.canvas.create_text(self.stack1_x, self.stack_y_start + 80, text="Parking Garage",
                                font=("Press Start 2P", 10, "bold"), fill="white", tags="stack")
        self.canvas.create_text(self.stack2_x, self.stack_y_start + 80, text="Temporary Parking",
                                font=("Press Start 2P", 10, "bold"), fill="white", tags="stack")

        # Load and resize the image for the exit button
        self.exit_icon = self.load_and_resize_image("exiticon.png", 35)

        # Exit Button with image
        self.exit_button = tk.Button(root, image=self.exit_icon, command=root.quit, borderwidth=0, bg="white")
        self.exit_button.place(x=789, y=10)  # Adjust placement as needed

    def load_and_resize_background(self, filepath, canvas_width, canvas_height):
        """Load and resize the background image to fit the canvas."""
        with Image.open(filepath) as img:
            resized_img = img.resize((canvas_width, canvas_height), Image.LANCZOS)
            return ImageTk.PhotoImage(resized_img)

    def load_and_resize_image(self, filepath, target_height):
        """Load an image and resize it to the target height while maintaining aspect ratio."""
        with Image.open(filepath) as img:
            original_width, original_height = img.size
            scale = target_height / original_height
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
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
        self.canvas.delete("stack")  # Remove only stack-related images
        self.canvas.delete("vehicle")  # Remove only vehicle images

        # Redraw the background (only once)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw", tags="background")

        # Draw Stack 1
        y = self.stack_y_start
        for value in self.stack1:
            self._draw_image(self.stack1_x, y, value)
            y -= self.stack_y_offset

        # Draw Stack 2
        y = self.stack_y_start
        for value in self.stack2:
            self._draw_image(self.stack2_x, y, value)
            y -= self.stack_y_offset

        # Redraw rectangle images for the stacks (always on top of the vehicles)
        self.stack1_rect = self.canvas.create_image(self.stack1_x, self.rectangle_y + 100,
                                                    image=self.stack1_rect_image, anchor="s", tags="stack")
        self.stack2_rect = self.canvas.create_image(self.stack2_x, self.rectangle_y + 100,
                                                    image=self.stack2_rect_image, anchor="s", tags="stack")

        # Draw labels for the stacks (always on top of the vehicles)
        self.canvas.create_text(self.stack1_x, self.stack_y_start + 80, text="Parking Garage",
                                font=("Press Start 2P", 10, "bold"), fill="white", tags="text")
        self.canvas.create_text(self.stack2_x, self.stack_y_start + 80, text="Temporary Parking",
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
        self.canvas.tag_raise("stack_rect")  # Stack rectangles at the top

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
            self.canvas.tag_raise("stack_rect")

            y += step
            time.sleep(0.02)  # Pause for smooth animation

        # Ensure the final position is correct
        self.canvas.move(img, 0, end_y - y)
        self.canvas.tag_lower("background")
        self.canvas.tag_raise("vehicle")
        self.canvas.tag_raise("stack_rect")

    def update_visualization2(self):
        """Update the canvas visualization of stacks without clearing the background."""
        # Remove previous vehicles and labels
        self.canvas.delete("vehicle")  # Remove vehicle images
        self.canvas.delete("label")  # Remove vehicle labels

        # Draw Stack 1 with labels
        y = self.stack_y_start
        for value in self.stack1:
            self._draw_image(self.stack1_x, y, value)
            y -= self.stack_y_offset

        # Draw Stack 2 with labels
        y = self.stack_y_start
        for value in self.stack2:
            self._draw_image(self.stack2_x, y, value)
            y -= self.stack_y_offset

        # Redraw rectangles and labels for stacks
        self.stack1_rect = self.canvas.create_image(self.stack1_x, self.rectangle_y + 100,
                                                    image=self.stack1_rect_image, anchor="s", tags="stack")
        self.stack2_rect = self.canvas.create_image(self.stack2_x, self.rectangle_y + 100,
                                                    image=self.stack2_rect_image, anchor="s", tags="stack")
        self.canvas.create_text(self.stack1_x, self.stack_y_start + 80, text="Parking Garage",
                                font=("Press Start 2P", 10, "bold"), fill="white", tags="stack")
        self.canvas.create_text(self.stack2_x, self.stack_y_start + 80, text="Temporary Parking",
                                font=("Press Start 2P", 10, "bold"), fill="white", tags="stack")

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
        self.canvas.tag_raise("stack_rect")  # Rectangles always on top

    def add_to_stack1(self):
        """Add a new value to Stack1 and animate the vehicle."""
        value = self.input_entry.get()

        # Check if no input
        if not value.strip():
            messagebox.showerror("Input Error", "Please enter a vehicle.")
            return

        # Check if input is valid (letters and numbers only)
        if not value.isalnum():
            messagebox.showerror("Error", "Only letters and numbers are allowed.")
            return

        # Check if stack1 is full
        if len(self.stack1) >= 10:
            messagebox.showerror("Error", "Parking Garage is full. Maximum 10 vehicles allowed.")
            return

        # Prevent duplicate entries
        if value in self.stack1:
            messagebox.showerror("Error", f"Vehicle {value} already exists in the parking garage.")
            return

        # Randomly assign an image from the list to the input value
        image = random.choice(self.images)
        self.image_map[value] = image
        self.stack1.append(value)
        self.input_entry.delete(0, tk.END)

        # Disable buttons and start animation
        self.animation_in_progress = True
        self.add_button.config(state="disabled")
        self.remove_button.config(state="disabled")
        self.disable_entry_with_message()  # Disable input field with message

        # Animate the image falling into its position
        end_y = self.stack_y_start - (len(self.stack1) - 1) * self.stack_y_offset
        self.animate_image(self.stack1_x, 0, end_y, image)

        # Re-enable buttons after animation
        self.animation_in_progress = False
        self.add_button.config(state="normal")
        self.remove_button.config(state="normal")
        self.enable_entry()

        # Update the counters
        self.in_count += 1
        self.in_label.config(text=f"Arrived: {self.in_count}")

        # Update the visualization without deleting the background
        self.update_visualization1()
        self.set_layering()

    def remove_from_stack1(self):
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
        if target not in self.stack1:
            messagebox.showerror("Error", f"Vehicle {target} is not found in the parking slot.")
            return

        # Check if stack2 is full
        if len(self.stack2) >= 10:
            messagebox.showerror("Error", "Temporary Storage is full. Maximum 10 vehicles allowed.")
            return

        # Disable buttons and start animation
        self.animation_in_progress = True
        self.add_button.config(state="disabled")
        self.remove_button.config(state="disabled")
        self.disable_entry_with_message()  # Disable input field with message

        # Animate the cars above the target moving to Stack 2
        while self.stack1:
            top = self.stack1.pop()
            if top == target:
                # Animate the target car leaving upwards
                start_y = self.stack_y_start - len(self.stack1) * self.stack_y_offset
                self.animate_image(self.stack1_x, start_y, 0, self.image_map[top], direction="up")
                messagebox.showinfo("Notice", f"Vehicle {target} has left the parking garage.")
                break
            else:
                # Animate the car moving to Stack 2
                start_y = self.stack_y_start - len(self.stack1) * self.stack_y_offset
                end_y = self.stack_y_start - len(self.stack2) * self.stack_y_offset
                self.animate_image(self.stack1_x, start_y, 0, self.image_map[top], direction="up")
                self.animate_image(self.stack2_x, 0, end_y, self.image_map[top], direction="down")
                self.stack2.append(top)

        # Animate the cars in Stack 2 moving back to Stack 1
        while self.stack2:
            top = self.stack2.pop()
            start_y = self.stack_y_start - len(self.stack2) * self.stack_y_offset
            end_y = self.stack_y_start - len(self.stack1) * self.stack_y_offset
            self.animate_image(self.stack2_x, start_y, 0, self.image_map[top], direction="up")
            self.animate_image(self.stack1_x, 0, end_y, self.image_map[top], direction="down")
            self.stack1.append(top)

        # Re-enable buttons after animation
        self.animation_in_progress = False
        self.add_button.config(state="normal")
        self.remove_button.config(state="normal")
        self.enable_entry()  # Re-enable input field

        # Update the counters
        self.out_count += 1
        self.out_label.config(text=f"Vehicles Out: {self.out_count}")

        self.update_visualization2()
        # Delete the target car's image from stack1
        self.canvas.delete(f"vehicle_{target}")
        self.set_layering()

        # Delete the target car's image and label from stack1
        self.canvas.delete(f"vehicle_{target}")
        self.canvas.delete(f"label_{target}")


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)  # Prevent full-screen and resizing
    app = ParkingGarage(root)
    root.mainloop()