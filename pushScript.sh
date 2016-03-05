#!/bin/sh

i="$2"
if [ ${#i} -ge 5 ]
then
  rm -rf $2/*
fi
for i in $(find $1);
do
  file=$2/$(echo $i | openssl enc -aes-256-cbc -salt -pass file:$3 | xxd -p | tr -d '\n') \
  && head $i 1>/dev/null 2>/dev/null \
  && mkdir -p $(dirname ${file}) && touch ${file}\
  && cat $i | openssl enc -aes-256-cbc -salt -pass file:$3 -out ${file} \
  && echo $(basename ${file}) \
  && echo $(basename ${file}) | xxd -r -p | openssl enc -d -aes-256-cbc -pass file:$3
done
