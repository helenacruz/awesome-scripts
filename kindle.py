import argparse
import os.path
import ntpath
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from subprocess import call

# emails are limited to 25 attachments or 25mb
MAX_ATTACHMENTS = 25
MAX_SIZE = 26214400 # 25mb in bytes

me = "YOUR_EMAIL"
password = "YOUR PASSWORD"
kindle = "YOUR KINDLE EMAIL"

pdf_files = []
epub_files = []
mobi_files = []

# divide files by type

def parse_files(lst):
    global pdf_files
    global epub_files
    global mobi_files
    lst = list(set(lst)) # remove duplicates
    for file in lst:
        if file.endswith(".pdf"):
            pdf_files += [file]
        elif file.endswith(".epub"):
            epub_files += [file]
        elif file.endswith(".mobi"):
            mobi_files += [file]
        else:
            print(file + " is not a valid file. Needs to be either .pdf, .epub or .mobi.")

# check if they actually exist

def verify_files():
    for pdf_file in pdf_files:
        if not os.path.isfile(pdf_file):
            pdf_files.remove(pdf_file)
            print("Unable to locate the file " + pdf_file)
    for epub_file in epub_files:
        if not os.path.isfile(epub_file):
            epub_files.remove(epub_file)
            print("Unable to locate the file " + epub_file)
    for mobi_file in mobi_files:
        if not os.path.isfile(mobi_file):
            mobi_files.remove(mobi_file)
            print("Unable to locate the file " + mobi_file)

# convert the files

def convert_files():
    print("Converting files...")
    global mobi_files
    for epub_file in epub_files:
        mobi_name = epub_file[:-4] + "mobi"
        print("Trying to convert " + epub_file)
        if os.path.isfile(mobi_name):
            print(mobi_name + " already exists.")
            mobi_files += [mobi_name]
        elif call(["ebook-convert", epub_file, mobi_name]) == 0:
            mobi_files += [mobi_name]
            print("Successfully converted " + epub_file + " to .mobi.")
        else:
            print("The conversion of " + epub_file + " was not successful.")
            epub_files.remove(epub_file) # we couldn't convert it so we don't need it

# mail stuff

def connect_to_server():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(me, password)
    return server

def disconnect_from_server(server):
    server.quit()

def send_mail(server, files, subject):
    msg = MIMEMultipart()
    msg['From'] = me
    msg['To'] = kindle
    msg['Subject'] = subject
    for file in files:
        try:
            print("Sending " + file)
            file_name = file.split("/")[-1]
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(file, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(part)
        except:
            print("Could not send " + file)
    msg.attach(MIMEText("", 'html'))
    server.sendmail(me, kindle, msg.as_string())

# make sure we only send 25 attachments or 25mb

def check_limits(files, subject, server):
    to_send = []
    total_size = 0
    attachs = 0
    for file in files:
        file_size = os.path.getsize(file)
        if file_size > MAX_SIZE:
            print(file + " is too big to send. Maximum size is 25mb.")
        elif total_size + file_size < MAX_SIZE and attachs < MAX_ATTACHMENTS:
            to_send += [file]
            total_size += file_size
            attachs += 1
        else:
            total_size = file_size
            attachs = 1
            send_mail(server, to_send, subject)
            to_send = [file]
    if to_send: # send the rest
        send_mail(server, to_send, subject)

def send_files():
    print("Sending files...")
    server = connect_to_server()
    if pdf_files:
        print("Sending pdf files...")
        check_limits(pdf_files, "convert", server)
        print("Done")
    if mobi_files:
        print("Sending mobi files...")
        check_limits(mobi_files, "", server)
        print("Done")
    disconnect_from_server(server)

# application interface

parser = argparse.ArgumentParser()
parser.add_argument("-send",
                    nargs='+',
                    help="sends the files to the kindle"
                    )
parser.add_argument("-all",
                    nargs=1,
                    help="converts if necessary and sends everything in the \
                    folder to the kindle"
                    )

args = parser.parse_args()

if args.send:
    parse_files(args.send)
    verify_files()
    convert_files()
    if pdf_files or mobi_files:
        send_files()

elif args.all:
    directory = args.all[0]
    if os.path.isdir(directory):
        for dir_, _, files in os.walk(directory):
            for file in files:
                relDir = os.path.relpath(dir_, directory)
                relFile = os.path.join(relDir, file)
                if relFile.endswith(".pdf"):
                    pdf_files += [relFile]
                elif relFile.endswith("epub"):
                    epub_files += [relFile]
                elif relFile.endswith(".mobi"):
                    mobi_files += [relFile]
        convert_files()
        if pdf_files or mobi_files:
            send_files()
    else:
        print("Invalid directory name: " + directory)
