#!/bin/sh

i="$1"
if [ ${#i} -ge 5 ] || [ ${#i} -eq 1 ]
then
  rm -rf $1/*
fi
for i in $(find $2);
do
  if [ "${i}" != "$2" ]
  then
    file=$(echo $(basename ${i}) | xxd -r -p | openssl enc -d -aes-256-cbc -pass file:$3) \
    && head $i 1>/dev/null 2>/dev/null\
    && mkdir -p $(dirname ${file}) && touch ${file}\
    && cat $i | openssl enc -d -aes-256-cbc -salt -pass file:$3 > ${file}
  fi
done
