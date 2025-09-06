#!/usr/bin/env python3
"""
Remove background from image 19 and save as PNG with transparency
"""

from rembg import remove
from PIL import Image
import os

def remove_background_from_19():
    input_path = "assets/landing_mirror.JPG"
    output_path = "assets/landing_mirror_no_bg.png"
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found!")
        return
    
    print(f"Processing {input_path}...")
    
    # Read the image
    input_image = Image.open(input_path)
    
    # Remove background
    output_image = remove(input_image)
    
    # Save the result
    output_image.save(output_path, "PNG")
    
    print(f"Background removed! Saved as {output_path}")
    print("You can now replace the original image with this one.")

if __name__ == "__main__":
    remove_background_from_19()
