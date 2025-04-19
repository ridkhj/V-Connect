import os
from app.utils.csv_parser import csv_parser

def upload_service(file, upload_folder):
    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    data = csv_parser(filepath)

    return data
