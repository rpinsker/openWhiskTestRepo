#!/bin/bash

N=$(($@))
for i in `seq 1 ${N}`
do
    if (($i%2 == 0));
    then
        str="hello"
    else
        str="hi"
    fi
        echo $str > test.txt
        git add . > /dev/null
        git commit -m "Commit #${i}." > /dev/null
        git push > /dev/null 2>&1
done
