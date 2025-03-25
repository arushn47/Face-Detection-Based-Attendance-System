import csv

with open("data/attendance/Class 4/2025-03-24.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)  # Ensure the structure matches what you're expecting
