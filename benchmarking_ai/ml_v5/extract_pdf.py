
import os
from pypdf import PdfReader

files = [
    r"D:\Hamza\Family\Hamza\Certifications\aipm_credential_2026_neuefische.pdf",
    r"D:\Hamza\Family\Hamza\Certifications\AIPM_Graduation_Event.pdf"
]

for file_path in files:
    print(f"--- Processing {os.path.basename(file_path)} ---")
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        print(text)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    print("------------------------------------------------")
