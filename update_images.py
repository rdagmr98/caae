#!/usr/bin/env python3
from PIL import Image
import shutil
import os

source_dir = r"C:\Users\Gianmarco\Documents\sito"
target_dir = "imgs"

# Mappatura: source -> target
images_to_copy = {
    "169_d0_d0.jpg": "luh169d_caae.jpg",      # UH-169D con pattini
    "205.jpg": "ab205_improved.jpg",           # AB-205 versione migliore
    "206_2.jpg": "206_2_improved.jpg",         # AB-206 alternativa
    "206_3.jpg": "206_3_improved.jpg",         # AB-206 alternativa
}

for src, dst in images_to_copy.items():
    src_path = os.path.join(source_dir, src)
    dst_path = os.path.join(target_dir, dst)
    
    if not os.path.exists(src_path):
        print(f"Skip {src} - not found")
        continue
    
    try:
        img = Image.open(src_path)
        w, h = img.size
        print(f"Processing {src}: {w}x{h}")
        
        # Resize max 1920px width, maintain aspect ratio
        if w > 1920:
            ratio = 1920 / w
            new_h = int(h * ratio)
            img = img.resize((1920, new_h), Image.Resampling.LANCZOS)
            print(f"  -> Resized to {img.size}")
        
        # Save with 85% quality
        img.save(dst_path, "JPEG", quality=85)
        print(f"  -> Saved as {dst} ({os.path.getsize(dst_path) // 1024} KB)")
    except Exception as e:
        print(f"Error with {src}: {e}")

print("\nDone updating images")
