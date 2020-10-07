#!/bin/bash

#running client


python3 server.py $1 $2 &>/dev/null &
sleep 1
pids=$(pgrep python3)
echo "anon mem count:"
pmap $pids | grep -c anon
echo "process info server.py:"
ps aux | grep "server.py $1 $2"
echo "listener Started"
python3 listener.py &
echo "client Started"
python3 client.py $3 $4
pids=$(pgrep python3)
echo "Memory usage: Server"
pmap $pids | grep -c anon 
pmap $pids |  tail -1 
ps aux | grep "python3 server.py $1 $2"
#cat /prog/$pids/maps
#| tail -1
#kill pids
pkill python3
