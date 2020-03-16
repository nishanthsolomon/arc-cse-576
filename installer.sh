#!/bin/bash

CUR_DIR=`pwd`

while read line; do 
    directory_to_save="$(echo $line | cut -d',' -f1)"
    file_name="$(echo $line | cut -d',' -f2)"
    download_url="$(echo $line | cut -d',' -f3)"
    file_path=${directory_to_save}/${file_name}
    cd $CUR_DIR
    if [ -e $file_path ]
    then
        echo "${file_name} OK."
    else
        mkdir -p -- "$directory_to_save"
        cd $directory_to_save
        wget $download_url
        echo "Downloaded ${file_name}"
    fi

done < downloadables.txt