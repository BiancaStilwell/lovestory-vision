#!/usr/bin/env python3
"""
Remove bright outlines and artifacts from the collar image
"""

from PIL import Image, ImageFilter
import numpy as np

def cleanup_outlines():
    input_path = "assets/landing_collar_no_bg.png"
    output_path = "assets/landing_collar_clean_edges.png"
    
    # Open the image
    img = Image.open(input_path)
    img = img.convert('RGBA')
    
    # Convert to numpy array for easier manipulation
    data = np.array(img)
    
    # Get color channels
    red_channel = data[:, :, 0]
    green_channel = data[:, :, 1]
    blue_channel = data[:, :, 2]
    alpha_channel = data[:, :, 3]
    
    # Find bright areas (high values in any channel) with low alpha
    bright_areas = ((red_channel > 200) | (green_channel > 200) | (blue_channel > 200)) & (alpha_channel < 150)
    
    # Find areas that are too bright overall (likely artifacts)
    too_bright = (red_channel + green_channel + blue_channel) > 400
    
    # Find areas with low alpha that might be artifacts
    low_alpha_artifacts = (alpha_channel < 100) & ((red_channel > 100) | (green_channel > 100) | (blue_channel > 100))
    
    # Combine all artifact masks
    artifacts = bright_areas | too_bright | low_alpha_artifacts
    
    # Set artifact areas to completely transparent
    data[artifacts, 3] = 0
    
    # Create new image from cleaned data
    cleaned_img = Image.fromarray(data)
    
    # Apply a very slight blur to smooth any remaining edge artifacts
    cleaned_img = cleaned_img.filter(ImageFilter.GaussianBlur(radius=0.3))
    
    # Save the result
    cleaned_img.save(output_path, "PNG")
    
    print(f"Bright outlines and artifacts removed! Saved as {output_path}")

if __name__ == "__main__":
    cleanup_outlines()
