import cv2
import pytesseract
import platform
import os

def get_tesseract_cmd():
    """Locate Tesseract based on the OS for portability."""
    if platform.system() == "Windows":
        # Default path for Windows; adjust if you installed it elsewhere
        return r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    return "tesseract" # Linux and Mac usually have it in system PATH

def process_image_for_ocr(image_path):
    # 1. Load the image
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not read the image.")
        return

    # 2. Convert to Grayscale
    # Computers don't need color to read; grayscale simplifies the data
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Apply Adaptive Thresholding
    # This handles uneven lighting (e.g., a shadow falling across the page)
    processed_img = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )

    # 4. Configure Tesseract
    pytesseract.pytesseract.tesseract_cmd = get_tesseract_cmd()
    
    # --psm 3: Automatic page segmentation (works for paragraphs/poems)
    custom_config = r'--oem 3 --psm 3'
    
    # 5. Extract Text
    text = pytesseract.image_to_string(processed_img, config=custom_config)

    # Output formatting
    print("\n" + "="*40)
    print("EXTRACTED TEXT")
    print("="*40 + "\n")
    print(text.strip())
    print("\n" + "="*40)

if __name__ == "__main__":
    path = input("Enter image path (jpg, jpeg, png, etc.): ").strip().replace('"', '')
    process_image_for_ocr(path)