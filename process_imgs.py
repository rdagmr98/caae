import os, shutil
from pathlib import Path
from PIL import Image
import numpy as np

src  = Path(r"C:\Users\Gianmarco\Documents\sito")
saio = src / "Centro Addestrativo Aviazione Esercito - S.A.I.O._files"
dst  = Path(r"C:\Users\Gianmarco\caae\imgs")
dst.mkdir(exist_ok=True)

MAX_W   = 1920
QUALITY = 85

def resize_jpg(in_path, out_path, max_w=MAX_W, quality=QUALITY):
    img = Image.open(in_path).convert("RGB")
    w, h = img.size
    if w > max_w:
        ratio = max_w / w
        img = img.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
    img.save(out_path, "JPEG", quality=quality, optimize=True)
    print(f"  OK  {out_path.name}  {out_path.stat().st_size//1024} KB")

def resize_png(in_path, out_path, max_w=1280):
    img = Image.open(in_path)
    img = img.convert("RGBA")
    w, h = img.size
    if w > max_w:
        ratio = max_w / w
        img = img.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
    img.save(out_path, "PNG", optimize=True)
    print(f"  OK  {out_path.name}  {out_path.stat().st_size//1024} KB")

print("=== Elicotteri ===")
resize_jpg(src/"169_d0_d0.jpg",   dst/"luh169b_caae.jpg",      max_w=1920, quality=85)
resize_jpg(src/"_39A6896_d0.jpg", dst/"luh169b_ceremony.jpg",  max_w=1920, quality=85)
resize_jpg(src/"_39A6910_d0.JPG", dst/"luh169b_ceremony2.jpg", max_w=1920, quality=85)
resize_jpg(src/"169.jpg",          dst/"luh169_bg.jpg",         max_w=1920, quality=82)
resize_jpg(src/"205.jpg",          dst/"ab205_caae.jpg",        max_w=1920, quality=85)
shutil.copy2(src/"206_4_2_d0.jpg", dst/"ab206_caae.jpg")
print(f"  OK  ab206_caae.jpg  {(dst/'ab206_caae.jpg').stat().st_size//1024} KB")
for fn, outname in [("206_2.jpg","206_2_caae.jpg"),("206_3.jpg","206_3_caae.jpg"),
                     ("206_4.jpg","206_4_caae.jpg"),("206_31.jpg","206_31_caae.jpg")]:
    resize_jpg(src/fn, dst/outname, max_w=1280, quality=82)

print("\n=== Corsi SERE ===")
for i in range(1, 4):
    resize_png(saio/f"sere{i}_1_d0.PNG", dst/f"sere{i}.png")

print("\n=== Corsi MEDEVAC ===")
resize_png(saio/"medevac_d0.png",  dst/"medevac0.png")
resize_png(saio/"medevac1_d0.png", dst/"medevac1.png")
resize_png(saio/"medevac2_d0.png", dst/"medevac2.png")

print("\n=== Corsi PR ===")
resize_png(saio/"pr_d0.PNG",   dst/"pr0.png")
resize_png(saio/"pr2_d0.png",  dst/"pr1.png")
resize_png(saio/"pr3_d0.png",  dst/"pr2.png")

print("\n=== Stemmi corsi ===")
resize_png(saio/"stemmamedevac1_d0.PNG", dst/"stemma_medevac.png", max_w=400)
resize_png(saio/"stemmapr_d0_1_d0.PNG",  dst/"stemma_pr.png",     max_w=400)
resize_png(saio/"stemmasere_2_d0.PNG",   dst/"stemma_sere.png",   max_w=400)

print("\n=== Extra foto SAIO ===")
resize_jpg(saio/"IMG20231026WA0048_d0.jpg",   dst/"caae_extra1.jpg", max_w=1280, quality=82)
resize_jpg(saio/"20230615_204737_d0.jpg",      dst/"caae_extra2.jpg", max_w=1280, quality=82)
resize_jpg(saio/"20200303_185132_d0_d0.jpg",   dst/"caae_extra3.jpg", max_w=1280, quality=82)

print("\n=== Stemma ufficiale (rimozione sfondo bianco) ===")
img = Image.open(saio/"ceadd_aves_arald_d0.png").convert("RGBA")
data = np.array(img)
r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
white_mask = (r > 240) & (g > 240) & (b > 240)
data[white_mask, 3] = 0
result = Image.fromarray(data)
stemma_out = Path(r"C:\Users\Gianmarco\caae\stemma_caae.png")
result.save(stemma_out, "PNG")
print(f"  OK  stemma_caae.png  {stemma_out.stat().st_size//1024} KB")
# Versione grande per le pagine
w2, h2 = result.size
if w2 > 600:
    r2 = 600/w2
    big = result.resize((int(w2*r2), int(h2*r2)), Image.LANCZOS)
else:
    big = result
big.save(dst/"stemma_caae_hd.png", "PNG")
print(f"  OK  stemma_caae_hd.png  {(dst/'stemma_caae_hd.png').stat().st_size//1024} KB")

print("\n=== Vegetato footer ===")
resize_jpg(src/"vegetato_footer.jpg", dst/"vegetato_footer.jpg", max_w=1920, quality=80)

print("\nTUTTO FATTO!")
