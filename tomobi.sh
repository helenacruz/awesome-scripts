#!/bin/bash

if [ $# -eq 0 ]
then
    echo "Missing input directory"  
    exit 1
else
    echo $1
fi

find $1 -type f -print0 | while read -d $'\0' file; do
    if [[ $file == *.epub ]]
    then
        echo "Trying to convert $file"
        filename=${file%.*}
        ebook-convert "$file" "$filename.mobi"
    fi
done
