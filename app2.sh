#!/bin/bash

for i in 1 10 100
do
    echo $N
    echo -e -----------------------
    echo -e "          ${i}           "
    echo -e -----------------------
    wsk activation poll > "pollApp2.${i}.txt" & pid=$!
    time bash gitUpdate.sh $i
    sleep 10
    kill $pid
    echo "starting python script..."
    python ../parsePoll.py "pollApp2${i}.txt"
done

exit 0;

