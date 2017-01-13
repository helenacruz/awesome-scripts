# awesome crap
I may have spent more time writing these scripts than actually doing what they do by hand but where's the fun in that?

## tomobi.sh

Converts all the .epub files in the directory (including subdirectories) to .mobi. 
You need [calibre](https://calibre-ebook.com/) to convert them.

```
./tomobi.sh directory-name
```

## kindle.py

Converts .epub to .mobi and sends them to your kindle. It also works with .pdf files by sending an e-mail with the subject "convert" (which results in Amazon converting them for you from .pdf to .mobi). 
You also need [calibre](https://calibre-ebook.com/) to convert them.

To use replace the following variables with your emails and password. 

```
me = "YOUR EMAIL"
password = "YOUR PASSWORD"
kindle = "YOUR KINDLE EMAIL"
```

You can send a few files like this:

```
python3 kindle.py -send file1 file2 ... fileN
```

Or send all files in a folder.

```
python3 kindle.py -all folder
```
