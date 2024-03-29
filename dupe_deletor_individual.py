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
                duplicates.append((file_path, file_hash))
            else:
                file_hash_map[file_hash] = file_path

    return duplicates


def export_duplicates_to_csv(duplicates, csv_filename):
    """
    Export duplicate files to a CSV file.
    """
    with open(csv_filename, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["File Path", "File Hash"])
        csv_writer.writerows(duplicates)


def delete_duplicates(duplicates):
    """
    Delete duplicate files one by one with user consent.
    """
    for duplicate in duplicates:
        file_path, _ = duplicate
        print(f"Delete {file_path}? (y/n)")
        user_input = input().strip().lower()
        if user_input == "y":
            os.remove(file_path)
            print(f"{file_path} deleted.")
        else:
            print(f"{file_path} not deleted.")


if __name__ == "__main__":
    directory = input("Enter the directory to search for duplicates: ").strip()
    duplicates = find_duplicates(directory)

    if duplicates:
        csv_filename = "./data/duplicate_files.csv"
        export_duplicates_to_csv(duplicates, csv_filename)
        print(f"Duplicate files exported to {csv_filename}")

        print("Do you want to delete duplicate files? (y/n)")
        user_input = input().strip().lower()
        if user_input == "y":
            delete_duplicates(duplicates)
            print("All Duplicate Files Deleted Successfully")
        else:
            print("Duplicate files not deleted.")
    else:
        print("No duplicate files found.")
