import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from PIL import Image, ImageDraw
import requests
import os

# QR URL (GitHub Pages)
url = "https://rdagmr98.github.io/caae/"

# Download stemma CAAE from Wikimedia
logo_url = "https://upload.wikimedia.org/wikipedia/commons/5/58/CoA_mil_ITA_centro_aves.png"
logo_path = "caae_stemma_tmp.png"
headers = {"User-Agent": "Mozilla/5.0 (CAAE-QR-Generator/1.0)"}
resp = requests.get(logo_url, headers=headers, timeout=20)
resp.raise_for_status()
with open(logo_path, "wb") as f:
    f.write(resp.content)

# Generate QR
qr = qrcode.QRCode(
    version=3,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

qr_img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    fill_color="#0a1628",
    back_color="#ffffff",
).convert("RGB")

# Resize to standard size
qr_img = qr_img.resize((600, 600), Image.LANCZOS)

# Load and resize logo
logo = Image.open(logo_path).convert("RGBA")
logo_size = 120
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

# Create white circular background for logo
circle_bg = Image.new("RGBA", (logo_size + 20, logo_size + 20), (255, 255, 255, 0))
draw = ImageDraw.Draw(circle_bg)
draw.ellipse((0, 0, logo_size + 20 - 1, logo_size + 20 - 1), fill=(255, 255, 255, 255))

# Add gold border ring
ring_size = logo_size + 28
ring = Image.new("RGBA", (ring_size, ring_size), (255, 255, 255, 0))
draw_ring = ImageDraw.Draw(ring)
draw_ring.ellipse((0, 0, ring_size - 1, ring_size - 1), fill=(201, 162, 39, 255))
draw_ring.ellipse((6, 6, ring_size - 7, ring_size - 7), fill=(255, 255, 255, 255))

# Center position on QR
qr_rgba = qr_img.convert("RGBA")
ring_pos = ((600 - ring_size) // 2, (600 - ring_size) // 2)
qr_rgba.paste(ring, ring_pos, ring)

# Paste white circle background
circle_pos = ((600 - logo_size - 20) // 2, (600 - logo_size - 20) // 2)
qr_rgba.paste(circle_bg, circle_pos, circle_bg)

# Paste logo
logo_pos = ((600 - logo_size) // 2, (600 - logo_size) // 2)
qr_rgba.paste(logo, logo_pos, logo)

# Save final QR
output_path = os.path.join(os.path.expanduser("~"), "Desktop", "CAAE_QRCode.png")
final = qr_rgba.convert("RGB")
final.save(output_path, dpi=(300, 300))

# Clean up temp
os.remove(logo_path)

print(f"QR code saved to: {output_path}")
print(f"Points to: {url}")
print(f"Size: {final.size}")
