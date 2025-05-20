"""
Audio Metadata Stripper

This script recursively removes metadata from MP3 and M4A files in a specified directory.
It traverses through all subdirectories to find and process all audio files.

Requirements:
    - Python 3.6+
    - mutagen library (pip install mutagen)

Example usage:
    python script.py
    # Then enter the directory path when prompted
"""

import os
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.id3 import ID3, error

def remove_metadata_from_audio(directory_path):
    """
    Recursively removes metadata from all MP3 and M4A files in the specified directory and its subdirectories.

    Args:
        directory_path (str): Path to the directory containing audio files.
            The path can be absolute or relative to the current working directory.

    Returns:
        dict: Statistics about processed files including counts of metadata removed,
              files without metadata, and failures.

    Notes:
        - This function uses os.walk to recursively traverse all subdirectories.
        - Files with '.mp3' and '.m4a' extensions (case-insensitive) will be processed.
        - Progress messages are printed to the console.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        return {
            "metadata_removed": 0,
            "no_metadata_found": 0,
            "failed_count": 0
        }

    metadata_removed = 0
    no_metadata_found = 0
    failed_count = 0

    # Recursively traverse the directory structure
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_lower = file.lower()
            if file_lower.endswith('.mp3') or file_lower.endswith('.m4a'):
                file_path = os.path.join(root, file)
                try:
                    if file_lower.endswith('.mp3'):
                        # Handle MP3 files
                        audio = MP3(file_path, ID3=ID3)
                        if audio.tags:
                            audio.delete()  # Remove all metadata
                            audio.save()    # Save the file without metadata
                            metadata_removed += 1
                            print(f"Metadata removed from MP3: {file_path}")
                        else:
                            no_metadata_found += 1
                            print(f"No metadata found in MP3: {file_path}")
                    elif file_lower.endswith('.m4a'):
                        # Handle M4A files
                        audio = MP4(file_path)
                        if audio.tags:
                            audio.delete()  # Remove all metadata
                            audio.save()    # Save the file without metadata
                            metadata_removed += 1
                            print(f"Metadata removed from M4A: {file_path}")
                        else:
                            no_metadata_found += 1
                            print(f"No metadata found in M4A: {file_path}")
                except error as e:
                    failed_count += 1
                    print(f"Failed to process {file_path}: {e}")
                except OSError as e:
                    failed_count += 1
                    print(f"File system error processing {file_path}: {e}")
                except KeyboardInterrupt:
                    print("Process interrupted by user.")
                    raise
                except Exception as e:
                    failed_count += 1
                    print(f"Unexpected error processing {file_path}: {str(e)}")

    return {
        "metadata_removed": metadata_removed,
        "no_metadata_found": no_metadata_found,
        "failed_count": failed_count
    }

if __name__ == "__main__":
    # Get the target directory from the user
    directory = input("Enter the path to the directory containing audio files (MP3/M4A): ").strip()

    print()
    print("Starting to process audio files 🎵")
    print()

    result = remove_metadata_from_audio(directory)
    print()

    print("Processing complete. 🥳")
    print()
    print("-" * 40)
    print(f"✅ Successfully removed metadata from {result['metadata_removed']} files.")
    print(f"⚠️ Metadata not found in {result['no_metadata_found']} files.")
    print(f"🛑 Failed to process {result['failed_count']} files.")
    print("-" * 40)
    print()
