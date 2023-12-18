import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class PatchIndexExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("Patch Index Extractor")
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.open_image)
        input_frame = tk.Frame(root)
        input_frame.pack(side=tk.LEFT, padx=10)
        self.patch_size_label = tk.Label(input_frame, text="Patch Size:")
        self.patch_size_label.pack(side=tk.TOP, pady=5)
        self.patch_size_entry = tk.Entry(input_frame)
        self.patch_size_entry.pack(side=tk.TOP, pady=5)
        self.apply_button = tk.Button(input_frame, text="Apply", command=self.apply_patch_size)
        self.apply_button.pack(side=tk.TOP, pady=5)
        self.width_label = tk.Label(input_frame, text="Width:")
        self.width_label.pack(side=tk.TOP, pady=5)
        self.width_entry = tk.Entry(input_frame)
        self.width_entry.pack(side=tk.TOP, pady=5)
        self.height_label = tk.Label(input_frame, text="Height:")
        self.height_label.pack(side=tk.TOP, pady=5)
        self.height_entry = tk.Entry(input_frame)
        self.height_entry.pack(side=tk.TOP, pady=5)
        self.resize_button = tk.Button(input_frame, text="Resize", command=self.resize_image)
        self.resize_button.pack(side=tk.TOP, pady=5)
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.patch_index_label = tk.Label(root, text="Patch Index: -")
        self.patch_index_label.pack(side=tk.BOTTOM, pady=5)
        self.original_image = None
        self.resized_image = None
        self.photo_image = None
        self.patch_size = None
        self.highlight_rect = None

    def open_image(self):
        file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.resize_image()
            self.photo_image = ImageTk.PhotoImage(self.resized_image)
            self.canvas.config(width=self.photo_image.width(), height=self.photo_image.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

    def apply_patch_size(self):
        try:
            patch_size = int(self.patch_size_entry.get())
            if patch_size >= 4:
                self.patch_size = patch_size
                self.canvas.delete("patch")
                self.canvas.delete(self.highlight_rect)
                self.display_patches()
            elif patch_size > 0 and patch_size < 4:
                self.patch_size = patch_size
                self.canvas.delete("patch")
                self.canvas.delete(self.highlight_rect)
            else:
                print("Please enter a valid patch size.")
        except ValueError:
            print("Please enter a valid number for patch size.")

    def resize_image(self):
        width_str = self.width_entry.get()
        height_str = self.height_entry.get()
        if width_str and height_str:
            width = int(width_str)
            height = int(height_str)
            self.resized_image = self.original_image.resize((width, height))
        else:
            self.resized_image = self.original_image.copy()
        self.photo_image = ImageTk.PhotoImage(self.resized_image)
        self.canvas.config(width=self.photo_image.width(), height=self.photo_image.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
        self.canvas.delete("patch")
        self.display_patches()

    def display_patches(self):
        if self.resized_image and self.patch_size:
            image_width, image_height = self.resized_image.size
            for y in range(0, image_height, self.patch_size):
                for x in range(0, image_width, self.patch_size):
                    # patch line color
                    patch_rect = self.canvas.create_rectangle(x, y, x + self.patch_size, y + self.patch_size, outline="blue", tags="patch")
                    self.canvas.tag_bind(patch_rect, "<Button-1>", lambda event, rect=patch_rect: self.on_patch_click(event, rect))

    def on_patch_click(self, event, patch_rect):
        if self.patch_size:
            if self.highlight_rect:
                self.canvas.delete(self.highlight_rect)
            x1, y1, x2, y2 = self.canvas.coords(patch_rect)
            patch_index_x = x1 // self.patch_size
            patch_index_y = y1 // self.patch_size
            patch_index = patch_index_y * (self.resized_image.width // self.patch_size) + patch_index_x
            # highlight patch color
            self.highlight_rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)
            self.patch_index_label.config(text=f"Patch Index: {patch_index}")

    def on_canvas_click(self, event):
        if self.resized_image and self.patch_size:
            x, y = event.x, event.y
            patch_index_x = x // self.patch_size
            patch_index_y = y // self.patch_size
            patch_index = patch_index_y * (self.resized_image.width // self.patch_size) + patch_index_x
            if self.highlight_rect:
                self.canvas.delete(self.highlight_rect)
            self.highlight_rect = self.canvas.create_rectangle(
                patch_index_x * self.patch_size,
                patch_index_y * self.patch_size,
                (patch_index_x + 1) * self.patch_size,
                (patch_index_y + 1) * self.patch_size,
                outline="red", width=2
            )
            self.patch_index_label.config(text=f"Patch Index: {patch_index}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PatchIndexExtractor(root)
    root.mainloop()
