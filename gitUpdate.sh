#!/bin/bash

N=$(($@))
for i in `seq 1 ${N}`
do
    if (($i%2 == 0));
    then
        echo "here"
        str="hello"
    else
        echo "here!"
        str="hi"
    fi
        echo $str > test.txt
        git add . > /dev/null
        git commit -m "Commit #${i}." > /dev/null
        git push > /dev/null
done
