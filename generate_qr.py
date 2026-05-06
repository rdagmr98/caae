import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from PIL import Image, ImageDraw
import requests
import numpy as np
import io
import os

# QR URL (GitHub Pages)
url = "https://rdagmr98.github.io/caae/"

# Download stemma CAAE from Wikimedia
logo_url = "https://upload.wikimedia.org/wikipedia/commons/5/58/CoA_mil_ITA_centro_aves.png"
headers = {"User-Agent": "Mozilla/5.0 (CAAE-QR-Generator/1.0)"}
resp = requests.get(logo_url, headers=headers, timeout=20)
resp.raise_for_status()

# Load and remove white background
raw_logo = Image.open(io.BytesIO(resp.content)).convert("RGBA")
logo_arr = np.array(raw_logo)
r, g, b, a = logo_arr[:,:,0], logo_arr[:,:,1], logo_arr[:,:,2], logo_arr[:,:,3]
# Make near-white pixels transparent (smooth edges with gradual alpha reduction)
near_white = (r > 220) & (g > 220) & (b > 220)
# Proportional alpha: fully transparent at white (255), half at threshold 220
alpha_factor = np.clip((r.astype(float) - 220) / 35, 0, 1) * near_white
logo_arr[:,:,3] = np.where(near_white, (255 * (1 - alpha_factor)).astype(np.uint8), a)
transparent_logo = Image.fromarray(logo_arr)

# Save transparent stemma PNG for use in the website
script_dir = os.path.dirname(os.path.abspath(__file__))
stemma_out = os.path.join(script_dir, "stemma_caae.png")
transparent_logo.save(stemma_out)
print(f"Transparent stemma saved to: {stemma_out}")

# Resize for QR center logo
logo = transparent_logo.copy()
logo_size = 120
logo.thumbnail((logo_size, logo_size), Image.LANCZOS)
logo_w, logo_h = logo.size

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
).convert("RGBA")

# Resize to standard size
qr_img = qr_img.resize((600, 600), Image.LANCZOS)

# Create plain white circle background for stemma (no gold ring)
pad = 18
circ_w = logo_w + pad
circ_h = logo_h + pad
circle_bg = Image.new("RGBA", (circ_w, circ_h), (255, 255, 255, 0))
ImageDraw.Draw(circle_bg).ellipse((0, 0, circ_w - 1, circ_h - 1), fill=(255, 255, 255, 255))

# Paste circle then transparent stemma, both centered
circle_pos = ((600 - circ_w) // 2, (600 - circ_h) // 2)
qr_img.paste(circle_bg, circle_pos, circle_bg)
logo_pos = ((600 - logo_w) // 2, (600 - logo_h) // 2)
qr_img.paste(logo, logo_pos, logo)

# Save final QR
output_path = os.path.join(os.path.expanduser("~"), "Desktop", "CAAE_QRCode.png")
final = qr_img.convert("RGB")
final.save(output_path, dpi=(300, 300))

print(f"QR code saved to: {output_path}")
print(f"Points to: {url}")
print(f"Size: {final.size}")
