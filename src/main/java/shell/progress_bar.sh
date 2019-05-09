#!/bin/bash

b=''
str=("|" "/"  "~" "\\")
for ((i=0;i<=100;i++))
do
printf "progress:[%-100s] %3b%% [%c]\r" $b $i ${str[$(( $i % 4 ))]}
sleep 0.1
b=#$b
done
echo 
