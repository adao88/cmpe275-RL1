import threading
import grpc
import sys

import message_pb2 as message
import message_pb2_grpc as rpc

address = 'localhost'
port = 11912


class Listener:

    def __init__(self):
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.MessengerStub(channel)

        # create new listening thread for when new message streams come in
        # threading.Thread(target=self.__listen_for_messages, daemon=True).start()

    def __listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        count = 0
        for note in self.conn.ChatStream(message.Empty()):  # this line will wait for new messages from the server!
            # print('<Listener> - message: ', note.message)  # debugging statement
            count=count+1
            # self.chat_list.insert(END, "[{}] {}\n".format(note.name, note.message))  # add the message to the UI

            if note.message =='<>':
                # print(f'Last Message: {note.message}')
                break
        print(f'{count} Message Received')
        sys.exit()


    def start(self):
        print('Listener Listening...')
        t1 = threading.Thread(target=self.__listen_for_messages, daemon=True)
        t1.start()
        t1.join()


def run():
    # clientID = input('id ?')
    c = Listener()
    c.start()


if __name__ == '__main__':
    """
    username = 'Testing'
    print('working')
    c = Client(username)
    c.send_message()  # this starts a client and thus a thread which keeps connection to server open
    """
    run()
