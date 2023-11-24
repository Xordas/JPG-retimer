import os
import datetime
import piexif
import concurrent.futures
import time
import shutil
import re

# Define the path to the destination directory
destination_path = 'F:'

# Create a new directory for this run
run_directory = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
destination_path = os.path.join(destination_path, run_directory)
os.makedirs(destination_path, exist_ok=True)

def process_file(file):
    file_path = os.path.join(folder_path, file)
    processed = 0
    moved = 0

    # Check if the file is a jpg
    if os.path.splitext(file)[1].lower() == '.jpg':
        try:
            exif_dict = piexif.load(file_path)
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = today.strftime("%Y:%m:%d %H:%M:%S")
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, file_path)
            print(f'Updated {file_path} successfully')
            processed = 1

            # Define the new location for the file
            new_location = os.path.join(destination_path, file)

            # Move the file to the new location
            shutil.move(file_path, new_location)
            print(f'Moved {file_path} to {new_location} successfully')
            moved = 1

        except Exception as e:
            print(f'Failed to update and/or move {file_path}. {e}')
    return processed, moved

print('Starting')

start_time = time.time()  # Record the start time

# Get today's date
today = datetime.datetime.now()

# Define the path to the removable drive and the folder
folder_path = os.path.join('D:', 'DCIM', '100NCD60')

try:
    files = os.listdir(folder_path)
except OSError as e:
    print(f'Could not list the directory. {e}')
    exit(1)

print(f'Found {len(files)} files')

with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
    results = list(executor.map(process_file, files))

processed_counts, moved_counts = zip(*results)

end_time = time.time()  # Record the end time

total_time = end_time - start_time  # Calculate the total time

print(f'Processed {sum(processed_counts)} images and moved {sum(moved_counts)} images in {total_time:.2f} seconds')
print("Made by Xordas")
input("Press Enter to close...")
