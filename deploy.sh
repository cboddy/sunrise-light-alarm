#!/bin/bash

remote=$1

echo "tar-ing project"
rm -f bundle.tar.gz
tar -zcvf bundle.tar.gz public raspledstrip *.py

echo "copying project to remote " $1
scp bundle.tar.gz $1:~/

echo "unpacking project on remote " $1

ssh $1 '
mkdir -p sunrise 
mv bundle.tar.gz sunrise
cd sunrise
tar -zxvf bundle.tar.gz
'
