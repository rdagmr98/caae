#!/usr/bin/env python3
"""
Fix: processa le foto degli elicotteri e prepara il video SERE
"""
import os, shutil, subprocess
from PIL import Image
import urllib.request

OUT = os.path.join(os.path.dirname(__file__), "imgs")
SRC = r"C:\Users\Gianmarco\Documents\sito"

def save_img(img, path, quality=87):
    img = img.convert("RGB")
    img.save(path, "JPEG", quality=quality, optimize=True)
    print(f"  Salvato: {path} ({os.path.getsize(path)//1024}KB) {img.size}")

def crop_center(img, target_w, target_h):
    """Crop centrato all'aspect ratio desiderato."""
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    tgt_ratio = target_w / target_h
    if src_ratio > tgt_ratio:
        new_w = int(src_h * tgt_ratio)
        x = (src_w - new_w) // 2
        return img.crop((x, 0, x + new_w, src_h))
    else:
        new_h = int(src_w / tgt_ratio)
        y = (src_h - new_h) // 2
        return img.crop((0, y, src_w, y + new_h))

# ────────────────────────────────────────────────────────────
# 1. LUH 169D — usa 169.jpg (6403x4268, ratio 1.5) che ha
#    proporzioni perfette. Zoom sull'area centrale.
# ────────────────────────────────────────────────────────────
print("\n[1] LUH 169D — 169.jpg")
src_169 = os.path.join(SRC, "169.jpg")
img169 = Image.open(src_169)
print(f"  Originale: {img169.size}")

# Crop leggermente per togliere bordi vuoti e fare 3:2
img169_crop = crop_center(img169, 3, 2)
img169_final = img169_crop.resize((1920, 1280), Image.LANCZOS)
save_img(img169_final, os.path.join(OUT, "luh169d_caae.jpg"))

# Extra crop più stretto sull'elicottero (16:9) per background
img169_wide = crop_center(img169, 16, 9)
img169_wide = img169_wide.resize((1920, 1080), Image.LANCZOS)
save_img(img169_wide, os.path.join(OUT, "luh169d_bg.jpg"))

# ────────────────────────────────────────────────────────────
# 2. AB-205 — scarica foto HQ da Wikimedia (Lavaredo 2019)
# ────────────────────────────────────────────────────────────
print("\n[2] AB-205 — scarico da Wikimedia")
url_205_main = "https://upload.wikimedia.org/wikipedia/commons/1/12/Italian_Army_exercise_Lavaredo_2019_-_03.jpg"
url_205_alt  = "https://upload.wikimedia.org/wikipedia/commons/b/b7/Italian_Army_exercise_Lavaredo_2019_-_06.jpg"
url_205_side = "https://upload.wikimedia.org/wikipedia/commons/2/2b/Italian_Army_Aviation_AB_205_helicopter.png"

headers = {"User-Agent": "Mozilla/5.0 (CAAE-site/3.0)"}

def fetch_img(url, dest_path):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    with open(dest_path, "wb") as f:
        f.write(data)
    img = Image.open(dest_path)
    print(f"  Scaricato: {os.path.basename(dest_path)} {img.size}")
    return img

tmp_205_main = os.path.join(OUT, "_tmp_205_main.jpg")
tmp_205_side = os.path.join(OUT, "_tmp_205_side.png")

img_205 = fetch_img(url_205_main, tmp_205_main)
img_205_crop = crop_center(img_205, 3, 2)
img_205_final = img_205_crop.resize((1920, 1280), Image.LANCZOS)
save_img(img_205_final, os.path.join(OUT, "ab205_improved.jpg"))

img_205s = fetch_img(url_205_side, tmp_205_side)
img_205s_crop = crop_center(img_205s, 3, 2)
img_205s_final = img_205s_crop.resize((1920, 1280), Image.LANCZOS)
save_img(img_205s_final, os.path.join(OUT, "ab205_side.jpg"))

os.remove(tmp_205_main)
os.remove(tmp_205_side)

# ────────────────────────────────────────────────────────────
# 3. AB-205 caae.jpg — anche il caae dalla cartella
# ────────────────────────────────────────────────────────────
print("\n[3] AB-205 ufficiale da Documents/sito")
src_205 = os.path.join(SRC, "205.jpg")
img_205_official = Image.open(src_205)
print(f"  Originale: {img_205_official.size}")
img_205_official_crop = crop_center(img_205_official, 3, 2)
img_205_official_final = img_205_official_crop.resize((1920, 1280), Image.LANCZOS)
save_img(img_205_official_final, os.path.join(OUT, "ab205_caae.jpg"))

# ────────────────────────────────────────────────────────────
# 4. AB-206 — crop migliore con più zoom sull'elicottero
# ────────────────────────────────────────────────────────────
print("\n[4] AB-206 — crop migliorato")
for fname, outname in [("206_2.jpg","206_2_improved.jpg"), ("206_3.jpg","206_3_improved.jpg")]:
    src = os.path.join(SRC, fname)
    if os.path.exists(src):
        img = Image.open(src)
        print(f"  {fname}: {img.size}")
        # Crop 4:3 centrato — mostra meglio l'elicottero
        img_c = crop_center(img, 4, 3)
        img_f = img_c.resize((1920, 1440), Image.LANCZOS)
        save_img(img_f, os.path.join(OUT, outname))

# 206_4 per background
src_206_4 = os.path.join(SRC, "206_4.jpg")
if os.path.exists(src_206_4):
    img_206_4 = Image.open(src_206_4)
    img_206_4_c = crop_center(img_206_4, 16, 9)
    img_206_4_f = img_206_4_c.resize((1920, 1080), Image.LANCZOS)
    save_img(img_206_4_f, os.path.join(OUT, "ab206_caae.jpg"))

print("\nDone! Processa le immagini completato.")
