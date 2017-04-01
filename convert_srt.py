import sys
import codecs
import os.path
from bs4 import BeautifulSoup

srtfiles = []

if len(sys.argv) < 2:
    print("Usage: -all folder for sending all *.srt files recursively in folder" +
          " or file1.srt ... fileN.srt")
    sys.exit(1)

# converts all files recursively in a folder
elif len(sys.argv) == 3 and sys.argv[1] == "-all": # -all
    directory = sys.argv[2]
    if os.path.isdir(directory):
        for root, subFolders, files in os.walk(directory):
            for file in files:
                relDir = os.path.relpath(root, directory)
                relFile = os.path.join(relDir, file)
                if file.endswith(".srt"):
                    srtfiles += [relFile]
    else:
        print(directory + " is not a valid directory")
        sys.exit(1)

# folder missing
elif len(sys.argv) != 3 and sys.argv[1] == "-all":
    print("Usage: -all folder for sending all *.srt files recursively in folder" +
          " or file1.srt ... fileN.srt")
    sys.exit(1)

# converts all given files
else:
    for file in sys.argv[1:]:
        if not file.endswith(".srt"):
            print(file + " is not a valid .srt file")
        elif os.path.isfile(file):
            srtfiles += [file]
        else:
            print(file + " is not a valid file")

for srtfile in srtfiles:
    print("Trying to convert " + srtfile)
    file = open(srtfile, "rb")
    soup = BeautifulSoup(file.read(), 
                         "html.parser", # just to remove the warning  
                         exclude_encodings=["IBM855", "windows-1255"]) # for some 
                        # reason it was detecting portuguese subtitles as these 
                        # two so oopsy
    encoding = soup.original_encoding

    if encoding == "utf-8":
        print(srtfile + " is already in UTF-8\n")
        continue

    print(srtfile + " is in " + encoding)
    file.close()

    with codecs.open(srtfile, "r", encoding) as source_file:
        filename = os.path.splitext(srtfile)[0] + "utf.srt" 
        with codecs.open(filename, "w", "utf-8") as target_file:
            try:
                contents = source_file.read()
                target_file.write(contents)
                print("Successfully converted " + srtfile + "\n")
            except UnicodeDecodeError:
                print("Error converting " + srtfile + " from " + encoding + "\n")

print("Done!")
