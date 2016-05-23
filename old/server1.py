#Using python3.5
#!/ust/bin/env py3
#-*- coding: utf-8 -*-

import asyncio
import logging

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

    def _accept_client(self, reader, writer):

        task = asyncio.Task(self._handle_client(reader, writer))
        def client_done(task):
            self.logger.info("Client task done: {}".format(task))

        task.add_done_callback(client_done)


    async def _handle_client(self, reader, writer):
        self.logger.debug("--------new client is active")
        addr = writer.get_extra_info('peername')
        self.logger.info("Accepted connection from {}".format(addr))
        while True:
            data = await reader.read(100)
            if not data:
                break
            message = data.decode()
            if message == "~//break":
                self.logger.info("User {} disconnected. Closing the client socket".format(addr))
                writer.close()
                break
            self.logger.info("Received {} from {}".format(message, addr))
            #1: 
#            for wrtr in self.client_writers:
#                wrtr.write(data)
#                self.logger.info("Sent -{}- to {}".format(message)
#                await wrtr.drain()
            #2:
            writer.write(data)
            await writer.drain()
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
