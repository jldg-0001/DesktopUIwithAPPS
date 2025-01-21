import random
import tkinter as tk
from PIL import Image, ImageTk
import time

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def generate_bst_with_levels_and_nodes(num_nodes, max_levels):
    if max_levels < 1 or num_nodes < 1 or num_nodes > 2 ** max_levels - 1:
        return None

    values = random.sample(range(1, 101), num_nodes)
    values.sort()

    def build_left_heavy_tree(values, current_level, max_level):
        if not values or current_level > max_level:
            return None

        root = TreeNode(values[0])  # Always take the smallest value as the root
        values.pop(0)  # Remove the root value from the list

        # Prioritize left child 
        if current_level < max_level and values:
            root.left = build_left_heavy_tree(values, current_level + 1, max_level)

        # Add right child only if levels are already filled with left-heavy nodes
        if current_level < max_level and values:
            root.right = build_left_heavy_tree(values, current_level + 1, max_level)

        return root

    return build_left_heavy_tree(values, 1, max_levels)

def draw_tree(canvas, root, x, y, level, max_level, width_per_level, node_dict):
    if root is None or level > max_level:
        return

    radius = 20
    node_id = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#E1C6E8")
    canvas.create_text(x, y, text=str(root.value))

    node_dict[root.value] = node_id

    child_offset = width_per_level // (2 ** (level + 1))

    if root.left:
        canvas.create_line(x, y + radius, x - child_offset, y + 60, arrow=tk.LAST)
        draw_tree(canvas, root.left, x - child_offset, y + 60, level + 1, max_level, width_per_level, node_dict)

    if root.right:
        canvas.create_line(x, y + radius, x + child_offset, y + 60, arrow=tk.LAST)
        draw_tree(canvas, root.right, x + child_offset, y + 60, level + 1, max_level, width_per_level, node_dict)

def traverse_and_visualize(canvas, traversal_list, node_dict):
    for value in traversal_list:
        node_id = node_dict[value]
        canvas.itemconfig(node_id, fill="#FFB6C1")  # Pink
        canvas.update()
        time.sleep(0.5)  # Pause for visibility
        canvas.itemconfig(node_id, fill="#E1C6E8")  # Restore to purple
 
def on_generate():
    try:
        levels = int(levels_entry.get())
        num_values = int(values_entry.get())

        if levels < 1 or levels > 5 or num_values < 1 or num_values > 2**levels - 1:
            result_label.config(text="Please enter valid nodes per level.", fg="red")
            return

        global bst_root, node_dict
        bst_root = generate_bst_with_levels_and_nodes(num_values, levels)

        node_dict = {}
        canvas.delete("all")
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        root_x = canvas_width // 2
        root_y = 50
        draw_tree(canvas, bst_root, root_x, root_y, 1, levels, canvas_width, node_dict)

        preorder = preorder_traversal(bst_root)
        inorder = inorder_traversal(bst_root)
        postorder = postorder_traversal(bst_root)
        
        # Calculate the y-offset dynamically based on the height of the tree
        tree_height = 60 * (levels + 1)  # Assuming each level adds 60 pixels in height
        traversal_y_offset = tree_height + 30  # Add some space below the tree
        update_traversal_display(canvas, preorder, inorder, postorder, traversal_y_offset)
        
        result_label.config(text="Binary Search Tree Generated!")
    except ValueError:
        result_label.config(text="Please enter valid integer values.")

def show_tlr_steps():
    if bst_root:
        traverse_and_visualize(canvas, preorder_traversal(bst_root), node_dict)

def show_ltr_steps():
    if bst_root:
        traverse_and_visualize(canvas, inorder_traversal(bst_root), node_dict)

def show_lrt_steps():
    if bst_root:
        traverse_and_visualize(canvas, postorder_traversal(bst_root), node_dict)

def preorder_traversal(root):
    if root is None:
        return []
    return [root.value] + preorder_traversal(root.left) + preorder_traversal(root.right)

def inorder_traversal(root):
    if root is None:
        return []
    return inorder_traversal(root.left) + [root.value] + inorder_traversal(root.right)

def postorder_traversal(root):
    if root is None:
        return []
    return postorder_traversal(root.left) + postorder_traversal(root.right) + [root.value]

def update_traversal_display(canvas, preorder, inorder, postorder, y_offset):
    canvas_width = canvas.winfo_width()  # Get the canvas width
    canvas.create_text(canvas_width // 2, y_offset, anchor="center", font=("Helvetica", 12, "bold"), 
                       text=f"Preorder (TLR): {preorder}", fill="black")
    canvas.create_text(canvas_width // 2, y_offset + 30, anchor="center", font=("Helvetica", 12, "bold"), 
                       text=f"Inorder (LTR): {inorder}", fill="black")
    canvas.create_text(canvas_width // 2, y_offset + 60, anchor="center", font=("Helvetica", 12, "bold"), 
                       text=f"Postorder (LRT): {postorder}", fill="black")

def resize_background(event):
    """Resizes the background image when the window size changes."""
    new_width = root.winfo_width()
    new_height = root.winfo_height()
    resized_image = bg_original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    global bg_image
    bg_image = ImageTk.PhotoImage(resized_image)
    bg_label.config(image=bg_image)

root = tk.Tk()
root.title("Binary Search Tree Generator")

# Load and set the background image
bg_original_image = Image.open("case4bg.jpg")
bg_image = ImageTk.PhotoImage(bg_original_image)
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

# Add a title at the top
title_label = tk.Label(
    root, text="Binary Search Tree Generator", font=("Helvetica", 16, "bold"), bg="#FFB6C1"
)
title_label.pack(pady=10)  # Add padding to create space around the title

# Create a frame to contain everything
container_frame = tk.Frame(root, bg="white", bd=5)
container_frame.pack(pady=20)

# Controls, buttons, and canvas inside container frame
input_frame = tk.Frame(container_frame, bg="white")
input_frame.grid(row=0, column=0, padx=10, pady=10)

levels_label = tk.Label(input_frame, text="Levels (1-5):", bg="white")
levels_label.grid(row=0, column=0, padx=5)
levels_entry = tk.Entry(input_frame, bg="#E0E0E0", width=10)
levels_entry.grid(row=0, column=1, padx=5)


values_label = tk.Label(input_frame, text="Nodes (1-31):", bg="white")
values_label.grid(row=0, column=2, padx=5)
values_entry = tk.Entry(input_frame, bg="#E0E0E0", width=10)
values_entry.grid(row=0, column=3, padx=5)

generate_button = tk.Button(input_frame, text="Generate BST", command=on_generate, bg="#E1C6E8", fg="black", font=("Arial", 10, "bold"))
generate_button.grid(row=0, column=4, padx=5)

result_label = tk.Label(container_frame, text="", font=("Helvetica", 12), bg="white")
result_label.grid(row=1, column=0, pady=5)

# Buttons frame below input frame
buttons_frame = tk.Frame(container_frame, bg="white")
buttons_frame.grid(row=2, column=0, pady=10)

show_tlr_button = tk.Button(buttons_frame, text="Show TLR Steps", command=show_tlr_steps, bg="#FFB6C1", fg="black", font=("Arial", 10, "bold"))
show_tlr_button.grid(row=0, column=0, padx=10)

show_ltr_button = tk.Button(buttons_frame, text="Show LTR Steps", command=show_ltr_steps, bg="#FFB6C1", fg="black", font=("Arial", 10, "bold"))
show_ltr_button.grid(row=0, column=1, padx=10)

show_lrt_button = tk.Button(buttons_frame, text="Show LRT Steps", command=show_lrt_steps, bg="#FFB6C1", fg="black", font=("Arial", 10, "bold"))
show_lrt_button.grid(row=0, column=2, padx=10)

# Canvas at the bottom
canvas = tk.Canvas(root, width=1000, height=500, bg="white", highlightthickness=0)
canvas.pack(pady=10)

bst_root = None
node_dict = {}

# Bind resize event to update the background
root.bind("<Configure>", resize_background)

root.mainloop()