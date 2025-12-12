import requests
import zipfile
import io
import os

url = "https://github.com/VAST-AI-Research/TripoSR/archive/refs/heads/main.zip"
target_dir = "TripoSR-main"

print(f"Downloading {url}...")
r = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(r.content))

print("Extracting...")
z.extractall(".")
print("Done!")
