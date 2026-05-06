#!/usr/bin/env python3
from PIL import Image
import os

imgs_dir = "imgs"

# Immagini 206 da ritagliare
images_to_crop = [
    "ab206_caae.jpg",
    "206_2_caae.jpg",
    "206_3_caae.jpg"
]

for img_name in images_to_crop:
    path = os.path.join(imgs_dir, img_name)
    if not os.path.exists(path):
        print(f"Skip {img_name} - not found")
        continue
    
    try:
        img = Image.open(path)
        w, h = img.size
        print(f"{img_name}: {w}x{h}")
        
        if w > h:  # landscape - crop height to 65%
            new_h = int(h * 0.65)
            top = (h - new_h) // 2
            crop_box = (0, top, w, top + new_h)
            cropped = img.crop(crop_box)
            print(f"  -> Cropped to {cropped.size}")
            cropped.save(path, "JPEG", quality=85)
        else:
            print(f"  -> Skipping (not landscape)")
    except Exception as e:
        print(f"Error with {img_name}: {e}")

print("\nDone cropping AB-206 images")
