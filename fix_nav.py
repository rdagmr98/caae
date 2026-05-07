import re, os, glob

caae = r'C:\Users\Gianmarco\caae'

files = glob.glob(os.path.join(caae, '*.html')) + glob.glob(os.path.join(caae, '**', '*.html'))

for fp in sorted(files):
    with open(fp, encoding='utf-8') as f:
        content = f.read()
    orig = content

    # Remove the stemma img inside .nav-brand (top-left nav logo)
    # Matches: <img src="stemma_caae.png" alt="Stemma CAAE"> or ../stemma_caae.png
    pattern = r'(<a\s+href="[^"]*"\s+class="nav-brand">)\s*<img[^>]*stemma_caae[^>]*>\s*'
    content = re.sub(pattern, r'\1\n    ', content)

    if content != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'FIXED: {os.path.relpath(fp, caae)}')
    else:
        print(f'skip:  {os.path.relpath(fp, caae)}')
