#Using python2.5
#!/ust/bin/env py3
#-*- coding: utf-8 -*-

import asyncio
import logging
import json

class Server():
    def __init__(self):
        self.logger = logging.getLogger("server_logger")
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("\n %s \n" % ('-'*40))

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        fh = logging.FileHandler("_server.log")
        fh.setLevel(logging.INFO)

        fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt = "%d %B %Y - %H:%M:%S")
        fh.setFormatter(fh_formatter)
        ch_formatter =  logging.Formatter('%(asctime)s - %(message)s', datefmt = "%H:%M:%S")
        ch.setFormatter(ch_formatter)

        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

        self.clients = {} #addr: name

    def _accept_client(self, reader, writer):
        wr_socket = writer.get_extra_info('socket')
        self.clients[wr_socket] = "NoName"
        self.logger.debug("added to {} socket list".format(wr_socket))

        task = asyncio.Task(self._handle_client(reader, writer))
        def client_done(task):
            self.logger.info("Client task done: {}".format(task))
            try:
                self.clients.pop(wr_socket)
            except KeyError:
                pass #TODO may be some problems here

        task.add_done_callback(client_done)


    def _sendall(self, message, excpt=None):
        for socket in self.clients.keys():
            if excpt and socket == excpt:
                continue
            socket.send(message.encode())
            name = self.clients[socket]
            self.logger.debug("Sent {} to {}".format(message, (socket.getpeername(), name)))


    async def _handle_client(self, reader, writer):
        self.logger.debug("--------new client is active")
        addr = writer.get_extra_info('peername')
        sock = writer.get_extra_info('socket')
        self.logger.info("Accepted connection from {}".format(addr))
        while True:
            data = await reader.read(100)
            if not data:
                break

            message = data.decode()
            if message == "~//break":
                self._sendall("User {} disconnected".format(name), excpt = sock)
                self.logger.info("User {} disconnected. Closing the client socket".format(addr))
                writer.close()
                break
            elif "~//name" in message:
                name = message[8:]
                self.clients[sock] = name
                self.logger.debug("------ onl_list: {}".format(self.clients.values()))
                self._sendall("User {} connected!".format(name), excpt = sock)
                continue
            message = message[1:]
            self.logger.info("Received {} from {}".format(message, (addr, name)))
            

            message = name + ": " + message
            self._sendall(message, excpt = sock)

            try:
                client_names = [value for value in self.clients.values()]
                answer = json.dumps(client_names)
                writer.write("~//onl {}".format(answer).encode())
                await writer.drain()
            except Exception as e:
                self.logger.debug(e)
        self.logger.debug("---------Client is not active")

    def start(self):
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self._accept_client, '127.0.0.1', 17117, loop = loop)
        server = loop.run_until_complete(coro)

        # Serve requests until Ctrl+C is pressed
        self.logger.info('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
        self.logger.info("Serving stopped")

#-------------------------------------------------------------------------------------------------------------------------------------

server = Server()
server.start()
