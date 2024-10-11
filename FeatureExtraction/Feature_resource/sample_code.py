import csv
import requests
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import numpy as np

# Set the path for Tesseract (modify if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust the path if needed

# Function to preprocess the image
def preprocess_image(img):
    # Convert to grayscale
    img = img.convert('L')
    # Apply thresholding to enhance text
    img = img.point(lambda p: p > 128 and 255)
    return img

# Function to extract text from an image URL
def extract_text_from_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = preprocess_image(img)
    
    # Convert image to NumPy array for Tesseract
    img_array = np.array(img)
    
    text = pytesseract.image_to_string(img_array)
    return text

# Function to process CSV and save output text
def convert_images_to_text(csv_file, output_file):
    with open(csv_file, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Open output file to write the extracted text
        with open(output_file, mode='w', encoding='utf-8') as output:
            for row in reader:
                image_url = row['image_link']  # Assuming 'image_link' is the column name in the CSV
                extracted_text = extract_text_from_image(image_url)
                
                # Write the extracted text to the output file
                output.write(f"Image URL: {image_url}\n")
                output.write(f"Extracted Text:\n{extracted_text}\n")
                output.write("=" * 50 + "\n")  # Divider between images

# Example usage
csv_file = r'F:\DownloadF\amazoneDataset\student_resource 3\dataset\sample_test.csv'  # Replace with the path to your CSV file
output_file = 'output.txt'  # Output file for the extracted text

convert_images_to_text(csv_file, output_file)
