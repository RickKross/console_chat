#Using python3.5
#!/ust/bin/env py3
#-*- coding: utf-8 -*-

import asyncio
import logging

clients = []

class ServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        self.logger = logging.getLogger("server_logger")
        self.peername = transport.get_extra_info("peername")
        self.logger.info("connection_made: {}".format(self.peername))
        clients.append(self)

    def data_recieved(self, data):
        self.logger.info("data_received: {}".format(data.decode()))
        for client in clients:
            if client is not self:
                client.transport.write("{}: {}".format(self.peername, data.decode()).encode())

    def connection_lost(self, ex):
        self.logger.info("connection_lost: {}".format(self.peername))
        clients.remove(self)

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

    def start(self):
        loop = asyncio.get_event_loop()
        coro = loop.create_server(ServerProtocol, host = "127.0.0.1", port = 17117)
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
