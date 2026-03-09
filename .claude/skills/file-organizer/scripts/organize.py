
import os
import shutil
import sys

def organize_files(target_path):
    if not os.path.isdir(target_path):
        print(f"Error: Target path '{target_path}' does not exist or is not a directory.")
        sys.exit(1)

    print(f"Organizing files in '{target_path}'...")

    for item in os.listdir(target_path):
        item_path = os.path.join(target_path, item)

        if os.path.isfile(item_path):
            file_name, file_extension = os.path.splitext(item)
            
            if file_extension:
                folder_name = file_extension.lstrip('.')
            else:
                folder_name = "No_Extension"
            
            destination_folder = os.path.join(target_path, folder_name)

            try:
                os.makedirs(destination_folder, exist_ok=True)
                shutil.move(item_path, destination_folder)
                print(f"Moved '{item}' to '{folder_name}'")
            except Exception as e:
                print(f"Failed to move '{item}': {e}")
        elif os.path.isdir(item_path):
            print(f"Skipping directory: '{item}'")
        else:
            print(f"Skipping unknown item: '{item}'")

    print("File organization complete.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python organize.py <target_directory>")
        sys.exit(1)
    
    target_directory = sys.argv[1]
    organize_files(target_directory)
