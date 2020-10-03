from multiprocessing import Process 
from multiprocessing import Queue
from concurrent import futures

import sys
import grpc
import time

import message_pb2 as message
import message_pb2_grpc as rpc


def Send(post):
    message.Post(post)


class ChatServer(rpc.MessengerServicer):

    def __init__(self, q):
        self.chats = []
        self.q = q
        


    def ChatStream(self, request_iterator, context):
        lastIndex = 0

        while True:
            while len(self.chats) > lastIndex:
                n = self.q.get()
                lastIndex += 1
                yield message.Post(message=n)
            """

            while len(self.chats) > lastIndex:
                n = self.chats[lastIndex]
                lastIndex += 1
                yield message.Post(message=n)
            """

    def SendPost(self, request, context):
        print("[{}] {}".format(request.name, request.message))
        # Add it to the chat history
        self.chats.append(request.message)
        self.q.put(request.message)
        print('message: ', request.message)
        return message.PostReply(message='message received')  # something needs to be returned required by protobuf language, we just return empty msg

if __name__ == '__main__':
    q_size = int(sys.argv[1])
    q = Queue(q_size)
    port = 11912  # a random port for the server to run on
    # the workers is like the amount of threads that can be opened at the same time, when there are 10 clients connected
    # then no more clients able to connect to the server.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # create a gRPC server
    rpc.add_MessengerServicer_to_server(ChatServer(q), server)  # register the server to gRPC
    # gRPC basically manages all the threading and server responding logic, which is perfect!
    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    # Server starts in background (in another thread) so keep waiting
    # if we don't wait here the main thread will end, which will end all the child threads, and thus the threads
    # from the server won't continue to work and stop the server
    while True:
        time.sleep(64 * 64 * 100)

