
import time
import os

def measure_read_speed(file_path):
    start_time = time.time()
    with open(file_path, 'r') as file:
        file.read()
    end_time = time.time()
    return end_time - start_time

def measure_read_performance(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            data_size = os.path.getsize(file_path)
            read_time = measure_read_speed(file_path)
            print(f"Read time for {filename} (size: {data_size} bytes) in {read_time} seconds")
# Example Usage
folder_path = "C:/Users/vishn/OneDrive/Desktop/FuseFS/backup_folder"
measure_read_performance(folder_path)
