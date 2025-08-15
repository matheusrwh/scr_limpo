import os
import requests
import zipfile
from io import BytesIO
import shutil

class Downloader:
    def __init__ (self, zip_url, raw_dir):
        self.zip_url = zip_url
        self.raw_dir = raw_dir

    def download_zip(self):
        response = requests.get(self.zip_url)
        response.raise_for_status()
        return BytesIO(response.content)
    
    def extract_zip(self, zip_bytes, extract_to):
        with zipfile.ZipFile(zip_bytes) as z:
            z.extractall(extract_to)

    def move_files(self, src_dir):
        for filename in os.listdir(src_dir):
            src_path = os.path.join(src_dir, filename)
            dest_path = os.path.join(self.raw_dir, filename)
            if os.path.isfile(src_path):
                shutil.move(src_path, dest_path)

    def run(self):
        temp_extract_dir = 'temp_extract'
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(temp_extract_dir, exist_ok=True)
        zip_bytes = self.download_zip()
        self.extract_zip(zip_bytes, temp_extract_dir)
        self.move_files(temp_extract_dir)
        shutil.rmtree(temp_extract_dir)
