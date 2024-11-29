import os
import json
import csv

def extract_json_files_from_folder(folder_path):
    # Get all the JSON files from the folder
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    return json_files

def extract_data_from_json(json_file_path):
    # Load the JSON data from a file
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    # Extract the institute summary details
    institute_summary = data.get('institute_summary', {})
    
    # Extract course details, which is a list
    course_details = data.get('course_details', [])
    
    # Combine the institute details with each course
    combined_data = []
    for course in course_details:
        # Merge institute summary with course details
        row = {**institute_summary, **course}
        combined_data.append(row)
    
    return combined_data

def save_to_csv(data, csv_file_path):
    # Check if data is not empty
    if not data:
        print("No data to save.")
        return
    
    # Extract header from keys of the first dictionary
    header = data[0].keys()
    
    # Write the data to a CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

def process_json_files_to_csv(input_folder_path, output_csv_file_path):
    # Get the list of JSON files in the folder
    json_files = extract_json_files_from_folder(input_folder_path)
    
    # Initialize an empty list to store all data
    all_data = []
    
    # Process each JSON file
    for json_file in json_files:
        json_file_path = os.path.join(input_folder_path, json_file)
        json_data = extract_data_from_json(json_file_path)
        all_data.extend(json_data)
    
    # Save the extracted data into a CSV file
    save_to_csv(all_data, output_csv_file_path)
    print(f"Data has been saved to {output_csv_file_path}")

# Example usage:
input_folder_path = 'Colleges Data Scrape\2024-25'
output_csv_file_path = '2024-25.csv'

# Process all JSON files and save the data into a single CSV file
process_json_files_to_csv(input_folder_path, output_csv_file_path)
