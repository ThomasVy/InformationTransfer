import socket
import threading
import select
import os.path
import queue
import extract_piexif

NUMBER_OF_BYTES_SENT = 4096

class AtomicCounter:
    def __init__(self, initial=0):
        """Initialize a new atomic counter to given initial value (default 0)."""
        self.value = initial
        self._lock = threading.Lock()

    def increment(self, num=1):
        """Atomically increment the counter by num (default 1) and return the new value."""
        with self._lock:
            self.value += num
            return self.value
    def decrement(self, num =1):
        with self._lock:
            self.value -= num


class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.name = name
        self.threadID = threadID

    def run(self):
        while True:
            try:
                connection, address = serversocket.accept()
                print str(self.name) + ": " + str(address)

                while(True):
                    try:
                        signal = connection.recv(4)
                        """If client sends 'ready' or 'start', server sends next photo in queue to be analyzed."""
                        if signal == 'recv':
                            print("Sending photo to: " + str(address))
                            if que.empty()!= True:
                                file = que.get()
                                print file
                                input = os.path.abspath(file)
                                sum = 0
                                with open(input, 'rb') as file:
                                    while True:
                                        data = file.read(NUMBER_OF_BYTES_SENT)
                                        if len(data):
                                            connection.send(data)
                                            sum += len(data)
                                        else:
                                            print ("Sent: " + str(sum) + " bytes")
                                            print("Finished sending.\n")
                                            break
                            else:
                                connection.send("")

                                """If client sends 'send', server receives photo from client."""
                        elif signal == 'send':
                            print("Recieving photo from: " + str(address))
                            temp = os.path.join("Recieved", "output" + str(counter1.value) + "v2.jpg")
                            temp = os.path.join("Server", temp)
                            output = os.path.abspath(temp)
                            counter1.increment()
                            sum = 0
                            with open(output, 'wb') as file:
                                while True:
                                    r = select.select([connection], [], [], 1)
                                    if r[0]:
                                        last_data = connection.recv(NUMBER_OF_BYTES_SENT)
                                        file.write(last_data)
                                        sum += len(last_data)
                                    else:
                                        if sum != 0:
                                            print("Recieved: " + str(sum) + " bytes")
                                            print("Finished recieving.\n")
                                        else:
                                            print("Received nothing.")
                                            counter1.decrement()
                                        break
                        elif signal == 'quit':
                            return
                    except:
                            print "I don't understand what happened"
                """If thread cannot start after 5 tries, the program ends."""
            except:
                print("An error occurred. Retrying...")

def updateAll(photo):
    #get geo tag and place other geeses on it
    replacement = os.path.join(output, photo)
    data = extract_piexif.extract_piexif(replacement)
    print data

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 9999))
serversocket.listen(5) # become a server socket, maximum 5 connections
print "Server is running..."

counter1 = AtomicCounter()
que = queue.Queue()
temp = os.path.join("Server", "ToSend")
output = os.path.abspath(temp)
photos = [f for f in os.listdir(output) if os.path.isfile(os.path.join(output, f))]
for file in photos:
    out = os.path.join(temp, file)
    que.put_nowait(out)

thread1 = myThread(1, "Thread-1")
thread2 = myThread(2, "Thread-2")
thread3 = myThread(3, "Thread-3")
thread4 = myThread(4, "Thread-4")
thread5 = myThread(5, "Thread-5")

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()

t= [thread for thread in threading.enumerate() if thread.name != 'MainThread']

temp = os.path.join("Server", "Recieved")
output = os.path.abspath(temp)
old_photos = [f for f in os.listdir(output) if os.path.isfile(os.path.join(output, f))]
while True:
    new_photos = [f for f in os.listdir(output) if os.path.isfile(os.path.join(output, f))]
    diff = [photo for photo in new_photos if photo not in old_photos]
    for photo in diff:
         path = os.path.join(output, photo )
         updateAll(photo)

