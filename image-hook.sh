#!/bin/bash

# init
# start
# download
DIR=$(pwd)
log="/home/stephen/stephenskywatcher/image-hook.log"

get_exif() {
    exifdata=$(exiftool -T -AEBBracketValue -ISO -APERTURE -SHUTTERSPEED $1)
    read -ra arr <<<"$exifdata"
    aeb=${arr[0]}
    iso=${arr[1]}
    aperture=${arr[2]}
    shutterspeed=${arr[3]}
    filename="${1##*/}"
    # echo "${filename}    +/- ${aeb}  ISO${iso}  f/${aperture}  ${shutterspeed}" >> $log    

    # fmt="%-30s%-8s%-8s%-8s%-8s\n"
    echo "'"$DIR/$filename"'" >> $log
    printf "±AEB %-7s ISO%-7s ƒ/%-7s %-7s\n" "$aeb" "$iso" "$aperture" "$shutterspeed" >> $log

}
# echo "" > $log
# get_exif /home/stephen/stephenskywatcher/captures/test_bracketing/lights/03-25-24_22:13:56-capt0000.jpg
# get_exif /home/stephen/stephenskywatcher/captures/test_bracketing/lights/03-25-24_22:49:20-capt0001.jpg
# get_exif /home/stephen/stephenskywatcher/captures/test_bracketing/lights/03-25-24_22:49:20-capt0002.jpg

if [ $ARGUMENT ]; then
    BASENAME=$(basename "$ARGUMENT")
    FILE="$DIR/$BASENAME"
    ACTION=download
    get_exif $FILE
fi

