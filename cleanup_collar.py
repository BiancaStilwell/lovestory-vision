#!/usr/bin/env python3
"""
Remove cream background from collar image and make it 15% bigger
"""

from rembg import remove
from PIL import Image
import os

def cleanup_collar():
    input_path = "assets/landing_collar_clean.JPG"
    output_path = "assets/landing_collar_no_bg.png"
    
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
    
    # Calculate new dimensions (15% + 10% + 10% = 39.15% bigger total)
    new_width = int(width * 1.3915)
    new_height = int(height * 1.3915)
    
    # Resize the image
    resized_image = output_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Save the result
    resized_image.save(output_path, "PNG")
    
    print(f"Background removed and image enlarged by 39.15%! Saved as {output_path}")
    print(f"Original size: {width}x{height}, New size: {new_width}x{new_height}")

if __name__ == "__main__":
    cleanup_collar()
