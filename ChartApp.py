import tkinter as tk
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
            self.canvas.delete("all")
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
            self.canvas.delete("all")
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