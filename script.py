"""
MP3 Metadata Stripper

This script recursively removes ID3 metadata from MP3 files in a specified directory.
It traverses through all subdirectories to find and process all MP3 files.

Requirements:
    - Python 3.6+
    - mutagen library (pip install mutagen)

Example usage:
    python script.py
    # Then enter the directory path when prompted
"""

import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, error

def remove_metadata_from_mp3(directory_path):
    """
    Recursively removes metadata from all MP3 files in the specified directory and its subdirectories.

    Args:
        directory_path (str): Path to the directory containing MP3 files.
            The path can be absolute or relative to the current working directory.

    Returns:
        None

    Notes:
        - This function uses os.walk to recursively traverse all subdirectories.
        - Only files with '.mp3' extension (case-insensitive) will be processed.
        - Progress messages are printed to the console.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        return

    # Recursively traverse the directory structure
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                try:
                    # Load the MP3 file with ID3 support
                    audio = MP3(file_path, ID3=ID3)

                    # Check for and remove any ID3 metadata tags
                    if audio.tags:
                        audio.delete()  # Remove all metadata
                        audio.save()    # Save the file without metadata
                        print(f"Metadata removed from: {file_path}")
                    else:
                        print(f"No metadata found in: {file_path}")
                except error as e:
                    print(f"Failed to process {file_path}: {e}")
                except Exception as e:
                    print(f"Unexpected error processing {file_path}: {e}")

if __name__ == "__main__":
    # Get the target directory from the user
    directory = input("Enter the path to the directory containing MP3 files: ").strip()

    print(f"Starting to process MP3 files in: {directory}")
    print("This will recursively search all subdirectories.")

    remove_metadata_from_mp3(directory)

    print("Processing complete.")
