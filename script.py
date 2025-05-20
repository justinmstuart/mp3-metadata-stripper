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

    metadata_removed = 0
    no_metadata_found = 0
    failed_count = 0

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
                        metadata_removed += 1
                        print(f"Metadata removed from: {file_path}")
                    else:
                        no_metadata_found += 1
                        print(f"No metadata found in: {file_path}")
                except error as e:
                    failed_count += 1
                    print(f"Failed to process {file_path}: {e}")
                except OSError as e:
                    failed_count += 1
                    print(f"File system error processing {file_path}: {e}")
                except KeyboardInterrupt:
                    print("Process interrupted by user.")
                    raise

    return {
        "metadata_removed": metadata_removed,
        "no_metadata_found": no_metadata_found,
        "failed_count": failed_count
    }

if __name__ == "__main__":
    # Get the target directory from the user
    directory = input("Enter the path to the directory containing MP3 files: ").strip()

    print()
    print("Starting to process MP3 files 🎵")
    print()

    result = remove_metadata_from_mp3(directory)
    print()

    print("Processing complete. 🥳")
    print()
    print("-" * 40)
    print(f"✅ Successfully removed meta from {result['metadata_removed']} files.")
    print(f"⚠️ Metadata not found in {result['no_metadata_found']} files.")
    print(f"🛑 Failed to process {result['failed_count']} files.")
    print("-" * 40)
    print()
