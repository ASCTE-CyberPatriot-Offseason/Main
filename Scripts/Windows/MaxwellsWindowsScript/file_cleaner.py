import os
#test

# File types to delete
fileTypes = [".jpg", ".png", ".aac", ".ac3", ".avi", ".aiff", ".bat", ".bmp", ".exe", ".flac", ".gif", ".jpeg", ".mov", ".m3u", ".m4p",
             ".mp2", ".mp3", ".mp4", ".mpeg4", ".midi", ".msi", ".ogg", ".png", ".txt", ".sh", ".wav", ".wma", ".vqf", ".pcap", ".zip",
             ".pdf", ".json"]

# Directory path to exclude (e.g., "Cyber Patriot Personnel")
user = os.getlogin()
exclude_directory = ["C://Program Files/Cyber Patriot Personnel", "C://Users//"+user+"//Desktop"]

# Directories to search through
userDirectories = ["C://Users"]

for root_dir in userDirectories:
    for root, dirs, files in os.walk(root_dir):
        # Skip the exclude directory
        if exclude_directory in root:
            continue

        # Delete files of specified types
        for file in files:
            if any(file.endswith(ft) for ft in fileTypes):
                try:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
