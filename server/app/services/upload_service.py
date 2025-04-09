import os
from app.utils.csv_parser import parse_csv

def handle_csv_upload(file, upload_folder):
    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    data = parse_csv(filepath)

    return data
