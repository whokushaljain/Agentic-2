import base64

image_path = '/Users/kushal/.gemini/antigravity/brain/e6deaec8-e84f-4d22-9dd9-c2f5bf9c72d4/media__1777456969377.jpg'
html_path = 'RBL Agentic Payment.html'

with open(image_path, 'rb') as f:
    img_data = f.read()

b64_str = base64.b64encode(img_data).decode('utf-8')
data_uri = f"data:image/jpeg;base64,{b64_str}"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the thumbnail SVG
old_svg_card = """    <!-- Card -->
    <rect x="95" y="350" width="210" height="110" rx="12" fill="#111"></rect>
    <ellipse cx="270" cy="405" rx="55" ry="55" fill="#b8174a" opacity="0.7"></ellipse>"""

new_svg_card = f"""    <!-- Card -->
    <defs>
      <clipPath id="card-clip">
        <rect x="95" y="350" width="210" height="110" rx="12"></rect>
      </clipPath>
    </defs>
    <image x="95" y="350" width="210" height="110" preserveAspectRatio="xMidYMid slice" href="{data_uri}" clip-path="url(#card-clip)" />"""

if old_svg_card in html:
    html = html.replace(old_svg_card, new_svg_card)
    print("Replaced SVG card")
else:
    print("Could not find old SVG card")

# 2. Inject CSS for the actual card
css_inject = f"""    #__bundler_placeholder {{ color: #999; font-size: 14px; }}
    
    /* Injected styles for card image */
    .card-visual {{
      background-image: url('{data_uri}') !important;
      background-size: cover !important;
      background-position: center !important;
      background-repeat: no-repeat !important;
      background-color: transparent !important;
      border: none !important;
    }}
    .card-visual > * {{
      display: none !important;
    }}
"""

old_css_marker = "    #__bundler_placeholder { color: #999; font-size: 14px; }"

if old_css_marker in html and "/* Injected styles for card image */" not in html:
    html = html.replace(old_css_marker, css_inject)
    print("Injected CSS for card-visual")
elif "/* Injected styles for card image */" in html:
    print("CSS already injected")
else:
    print("Could not find old CSS marker")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Done")
