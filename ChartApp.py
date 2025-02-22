import tkinter as tk
from tkinter import filedialog
from PIL import ImageGrab
import json
import sys

class GridApp:
    def __init__(self, master, grid_width, grid_height, block_size):
        self.master = master
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.block_size = block_size  # Size of each block
        self.blocks = {}
        #print(type(self.grid_width))
        self.canvas = tk.Canvas(master, width=(self.grid_width + 2) * self.block_size,
                                height=(self.grid_height + 2) * self.block_size)
        self.canvas.pack()

        # Botones para guardar y cargar diseño
        self.save_image_button = tk.Button(master, text="Guardar como Imagen", command=self.save_as_image)
        self.save_image_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.save_json_button = tk.Button(master, text="Guardar para Editar", command=self.save_as_json)
        self.save_json_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.load_json_button = tk.Button(master, text="Cargar Diseño", command=self.load_from_json)
        self.load_json_button.pack(side=tk.LEFT, padx=5, pady=10)

        # Create a 2D list to track the color of each block (True for lightblue, False for white)
        # Also, track the "X" placement (False for no "X", True for "X" placed)
        self.grid = [[{'color': False, 'x': False} for _ in range(grid_width)] for _ in range(grid_height)]

        # Draw the grid with numbered border
        self.draw_grid_with_border()

        # Bind the mouse click events
        self.canvas.bind("<Button-1>", self.toggle_block)  # Left click for color toggle
        self.canvas.bind("<Button-3>", self.toggle_x)      # Right click for toggling "X"

    def draw_grid_with_border(self):
        """Draw the grid with a numbered border around it."""
        self.canvas.delete("all")
        # Draw the grid with blocks
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                x1 = (col + 1) * self.block_size  # Offset by 1 for the border
                y1 = (row + 1) * self.block_size
                x2 = x1 + self.block_size
                y2 = y1 + self.block_size

                # Determine block color (light blue for True, white for False)
                color = 'deep sky blue' if self.grid[row][col]['color'] else 'white'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="sky blue", width=1.5)

                # If there's an "X" in the block, draw it
                if self.grid[row][col]['x']:
                    self.draw_x(x1, y1, x2, y2)

        # Draw the numbers on the left, right, top, and bottom borders
        self.draw_border_numbers()

    def draw_border_numbers(self):
        """Draw the numbers along the outer borders."""
        # Left and Right borders (counting from bottom to top)
        for row in range(self.grid_height):
            # Left side (bottom to top)
            self.canvas.create_text(self.block_size // 2, (row + 1) * self.block_size + self.block_size // 2,
                                    text=str(self.grid_height - row), font=("Arial", 10))
            # Right side (bottom to top)
            #self.canvas.create_text((self.grid_height + 1.5) * self.block_size,
            #(row + 1) * self.block_size + self.block_size // 2,
            #text=str(self.grid_height - row), font=("Arial", 10))

        # Top and Bottom borders (counting from right to left)
        for col in range(self.grid_width):
            # Top side (right to left)
            self.canvas.create_text((col + 1) * self.block_size + self.block_size // 2,
                                    self.block_size // 2, text=str(self.grid_width - col), font=("Arial", 10))
            # Bottom side (right to left)
            #self.canvas.create_text((col + 1) * self.block_size + self.block_size // 2,
            #(self.grid_width + 1.5) * self.block_size,
            #text=str(self.grid_width - col), font=("Arial", 10))

    def draw_x(self, x1, y1, x2, y2):
        """Draw a smaller 'X' on the block."""
        margin = 4  # Margin from the edges of the block (adjust as needed)
        x1_margin = x1 + margin
        y1_margin = y1 + margin
        x2_margin = x2 - margin
        y2_margin = y2 - margin

        # Draw the two diagonal lines that make the smaller "X"
        self.canvas.create_line(x1_margin, y1_margin, x2_margin, y2_margin, fill="gray20", width=1.5)
        self.canvas.create_line(x2_margin, y1_margin, x1_margin, y2_margin, fill="gray20", width=1.5)

    def toggle_block(self, event):
        """Toggle the color of the block when clicked (left-click)."""
        col = (event.x // self.block_size) - 1  # Adjust for border
        row = (event.y // self.block_size) - 1  # Adjust for border

        # Ensure the click is within the grid and not on the border
        if 0 <= col < self.grid_width and 0 <= row < self.grid_height:
            # Toggle the color in the grid
            self.grid[row][col]['color'] = not self.grid[row][col]['color']
            # Redraw the grid to update the block color
            self.draw_grid_with_border()

    def toggle_x(self, event):
        """Toggle the "X" on the block when right-clicked."""
        col = (event.x // self.block_size) - 1  # Adjust for border
        row = (event.y // self.block_size) - 1  # Adjust for border

        # Ensure the click is within the grid and not on the border
        if 0 <= col < self.grid_width and 0 <= row < self.grid_height:
            # Toggle the "X" on the clicked block
            self.grid[row][col]['x'] = not self.grid[row][col]['x']
            # Redraw the grid to show the toggled "X"
            self.draw_grid_with_border()

    def save_as_image(self):
        """Save the canvas as a PNG image."""
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                                                 title="Save as image")
        if file_path:
            self.master.update()
            x = self.master.winfo_rootx() + self.canvas.winfo_x()
            y = self.master.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()

            ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)

    def save_as_json(self):
        """Save the grid data as a JSON file for future editing."""
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                                                 title="Save for editing")
        if file_path:
            data = {
                "grid_width": self.grid_width,
                "grid_height": self.grid_height,
                "block_size": self.block_size,
                "grid": self.grid
            }
            with open(file_path, 'w') as f:
                json.dump(data, f)

    def load_from_json(self):
        """Load a grid design from a JSON file."""
        file_path = filedialog.askopenfilename(defaultextension=".json",
                                               filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                                               title="Load design")
        if file_path:
            with open(file_path, 'r') as f:
                data = json.load(f)

            self.grid_width = data.get("grid_width", self.grid_width)
            self.grid_height = data.get("grid_height", self.grid_height)
            self.block_size = data.get("block_size", self.block_size)
            self.grid = data["grid"]

            self.canvas.config(width=(self.grid_width + 2) * self.block_size,
                               height=(self.grid_height + 2) * self.block_size)
            self.draw_grid_with_border()

# Create the main window
root = tk.Tk()
root.title("Mosaic Chart Creator App")

# Set the default grid size (e.g., 30x30) and block size
grid_width = 75
grid_height = 43
block_size = 20

# Set the sizes according to command line arguments if they exist
n = len(sys.argv)
if n >= 2:
    grid_width = int(sys.argv[1])
if n >= 3:
    grid_height = int(sys.argv[2])
if n >= 4:
    block_size = int(sys.argv[3])

# Create the application
app = GridApp(root, grid_width, grid_height, block_size)

# Run the Tkinter event loop
root.mainloop()