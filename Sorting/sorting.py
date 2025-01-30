import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Global flag to stop sorting when the user closes the window
stop_sorting = False

# Load background images
bg_image = mpimg.imread("sortingpage2.png")  # Used in sorting visualization
tk_bg_image = Image.open("sortingpage1.png")  # Used for Tkinter background

def draw_bars_with_labels(arr, step):
    """ Draws bars with background image and updates the plot. """
    global stop_sorting
    if stop_sorting:
        return
    
    plt.clf()
    plt.imshow(bg_image, aspect='auto', extent=[-1, len(arr), 0, max(arr) + 5], alpha=0.7)  # Adjust alpha for transparency
    plt.bar(range(len(arr)), arr, color="#1035AC")
    
    for i, val in enumerate(arr):
        plt.text(i, val + 0.5, str(val), ha='center', va='bottom', fontsize=9, color='black')
    
    # Set y-ticks to include 0, 20, 40, 60, 80, and 100
    plt.yticks(np.arange(0, 101, 20))  # Adds 100 to the list of y-ticks

    # Set x-ticks starting from 5 and jumping between the bars
    tick_positions = [4, 9, 14, 19, 24, 29]  # Indices corresponding to 5, 10, 15, 20, 25, 30
    tick_labels = [5, 10, 15, 20, 25, 30]  # The labels to display at those positions

    plt.xticks(tick_positions, tick_labels)  # Specify custom ticks and their labels
    plt.title(f"Sorting Visualization - Step {step}")
    plt.pause(0.01)

def sorting_wrapper(sort_function, arr):
    """ Wrapper to handle premature closing of the plot window. """
    global stop_sorting
    stop_sorting = False

    def on_close(event):
        """ Set flag when the figure is closed. """
        global stop_sorting
        stop_sorting = True
        plt.close()

    fig = plt.figure()
    fig.canvas.mpl_connect("close_event", on_close)

    sort_function(arr)

    if not stop_sorting:
        finalize_plot(arr)

def finalize_plot(arr):
    """ Finalizes the sorting plot. Ensures proper closing behavior. """
    plt.clf()
    plt.imshow(bg_image, aspect='auto', extent=[-1, len(arr), 0, max(arr) + 5], alpha=0.7)  # Same background as draw_bars_with_labels
    plt.bar(range(len(arr)), arr, color="#1035AC")  # Same color as draw_bars_with_labels
    
    for i, val in enumerate(arr):
        plt.text(i, val + 0.5, str(val), ha='center', va='bottom', fontsize=9, color='black')
    
    plt.title("Sorting Completed")
    plt.show(block=True)

def bubble_sort(arr):
    """ Bubble sort implementation. """
    n = len(arr)
    step = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            if stop_sorting:
                return
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                step += 1
                draw_bars_with_labels(arr, step)

def insertion_sort(arr):
    """ Insertion sort implementation. """
    step = 0
    for i in range(1, len(arr)):
        if stop_sorting:
            return
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            step += 1
            draw_bars_with_labels(arr, step)
        arr[j + 1] = key
        step += 1
        draw_bars_with_labels(arr, step)

def selection_sort(arr):
    """ Selection sort implementation. """
    step = 0
    n = len(arr)
    for i in range(n):
        if stop_sorting:
            return
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        step += 1
        draw_bars_with_labels(arr, step)

def merge_sort(arr):
    """ Merge sort implementation. """
    def _merge_sort(arr, left, right, step):
        if left < right:
            mid = (left + right) // 2
            step = _merge_sort(arr, left, mid, step)
            step = _merge_sort(arr, mid + 1, right, step)
            step = merge(arr, left, mid, right, step)
        return step
    
    def merge(arr, left, mid, right, step):
        left_copy = arr[left:mid + 1]
        right_copy = arr[mid + 1:right + 1]
        i, j, k = 0, 0, left
        
        while i < len(left_copy) and j < len(right_copy):
            if stop_sorting:
                return step
            if left_copy[i] < right_copy[j]:
                arr[k] = left_copy[i]
                i += 1
            else:
                arr[k] = right_copy[j]
                j += 1
            k += 1
            step += 1
            draw_bars_with_labels(arr, step)
        
        while i < len(left_copy):
            if stop_sorting:
                return step
            arr[k] = left_copy[i]
            i += 1
            k += 1
            step += 1
            draw_bars_with_labels(arr, step)
        
        while j < len(right_copy):
            if stop_sorting:
                return step
            arr[k] = right_copy[j]
            j += 1
            k += 1
            step += 1
            draw_bars_with_labels(arr, step)
        
        return step

    _merge_sort(arr, 0, len(arr) - 1, 0)

def shell_sort(arr):
    """ Shell sort implementation. """
    n = len(arr)
    gap = n // 2
    step = 0
    while gap > 0:
        for i in range(gap, n):
            if stop_sorting:
                return
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
                step += 1
                draw_bars_with_labels(arr, step)
            arr[j] = temp
            step += 1
            draw_bars_with_labels(arr, step)
        gap //= 2

def quick_sort(arr):
    """ Quick sort implementation. """
    def _quick_sort(items, low, high, step):
        if low < high:
            pi, step = partition(items, low, high, step)
            step = _quick_sort(items, low, pi - 1, step)
            step = _quick_sort(items, pi + 1, high, step)
        return step

    def partition(items, low, high, step):
        pivot = items[high]
        i = low - 1
        for j in range(low, high):
            if stop_sorting:
                return step
            if items[j] < pivot:
                i += 1
                items[i], items[j] = items[j], items[i]
                step += 1
                draw_bars_with_labels(items, step)
        items[i + 1], items[high] = items[high], items[i + 1]
        step += 1
        draw_bars_with_labels(items, step)
        return i + 1, step

    _quick_sort(arr, 0, len(arr) - 1, 0)

def heap_sort(arr):
    """ Heap sort implementation. """
    def heapify(arr, n, i, step):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[l] > arr[largest]:
            largest = l

        if r < n and arr[r] > arr[largest]:
            largest = r

        if largest != i:
            if stop_sorting:
                return step
            arr[i], arr[largest] = arr[largest], arr[i]
            step += 1
            draw_bars_with_labels(arr, step)
            step = heapify(arr, n, largest, step)
        return step

    n = len(arr)
    step = 0
    for i in range(n // 2 - 1, -1, -1):
        step = heapify(arr, n, i, step)

    for i in range(n - 1, 0, -1):
        if stop_sorting:
            return
        arr[i], arr[0] = arr[0], arr[i]
        step += 1
        draw_bars_with_labels(arr, step)
        step = heapify(arr, i, 0, step)

# GUI Setup
root = tk.Tk()
root.title("Sorting Algorithms Visualization")

# Load the background image
original_bg = Image.open("sortingpage1.png")

def update_background(event=None):
    """ Resize and update the background dynamically when the window is resized. """
    new_width = root.winfo_width()
    new_height = root.winfo_height()

    # Resize the background image to match window dimensions
    resized_bg = original_bg.resize((new_width, new_height), Image.Resampling.LANCZOS)
    new_tk_bg = ImageTk.PhotoImage(resized_bg)

    # Update canvas size
    canvas.config(width=new_width, height=new_height)

    # Update background image and keep reference to prevent garbage collection
    canvas.itemconfig(bg_canvas_image, image=new_tk_bg)
    canvas.image = new_tk_bg  # Store reference to prevent garbage collection

    # Keep the image anchored at (0,0)
    canvas.coords(bg_canvas_image, 0, 0)

    # **Call `update_positions` AFTER resizing**
    update_positions()

# Set initial window size (small)
initial_width = 800
initial_height = 600
root.geometry(f"{initial_width}x{initial_height}")

# Create a Canvas for background
canvas = tk.Canvas(root, width=initial_width, height=initial_height)
canvas.pack(fill="both", expand=True)

# Set background image
resized_bg = original_bg.resize((initial_width, initial_height), Image.Resampling.LANCZOS)
tk_bg_image = ImageTk.PhotoImage(resized_bg)
bg_canvas_image = canvas.create_image(0, 0, image=tk_bg_image, anchor="nw")

# Bind resizing event to update the background dynamically
root.bind("<Configure>", update_background)

def process_input(sort_algorithm):
    user_input = entry.get()
    try:
        arr = list(map(int, user_input.split()))
        if len(arr) != 30:
            raise ValueError("Please enter exactly 30 integers.")
        
        # Check if all numbers are between 0 and 100 (inclusive)
        if any(val > 100 for val in arr):
            raise ValueError("All numbers must be less than or equal to 100.")

        plt.ion()
        sorting_wrapper(
            {
                "bubble": bubble_sort,
                "insertion": insertion_sort,
                "selection": selection_sort,
                "merge": merge_sort,
                "shell": shell_sort,
                "quick": quick_sort,
                "heap": heap_sort
            }[sort_algorithm],
            arr
        )

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
        
# Create UI elements on top of background
label = tk.Label(root, text="Enter 30 Integers (Space-Separated):", bg="#ffffff", font=("Arial", 12, "bold"))
entry = tk.Entry(root, width=50)
bubble_button = tk.Button(root, text="Bubble Sort", command=lambda: process_input("bubble"))
insertion_button = tk.Button(root, text="Insertion Sort", command=lambda: process_input("insertion"))
selection_button = tk.Button(root, text="Selection Sort", command=lambda: process_input("selection"))
merge_button = tk.Button(root, text="Merge Sort", command=lambda: process_input("merge"))
shell_button = tk.Button(root, text="Shell Sort", command=lambda: process_input("shell"))
quick_button = tk.Button(root, text="Quick Sort", command=lambda: process_input("quick"))
heap_button = tk.Button(root, text="Heap Sort", command=lambda: process_input("heap"))

def update_positions():
    """ Dynamically centers label, entry, and buttons when the window is resized. """
    canvas_width = root.winfo_width()
    canvas_height = root.winfo_height()
    
    # Center X coordinate for label and entry
    center_x = canvas_width // 2  

    # Space between label and entry field
    label_to_entry_space = 30  # Adjust this value for more or less space between label and entry

    # Update label and entry field position (set them to be just above the buttons)
    start_y = canvas_height - 250  # Place label 50px above the buttons (adjust as needed)
    canvas.coords(label_window, center_x, start_y + 20)
    canvas.coords(entry_window, center_x, start_y + 20 + label_to_entry_space)  # Added space between label and entry

    # Update sorting buttons dynamically
    button_spacing = 110  # Horizontal spacing between buttons
    num_buttons = 7
    total_width = (num_buttons - 1) * button_spacing
    start_x = (canvas_width - total_width) // 2  # Center buttons

    for i, button_window in enumerate(button_windows):
        canvas.coords(button_window, start_x + i * button_spacing, canvas_height - 100)

# Place label and entry field
label_window = canvas.create_window(250, 20, window=label)
entry_window = canvas.create_window(250, 50, window=entry)

# Define button placement (initial empty positions, update_positions will adjust them)
button_windows = [
    canvas.create_window(0, 0, window=bubble_button),
    canvas.create_window(0, 0, window=insertion_button),
    canvas.create_window(0, 0, window=selection_button),
    canvas.create_window(0, 0, window=merge_button),
    canvas.create_window(0, 0, window=shell_button),
    canvas.create_window(0, 0, window=quick_button),
    canvas.create_window(0, 0, window=heap_button),
]

# Bind resizing event **once** for background & positions
root.bind("<Configure>", update_background)

root.resizable(True, True)  # Enable resizing

root.mainloop()
