import tkinter as tk
from tkinter import filedialog, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from core import convert_to_ascii


class PicToAsciiApp:

    def __init__(self, root):
        self.root = root
        self.root.title("PicToAsciiArt")
        self.root.geometry("800x650")

        self.image_path = None

        # Control Panel
        control_frame = ttk.Frame(root, padding="10")
        control_frame.pack(fill=tk.X)

        self.btn_select = ttk.Button(
            control_frame, text="Open Image", command=self.load_image
        )
        self.btn_select.pack(side=tk.LEFT, padx=5)

        self.btn_copy = ttk.Button(
            control_frame, text="Copy ASCII", command=self.copy_to_clipboard
        )
        self.btn_copy.pack(side=tk.LEFT, padx=5)

        # Save As File Button
        self.btn_save = ttk.Button(
            control_frame, text="Save As...", command=self.save_to_file
        )
        self.btn_save.pack(side=tk.LEFT, padx=5)

        # Manual Width Entry Field
        ttk.Label(control_frame, text="Width:").pack(side=tk.LEFT, padx=(15, 5))
        
        self.width_var = tk.StringVar(value="100")
        self.width_entry = ttk.Entry(
            control_frame, textvariable=self.width_var, width=6
        )
        self.width_entry.pack(side=tk.LEFT, padx=5)
        
        # Apply/Update width on Enter key or when leaving field
        self.width_entry.bind("<Return>", lambda e: self.on_width_change())
        self.width_entry.bind("<FocusOut>", lambda e: self.on_width_change())

        self.btn_apply_width = ttk.Button(
            control_frame, text="Apply Width", command=self.on_width_change
        )
        self.btn_apply_width.pack(side=tk.LEFT, padx=5)

        # Status Label / Drop Zone Indicator
        self.status_label = ttk.Label(
            root,
            text="Drag and drop an image file anywhere into the window",
            anchor="center",
            padding="5",
        )
        self.status_label.pack(fill=tk.X)

        # Text Output Area Frame
        text_frame = ttk.Frame(root, padding="10")
        text_frame.pack(fill=tk.BOTH, expand=True)

        # Grid configuration for scrollbars alignment
        text_frame.rowconfigure(0, weight=1)
        text_frame.columnconfigure(0, weight=1)

        self.text_area = tk.Text(text_frame, font=("Courier", 6), wrap=tk.NONE)
        self.text_area.grid(row=0, column=0, sticky="nsew")

        # Vertical Scrollbar
        v_scroll = ttk.Scrollbar(
            text_frame, orient=tk.VERTICAL, command=self.text_area.yview
        )
        v_scroll.grid(row=0, column=1, sticky="ns")
        self.text_area.configure(yscrollcommand=v_scroll.set)

        # Horizontal Scrollbar
        h_scroll = ttk.Scrollbar(
            text_frame, orient=tk.HORIZONTAL, command=self.text_area.xview
        )
        h_scroll.grid(row=1, column=0, sticky="ew")
        self.text_area.configure(xscrollcommand=h_scroll.set)

        # Register Drag and Drop Target
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.handle_drop)

    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp")]
        )
        if path:
            self.set_image_path(path)

    def handle_drop(self, event):
        file_path = event.data.strip()
        if file_path.startswith("{") and file_path.endswith("}"):
            file_path = file_path[1:-1]

        if file_path.lower().endswith(
            (".png", ".jpg", ".jpeg", ".bmp", ".webp")
        ):
            self.set_image_path(file_path)
        else:
            self.status_label.config(
                text="Unsupported file type! Please drop an image."
            )

    def set_image_path(self, path):
        self.image_path = path
        self.status_label.config(text=f"Loaded: {path}")
        self.process_image()

    def on_width_change(self):
        if self.image_path:
            self.process_image()

    def process_image(self):
        try:
            width = int(self.width_var.get())
            if width <= 0:
                raise ValueError("Width must be positive")
        except ValueError:
            self.status_label.config(text="Please enter a valid positive integer for width.")
            return

        ascii_art = convert_to_ascii(self.image_path, new_width=width)

        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, ascii_art)
        self.status_label.config(text=f"Loaded: {self.image_path} (Width: {width})")

    def copy_to_clipboard(self):
        content = self.text_area.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.status_label.config(text="ASCII art copied to clipboard!")

    def save_to_file(self):
        content = self.text_area.get("1.0", tk.END).strip()
        if not content:
            self.status_label.config(text="Nothing to save!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save ASCII Art As",
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.status_label.config(text=f"Saved to {file_path}")
            except Exception as e:
                self.status_label.config(text=f"Error saving file: {e}")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PicToAsciiApp(root)
    root.mainloop()