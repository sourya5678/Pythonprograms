import os
import docx
import PyPDF2
import cv2
import pytesseract
from PIL import Image

# --- OCR SETTINGS ---
# If on Windows, uncomment and set your Tesseract path:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_from_pdf(file_path):
    """Extracts text from PDF using PyPDF2 (Policy-friendly)."""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            print(f"\n--- Found {len(reader.pages)} pages in PDF ---")
            
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                print(f"\n[ PAGE {i + 1} ]")
                print("-" * 30)
                print(text.strip() if text else "[No readable text found on this page]")
                print("-" * 30)
    except Exception as e:
        print(f"Error reading PDF: {e}")

def extract_from_docx(file_path):
    """Extracts text from Word documents."""
    try:
        doc = docx.Document(file_path)
        print(f"\n--- Extracting DOCX Content ---")
        for para in doc.paragraphs:
            if para.text.strip():
                print(para.text)
    except Exception as e:
        print(f"Error reading DOCX: {e}")

def extract_from_image(file_path):
    """Extracts text from Images using OpenCV and Tesseract."""
    try:
        img = cv2.imread(file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Simple thresholding for better clarity
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        text = pytesseract.image_to_string(thresh)
        print(f"\n--- Extracting Image Content ---")
        print("-" * 30)
        print(text.strip() if text.strip() else "[No text detected]")
        print("-" * 30)
    except Exception as e:
        print(f"Error reading Image: {e}")

def main():
    path = input("Enter file path (Image, PDF, or DOCX): ").strip().replace('"', '')
    
    if not os.path.exists(path):
        print("Error: File not found.")
        return

    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        extract_from_pdf(path)
    elif ext == ".docx":
        extract_from_docx(path)
    elif ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        extract_from_image(path)
    else:
        print(f"Format {ext} not supported.")

if __name__ == "__main__":
    main()