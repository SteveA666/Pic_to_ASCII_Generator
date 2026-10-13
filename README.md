# Pic to ASCII Generator

Turn images into ASCII art with a simple Python desktop app. Open an image or drag it into the window, adjust the output width, and copy or save the result as text.

## Features

- Open PNG, JPG, JPEG, BMP, and WebP images.
- Drag and drop a single image into the app.
- Adjust the output width in characters (default: 100).
- Preview ASCII art in a monospaced text area with horizontal and vertical scrolling.
- Copy the result to your clipboard or save it as a UTF-8 text file.
- Use the conversion function directly from Python.

## Getting started

You need Python 3 with Tkinter support and Git to clone the repository. The app uses Pillow for image processing and tkinterdnd2 for drag and drop.

```bash
git clone https://github.com/SteveA666/Pic_to_ASCII_Generator.git
cd Pic_to_ASCII_Generator
python -m venv .venv
```

Activate the virtual environment:

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Install the dependencies and start the app:

```bash
python -m pip install -r requirements.txt
python gui.py
```

If your system uses `python3` instead of `python`, substitute it in the commands above. A graphical desktop session is required to run the app.

## Usage

1. Click **Open Image** or drag a supported image into the window. The app converts it automatically.
2. Enter a positive integer in **Width** to set the number of characters per line.
3. Click **Apply Width**, press Enter, or leave the width field to regenerate the output.
4. Click **Copy ASCII** to copy the text, or **Save As...** to export it to a file.

View exported art with a monospaced font and disable line wrapping to preserve its shape. Smaller widths produce compact results; larger widths retain more detail and generate more text.

## Use from Python

From the repository directory, import `convert_to_ascii`:

```python
from core import convert_to_ascii

ascii_art = convert_to_ascii("example.png", new_width=120)
print(ascii_art)

with open("ascii_art.txt", "w", encoding="utf-8") as output:
    output.write(ascii_art)
```

Pass a positive integer for `new_width`. If an image cannot be opened, the function returns a string beginning with `Error loading image:`. `core.py` is an importable module; launch the desktop app with `gui.py`.

## How it works

The converter turns the image into grayscale, resizes it to the requested width, and maps pixel brightness to this character ramp, from dark to light:

```text
@#S%?*+;:,.
```

The output height is calculated as:

```text
max(1, int(output_width × original_height / original_width × 0.55))
```

The `0.55` factor compensates for the height of monospaced characters. The resulting characters are arranged into lines of the requested width.

## Project structure

```text
Pic_to_ASCII_Generator/
├── core.py           # Image resizing and ASCII conversion
├── gui.py            # Tkinter interface, clipboard, and file export
└── requirements.txt  # Python dependencies
```

## Troubleshooting

- **Tkinter is missing:** Check with `python -m tkinter`. If it fails, install Tkinter support for your Python distribution or operating system.
- **A dependency cannot be imported:** Activate your virtual environment and run `python -m pip install -r requirements.txt` using the same interpreter that launches the app.
- **An image will not load:** Confirm that the path is valid and the file is a readable image in a supported format.
- **The output looks distorted:** Use a monospaced font and turn off line wrapping. Font proportions can affect the appearance.
- **Drag and drop fails:** Try dropping one supported image at a time, or use **Open Image**.

## Contributing

Bug reports and improvements are welcome through [GitHub issues](https://github.com/SteveA666/Pic_to_ASCII_Generator/issues) and pull requests. For bug reports, include your operating system, Python version, steps to reproduce, and any error message.

## License

The repository currently does not include a license file. A license should be added to clarify permissions for reuse and distribution.
