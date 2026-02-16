
import os
from pypdf import PdfReader

files = [
    r"D:\Hamza\Family\Hamza\Certifications\aipm_credential_2026_neuefische.pdf",
    r"D:\Hamza\Family\Hamza\Certifications\AIPM_Graduation_Event.pdf"
]

output_file = r"d:\SpicedProjects\Projects\ai-compass\benchmarking_ai\ml_v5\pdf_content_fixed.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for file_path in files:
        f.write(f"--- Processing {os.path.basename(file_path)} ---\n")
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            f.write(text)
        except Exception as e:
            f.write(f"Error reading {file_path}: {e}\n")
        f.write("\n------------------------------------------------\n")
    
print("Extraction complete.")
