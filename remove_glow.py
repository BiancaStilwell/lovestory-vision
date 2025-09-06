#!/usr/bin/env python3
"""
Remove glow effect and clean up edges of the mirror image
"""

from PIL import Image, ImageFilter
import numpy as np

def remove_glow():
    input_path = "assets/landing_mirror_oval_no_bg.png"
    output_path = "assets/landing_mirror_oval_clean.png"
    
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
    
    # Find semi-transparent areas (glow effect)
    semi_transparent = (alpha_channel > 0) & (alpha_channel < 200)
    
    # Find areas that are too bright with low alpha (glow artifacts)
    bright_glow = ((red_channel > 150) | (green_channel > 150) | (blue_channel > 150)) & (alpha_channel < 100)
    
    # Find any areas with very low alpha that might be glow
    low_alpha_glow = alpha_channel < 50
    
    # Combine all glow masks
    glow_areas = semi_transparent | bright_glow | low_alpha_glow
    
    # Set glow areas to completely transparent
    data[glow_areas, 3] = 0
    
    # Create new image from cleaned data
    cleaned_img = Image.fromarray(data)
    
    # Apply a very slight blur to smooth any remaining edge artifacts
    cleaned_img = cleaned_img.filter(ImageFilter.GaussianBlur(radius=0.2))
    
    # Save the result
    cleaned_img.save(output_path, "PNG")
    
    print(f"Glow effect removed! Saved as {output_path}")

if __name__ == "__main__":
    remove_glow()
