#!/bin/bash

for i in 2
do
    wsk activation poll > "pollApp2.${i}.txt" & pid=$!
    time bash gitUpdate.sh $2
    sleep 20
    kill $pid
    echo "starting python script..."
    python parsePoll.py "pollApp2${i}.txt"
done

exit 0;

