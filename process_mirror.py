#!/usr/bin/env python3
"""
Remove white background from mirror image and make it 25% bigger
"""

from rembg import remove
from PIL import Image
import os

def process_mirror():
    input_path = "assets/landing_mirror_oval.JPG"
    output_path = "assets/landing_mirror_oval_no_bg.png"
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found!")
        return
    
    print(f"Processing {input_path}...")
    
    # Read the image
    input_image = Image.open(input_path)
    
    # Remove background
    output_image = remove(input_image)
    
    # Get original dimensions
    width, height = output_image.size
    
    # Calculate new dimensions (25% bigger)
    new_width = int(width * 1.25)
    new_height = int(height * 1.25)
    
    # Resize the image
    resized_image = output_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Save the result
    resized_image.save(output_path, "PNG")
    
    print(f"Background removed and image enlarged by 25%! Saved as {output_path}")
    print(f"Original size: {width}x{height}, New size: {new_width}x{new_height}")

if __name__ == "__main__":
    process_mirror()
