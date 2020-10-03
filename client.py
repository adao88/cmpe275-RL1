import threading
import grpc 
import sys

import random
import string



import message_pb2 as message
import message_pb2_grpc as rpc

address = 'localhost'
port = 11912

class Client:

    def __init__(self, user):
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.MessengerStub(channel)
        
        # create new listening thread for when new message streams come in
        #threading.Thread(target=self.__listen_for_messages, daemon=True).start()

    
    def __listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        for note in self.conn.ChatStream(message.Empty()):  # this line will wait for new messages from the server!
            print('message: ', note.message)  # debugging statement
            
    def send_message(self, word):
        #post = input('Send: \n')
        n = message.Post(name='An', message=word)
        response = self.conn.SendPost(n)
        print(response.message)

def run(count):
    
    c = Client('Test')
    
    for _ in range(count):
        c.send_message(get_random_string())
    c.send_message('done')   

def get_random_string(length = 15):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

if __name__ == '__main__':
    count = int(sys.argv[1])
    run(count)