import csv
import requests
from io import BytesIO
import keras_ocr
from PIL import Image
import numpy as np
import tensorflow as tf

# Initialize the Keras-OCR pipeline
pipeline = keras_ocr.pipeline.Pipeline()

# Function to extract text from an image URL
def extract_text_from_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = img.convert('RGB')  # Ensure the image is in RGB mode
    
    # Convert image to a NumPy array
    img_array = np.array(img)
    
    # Use the Keras-OCR pipeline to detect and recognize text
    prediction_groups = pipeline.recognize([img_array])
    text = ' '.join([text for box, text in prediction_groups[0]])
    
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
output_file = 'output_kerasocr.txt'  # Output file for the extracted text

convert_images_to_text(csv_file, output_file)
