import socket
import traceback

class Client():

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, conn_addr = ("localhost", 17117)):
        try:
            print("Connecting to ", self.conn_addr, "...")
            self.sock.connect(self.conn_addr)
        except Exception:
            print(traceback.format_exc())
        else:
            print("Connected!")

    def start(self):
        self.host = input("Enter IP to connect: ")
        if not self.host or self.host == "\n":
            self.host = "localhost"
        self.port = 17117
        self.conn_addr = (self.host, self.port)
        self.connect(self.conn_addr)
        while True:
            try:
                self.sock.send(input("Type some data to send: ").encode())
                data = self.sock.recv(100).decode()
                print("Recieved: ", data)
            except KeyboardInterrupt:
                self.sock.send("~//break".encode("utf-8"))
                break



c = Client()
c.start()



