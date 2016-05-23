import socket, asyncio
import traceback

class Client():

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host = 'localhost', port = 17117):
        try:
            reader, writer = yield from asyncio.open_connection(host, port)
        except ConnectionRefusedError:
            print("Can't connect to server. Probably somethind went wrong..")
            return
        except Exception:
            print(traceback.format_exc())
            return
        print("Connected!")

        task = asyncio.Task(self._handle_connection(reader, writer))
        def connection_done(task):
            print("Connection to {} closed".format((host, port)))
        task.add_done_callback(connection_done)

    async def _handle_connection(self, reader, writer):
        print("connection_handler")
        try:
            while True:
               message = input(">> ")
               if not message or message == "\n":
                   continue
               data = message.encode()
               writer.write(data)
               print("Sent")
               data = await reader.read()
               data = data.decode()
               print("Received: {}".format(data))
               await writer.drain()
        except KeyboardInterrupt:
            writer.write("~//break".encode())
            await writer.drain()
            writer.close()
        except Exception:
            print(traceback.format_exc())

    def start(self):
        host = input("Enter IP to connect: ")
        if not host or host == "\n":
            host = "localhost"
        port = 17117

        loop = asyncio.get_event_loop()
        client = loop.run_until_complete(self.connect(host, port))
        loop.close()

        print("Connection closed")

#------------------------------------------------------------------------------------------------------------------------
c = Client()
c.start()



