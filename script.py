import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, error

def remove_metadata_from_mp3(directory_path):
    """
    Removes metadata from all MP3 files in the specified directory.

    Args:
        directory_path (str): Path to the directory containing MP3 files.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        return

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.mp3'):
                file_path = os.path.join(root, file)
                try:
                    # Load the MP3 file
                    audio = MP3(file_path, ID3=ID3)

                    # Delete the ID3 metadata
                    if audio.tags:
                        audio.delete()
                        audio.save()
                        print(f"Metadata removed from: {file_path}")
                    else:
                        print(f"No metadata found in: {file_path}")
                except error as e:
                    print(f"Failed to process {file_path}: {e}")

if __name__ == "__main__":
    directory = input("Enter the path to the directory containing MP3 files: ").strip()
    remove_metadata_from_mp3(directory)
