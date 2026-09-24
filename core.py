from PIL import Image
import sys

# Standard ASCII character ramp (dark to light)
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image: Image.Image, new_width: int = 100) -> Image.Image:
    """Resizes an image maintaining aspect ratio, corrected for vertical font height."""
    width, height = image.size
    aspect_ratio = height / width
    # 0.55 corrects for vertical height of monospace characters
    new_height = int(new_width * aspect_ratio * 0.55)
    return image.resize((new_width, max(1, new_height)))

def pixels_to_ascii(image: Image.Image) -> str:
    """Converts image pixels to ASCII characters based on brightness."""
    pixels = image.getdata()
    num_chars = len(ASCII_CHARS)
    characters = "".join([ASCII_CHARS[pixel * num_chars // 256] for pixel in pixels])
    return characters

def convert_to_ascii(image_path: str, new_width: int = 100) -> str:
    """Loads an image file and converts it to a formatted ASCII string."""
    try:
        image = Image.open(image_path)
    except Exception as e:
        return f"Error loading image: {e}"

    image = image.convert("L")  # Convert to grayscale
    resized_image = resize_image(image, new_width)
    ascii_str = pixels_to_ascii(resized_image)
    
    # Format the string into lines of equal width
    pixel_count = len(ascii_str)
    ascii_img = "\n".join(
        [ascii_str[i : i + new_width] for i in range(0, pixel_count, new_width)]
    )
    return ascii_img

if __name__ == "__main__":
    raise Exception("Error: this file is not meant to be run as a standalone file")
