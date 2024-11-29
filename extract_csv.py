import re
import csv

# Define file paths
input_file = 'process_data.txt'  # Replace with your text file
output_file = 'college_data.csv'

# Initialize lists to hold the data
institute_codes = []
college_data = []
course_codes = []
course_data = []
status_data = []
level_data = []
category_data = []
cutoff_rank_data = []
score_data = []

# Regex patterns to capture different parts of the data
institute_pattern = re.compile(r'(\d{4})\s*-\s*(.*)')  # e.g., 1002 - Government College
course_pattern = re.compile(r'(\d{9})\s*-\s*(.*)')  # e.g., 100219110 - Civil Engineering
rank_score_pattern = re.compile(r'(\d+)\s*\(([\d\.]+)\)')  # e.g., 45820 (80.7328826)

with open(input_file, 'r') as file:
    lines = file.readlines()

current_institute = None
current_course = None
current_status = None
current_level = None

for line in lines:
    line = line.strip()
    
    # Match institute
    institute_match = institute_pattern.match(line)
    if institute_match:
        current_institute = institute_match.group(1)
        institute_name = institute_match.group(2)
        institute_codes.append(current_institute)
        college_data.append(institute_name)
        continue
    
    # Match course
    course_match = course_pattern.match(line)
    if course_match:
        current_course = course_match.group(1)
        course_name = course_match.group(2)
        course_codes.append(current_course)
        course_data.append(course_name)
        continue
    
    # Match status
    if "Status:" in line:
        current_status = next(lines).strip()  # Get the next line for status
        status_data.append(current_status)
        continue

    # Match level
    if "Level" in line or "State Level" in line:
        current_level = "State Level"  # Since it's always state level, we directly append this
        level_data.append(current_level)
        continue
    
    # Match category (e.g., GOPENS, GSCS)
    if re.match(r'[A-Z]{5,}', line):
        category_data.append(line)
        continue

    # Match rank and score
    rank_score_match = rank_score_pattern.match(line)
    if rank_score_match:
        cutoff_rank_data.append(rank_score_match.group(1))
        score_data.append(rank_score_match.group(2))
        continue

# Write the data to a CSV file
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header row
    writer.writerow(['Institute Code', 'Institute Name', 'Course Code', 'Course Name', 'Status', 'Level', 'Category', 'Cutoff Rank', 'Score'])
    
    # Write data rows
    for i in range(len(institute_codes)):
        writer.writerow([
            institute_codes[i] if i < len(institute_codes) else '',
            college_data[i] if i < len(college_data) else '',
            course_codes[i] if i < len(course_codes) else '',
            course_data[i] if i < len(course_data) else '',
            status_data[i] if i < len(status_data) else '',
            level_data[i] if i < len(level_data) else '',
            category_data[i] if i < len(category_data) else '',
            cutoff_rank_data[i] if i < len(cutoff_rank_data) else '',
            score_data[i] if i < len(score_data) else ''
        ])

print(f"Data extraction complete. Saved to {output_file}.")
