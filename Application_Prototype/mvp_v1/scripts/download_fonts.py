
import os
import requests
import re

# Configuration
FONTS = [
    {
        "family": "Inter",
        "css_url": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
        "weights": [300, 400, 500, 600, 700]
    },
    {
        "family": "Outfit",
        "css_url": "https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap",
        "weights": [400, 500, 600, 700, 800]
    }
]

BASE_DIR = r"d:\SpicedProjects\Projects\ai-compass\Application_Prototype\mvp_v1\frontend\src\assets\fonts"
CSS_OUTPUT = r"d:\SpicedProjects\Projects\ai-compass\Application_Prototype\mvp_v1\frontend\src\assets\fonts\fonts.css"

def download_file(url, filepath):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    return False

def process_fonts():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
        
    final_css = "/* Local Fonts - GDPR Compliant */\n\n"
    
    # Headers to mimic a modern browser so Google sends us WOFF2
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print(f"Downloading fonts to {BASE_DIR}...")
    
    for font in FONTS:
        print(f"Processing {font['family']}...")
        
        # 1. Fetch the CSS from Google
        try:
            r = requests.get(font['css_url'], headers=headers)
            css_content = r.text
        except Exception as e:
            print(f"Failed to fetch CSS for {font['family']}: {e}")
            continue
            
        # 2. Parse the CSS to find font URLs
        # Regex to find src: url(https://...) format
        # simpler parsing: split by @font-face blocks
        blocks = css_content.split('@font-face')
        
        for block in blocks:
            if not block.strip(): continue
            
            # Extract font-weight
            weight_match = re.search(r'font-weight:\s*(\d+);', block)
            if not weight_match: continue
            weight = int(weight_match.group(1))
            
            if weight not in font['weights']:
                continue
                
            # Extract URL
            url_match = re.search(r'url\((https?://[^)]+)\)', block)
            if not url_match: continue
            url = url_match.group(1)
            
            # Generate filename
            extension = url.split('.')[-1]
            filename = f"{font['family'].lower()}-{weight}.{extension}"
            filepath = os.path.join(BASE_DIR, filename)
            
            # Download font file
            print(f"  Downloading {filename}...")
            if download_file(url, filepath):
                # Add to our local CSS
                local_css = f"""
@font-face {{
  font-family: '{font['family']}';
  font-style: normal;
  font-weight: {weight};
  font-display: swap;
  src: url('./assets/fonts/{filename}') format('woff2');
}}
"""
                final_css += local_css
            else:
                print("    Failed to download file.")

    # Write the CSS file
    try:
        with open(CSS_OUTPUT, 'w') as f:
            f.write(final_css)
        print(f"Done! CSS written to {os.path.abspath(CSS_OUTPUT)}")
    except Exception as e:
        print(f"Error writing CSS file: {e}") 

if __name__ == "__main__":
    process_fonts()
