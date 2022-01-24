#!/usr/bin/env bash

#Define IO vars
HOST=$(echo $(hostname) | sed "s,\.$(hostname -d),,")
OUTFILE=$HOST"_profile.txt"

#Add json support //TODO -- easier with a python library

#function setn_IFS {
#  IFS="\n"
#}

#function reset_IFS {
#  IFS=$" \t\n"
#}

echo "Writing output of $HOST to $OUTFILE"

#Main

echo '{' >> $OUTFILE

echo 'uname -a: '$(uname -a)',' >> $OUTFILE

echo 'host: '$HOST',' >> $OUTFILE

echo 'domain: '$(hostname -d)',' >> $OUTFILE

echo 'date: '$(date)',' >> $OUTFILE

echo 'lsblk: ' >> $OUTFILE
lsblk >> $OUTFILE

echo 'lsscsi: ' >> $OUTFILE
lsscsi >> $OUTFILE

echo "ip -h -s link: " >> $OUTFILE
#while read i; do echo -e "\t"$i >> $OUTFILE; done <<< $(ip -h -s link | sed 's,link.*,,')
ip -h -s link | sed 's,link.*,,' >> $OUTFILE


echo "ethtool \$INTERFACE: " >> $OUTFILE
INTERFACES=$(netstat -i | awk '{print $1}' | sed '1,2d')
for i in $INTERFACES; do ethtool $i >> $OUTFILE; done

echo "lscpu: " >> $OUTFILE
lscpu | sed 's,Flags.*,,' >> $OUTFILE


echo "dmidecode-noroot: " >> $OUTFILE
for i in $(ls /sys/devices/virtual/dmi/id/{board,chassis}_*); do echo $i": "$(grep '' $i) >> $OUTFILE; done

