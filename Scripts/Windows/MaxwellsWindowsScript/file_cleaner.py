#delete files of certain types in all directories except for cyber patriot personel directory
#Can probably localize it to program files directory and users directory (research probably)
import os

#list all file types to delete
fileTypes = [".jpg", ".png", ".aac", ".ac3", ".avi", ".aiff", ".bat", ".bmp", ".exe", ".flac", ".gif", ".jpeg", ".mov", ".m3u", ".m4p"
            , ".mp2", ".mp3", ".mp4", ".mpeg4", ".midi", ".msi", ".ogg", ".png", ".txt", ".sh", ".wav",".wma", ".vqf", ".pcap", ".zip",
            ".pdf", ".json"]
#directories to search through
userDirectories = os.listdir("C://Users")
print(userDirectories)
for x in range(len(userDirectories) - 1):
    userDirectories[x] = "C://Users//" + userDirectories[x]
for directory in userDirectories:
    for type in fileTypes:
        for file in os.listdir(directory):
            if file.endswith(type):
                os.remove(file)
                print(file)
            else:
                print(file)

