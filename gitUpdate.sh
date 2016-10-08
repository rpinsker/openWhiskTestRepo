#!/bin/bash


for i in {1..4}
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
        git add .
        git commit -m "Commit #${i}."
        git push
done
