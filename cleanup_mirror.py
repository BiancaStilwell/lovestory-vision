#!/usr/bin/env python3
"""
Clean up red reflections and dots from the black areas of the mirror image
"""

from PIL import Image, ImageFilter
import numpy as np

def cleanup_red_reflections():
    input_path = "assets/landing_mirror_clean.png"
    output_path = "assets/landing_mirror_cleaner.png"
    
    # Open the image
    img = Image.open(input_path)
    img = img.convert('RGBA')
    
    # Convert to numpy array for easier manipulation
    data = np.array(img)
    
    # Create a mask for red areas (more aggressive)
    red_channel = data[:, :, 0]
    green_channel = data[:, :, 1]
    blue_channel = data[:, :, 2]
    alpha_channel = data[:, :, 3]
    
    # More aggressive red detection
    red_mask = (red_channel > 100) & (red_channel > green_channel * 1.2) & (red_channel > blue_channel * 1.2) & (alpha_channel > 30)
    
    # Find any reddish areas (lower threshold)
    reddish_areas = (red_channel > 80) & (red_channel > green_channel) & (red_channel > blue_channel) & (alpha_channel > 20)
    
    # Find dark areas that should be blacker
    dark_areas = (red_channel < 100) & (green_channel < 100) & (blue_channel < 100) & (alpha_channel > 50)
    
    # Combine masks
    red_areas = red_mask | reddish_areas
    
    # Set red areas to transparent
    data[red_areas, 3] = 0  # Set alpha to 0 for red areas
    
    # Make dark areas blacker
    data[dark_areas, 0] = np.minimum(data[dark_areas, 0], 30)  # Reduce red
    data[dark_areas, 1] = np.minimum(data[dark_areas, 1], 30)  # Reduce green
    data[dark_areas, 2] = np.minimum(data[dark_areas, 2], 30)  # Reduce blue
    
    # Create new image from cleaned data
    cleaned_img = Image.fromarray(data)
    
    # Apply a stronger blur to smooth artifacts
    cleaned_img = cleaned_img.filter(ImageFilter.GaussianBlur(radius=1.0))
    
    # Save the result
    cleaned_img.save(output_path, "PNG")
    
    print(f"More aggressive red cleanup and black enhancement! Saved as {output_path}")
    print("You can now update the landing page to use this cleaner version.")

if __name__ == "__main__":
    cleanup_red_reflections()
