#!/bin/bash

for i in 200
do
    echo $N
    echo -e -----------------------
    echo -e "          ${i}           "
    echo -e -----------------------
    wsk activation poll > "pollApp2.${i}.txt" & pid=$!
    time bash gitUpdate.sh $i
    sleep 800
    kill $pid
done

exit 0;

