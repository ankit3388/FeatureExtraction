import csv
import requests
from io import BytesIO
from PIL import Image
import easyocr
import numpy as np
import json

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Function to extract text from an image URL
def extract_text_from_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = img.convert('RGB')  # Convert image to RGB format
    img_array = np.array(img)  # Convert PIL image to NumPy array
    
    results = reader.readtext(img_array)
    # Combine text results
    text = ' '.join([result[1] for result in results])
    return text

# Function to process CSV and save output text in JSON format
def convert_images_to_text(csv_file, output_file):
    output_data = []
    
    with open(csv_file, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for index, row in enumerate(reader):
            image_url = row['image_link']  # Assuming 'image_link' is the column name in the CSV
            extracted_text = extract_text_from_image(image_url)
            
            # Collect data in a dictionary
            data = {
                "index": index,
                "image_link": image_url,
                "group_id": row.get('group_id', ''),  # Replace with the actual column name if different
                "entity_name": row.get('entity_name', ''),  # Replace with the actual column name if different
                "text": extracted_text
            }
            
            output_data.append(data)
    
    # Write the collected data to a JSON file
    with open(output_file, mode='w', encoding='utf-8') as jsonfile:
        json.dump(output_data, jsonfile, indent=4)

# Example usage
csv_file = r'F:\DownloadF\amazoneDataset\student_resource 3\dataset\sample_test.csv'  # Replace with the path to your CSV file
output_file = 'output2.json'  # Output file for the extracted text

convert_images_to_text(csv_file, output_file)
