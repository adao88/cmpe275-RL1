# cmpe275-RL1

Set up:
pip3 install --upgrade google-api-python-client
pip3 install grpcio

Client.py:
takes in (1)number argument for how many random strings/message to be sent to server

Server.py:
takes in (1)number argument for queue size

todo - Implement multiprocessing

Listener.py:
No arguments, just listens for the message stream from client -> server -> listener

Ideas:

- Thread & Queue Increase/Decrease and How it affects performance

- Blocking / Non-Blocking gRPC Client
