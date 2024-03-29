import os
import csv
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


def delete_duplicates(duplicates):
    """
    Delete duplicate files with user consent.
    """
    print("List of duplicate files found:")
    for duplicate in duplicates:
        print(duplicate)

    print("Do you want to delete all duplicate files? (y/n)")
    user_input = input().strip().lower()
    if user_input == "y":
        deleted_files = []
        for duplicate in duplicates:
            try:
                os.remove(duplicate)
                deleted_files.append(duplicate)
            except Exception as e:
                print(f"Error deleting {duplicate}: {str(e)}")

        if deleted_files:
            with open("./data/duplicates_deleted.csv", "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["File Path"])
                csv_writer.writerows([[file_path] for file_path in deleted_files])
            print("All Duplicate Files Deleted Successfully")
        else:
            print("No duplicate files were deleted.")
    else:
        print("Duplicate files not deleted.")


if __name__ == "__main__":
    directory = input("Enter the directory to search for duplicates: ").strip()
    duplicates = find_duplicates(directory)

    if duplicates:
        delete_duplicates(duplicates)
    else:
        print("No duplicate files found.")
