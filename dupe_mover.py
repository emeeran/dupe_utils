import os
import shutil
import hashlib


def get_file_hash(file_path):
    """
    Calculate the hash of a file.
    """
    hasher = hashlib.md5()
    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_duplicates(directory):
    """
    Find duplicate files in a directory and its subdirectories.
    """
    file_hash_map = {}
    duplicates = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            if file_hash in file_hash_map:
                duplicates.append(file_path)
            else:
                file_hash_map[file_hash] = file_path

    return duplicates


def move_duplicates_to_directory(duplicates, dest_directory):
    """
    Move duplicate files to a destination directory.
    """
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    for duplicate in duplicates:
        filename = os.path.basename(duplicate)
        dest_path = os.path.join(dest_directory, filename)
        shutil.move(duplicate, dest_path)
        print(f"Moved {duplicate} to {dest_path}")


if __name__ == "__main__":
    directory = input("Enter the directory to search for duplicates: ").strip()
    duplicates = find_duplicates(directory)

    if duplicates:
        destination_directory = os.path.join(directory, "duplicates_found")
        move_duplicates_to_directory(duplicates, destination_directory)
        print("Duplicates moved to 'duplicates_found' directory.")
    else:
        print("No duplicate files found.")
