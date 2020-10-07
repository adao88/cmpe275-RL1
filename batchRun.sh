#!/bin/bash

echo "starting test...."
for i in {100..500..100}
do
    for j in {0..1000..200}
		do
			echo "*************************Sending $i messages, QueueSize: $j********************"
			time ./run.sh $j 5 $i 1000000
			echo "*********************************************************************************" 
		done
done
