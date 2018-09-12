"""TO DO:
- Create Module
- Make it so the program knows how many photos are left to distribute
- Photo queueing system
- Have the server eliminate re-occuring/redundant photos
- Create new folders to organize
- Set exceptions for reading photos"""

import socket
import select
import os


#for sending a request of photos and recieving them.
import queue


def Receive():
    global counter
    temp = os.path.join("Recieved", "output"+ str(counter)+ ".jpg")
    counter+=1
    temp = os.path.join("Client", temp)
    file_name = os.path.abspath(temp)
    print("Recieving next photo from server...")
    with open (file_name, 'wb') as file:
        sum = 0
        while True:
            r = select.select([clientsocket], [], [], 1)
            if r[0]:
                wrt = clientsocket.recv(NUMBER_OF_BYTES_SENT)
                file.write(wrt)
                sum += len(wrt)
            else:
                if sum != 0:
                    print ("Finish recieving. Stored picture is in: " + file_name )
                    print ("Recieved: " + str(sum) + " bytes\n")
                    que.put(file_name)
                else:
                    print "No photo was sent"
                    counter-=1
                break


#for sending photos back
def Send ():
    global counter
    if que.empty()!=True:
        file_name = que.get()
        print file_name
        print("Sending photo: " + file_name + " to server...")
        with open (file_name, 'rb') as file:
            sum = 0
            while True:
                name = file.read(NUMBER_OF_BYTES_SENT)
                if len(name) != 0:
                    clientsocket.send(name)
                    sum += len(name)
                else:
                    print ("Sent: " + str(sum) + " bytes\n")
                    break
    else:
        print "Don't have anything to send"
        clientsocket.send("")

def Start():
    a = True
    while a:
        try:
            hi = int(raw_input("Type one of the options\n1 = receive\n2 = send\n3 = quit\n"))
            if hi == 1:
                clientsocket.send("recv")
                Receive()

            elif hi == 2:
                    clientsocket.send('send')
                    Send()

            elif hi == 3:
                print("Exiting program...")
                clientsocket.send("quit")
                clientsocket.close()
                exit(0)
            else:
                print("Pick a valid number, idiot!!!!!!")
        except Exception:
            print "Put in a valid number!"


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost',9999))

que = queue.Queue()
NUMBER_OF_BYTES_SENT = 4096
counter = 0
Start()