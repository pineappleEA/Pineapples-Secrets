#!/bin/bash

#sleep random amount of time
sleep $[ ( $RANDOM % 60 )  + 1 ]s
sleep $[ ( $RANDOM % 10 )  + 1 ]m

#sleep another 3 minutes
sleep 10m

OVPN=$(find /etc/openvpn/configs -type f | shuf -n 1)
vpnify sudo openvpn --config $OVPN --auth-user-pass authentication.txt --daemon
sleep 12s
ZIP_FILE=$(vpnify python3 /home/pi/yuzu/Downloader.py)
sudo killall openvpn
VER=$(echo $ZIP_FILE | grep -o "[0-9][0-9][0-9]*")

#check, if there's a newer version available
if [ -z "$ZIP_FILE" ]
then
    exit 0
fi

#upload to github and store the link
bash git-src.sh $VER
URL=$"https://github.com/pineappleEA/pineapple-src/releases/tag/EA-"$VER
rm YuzuEA-*

#edit the html file
HTMLLINE=$"<a href="$URL">Yuzu EA "$VER"</a><br>"

#push to github
cd pineappleEA.github.io
git pull
sed -i "/link-goes-here/a${HTMLLINE}" index.html
git add --all
git commit -m "update link for $VER"
git push
