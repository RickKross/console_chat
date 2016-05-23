#Using python2.5
#!/ust/bin/env py3
#-*- coding: utf-8 -*-

import asyncio, socket, traceback
import logging


class Client():
    def __init__(self):
        self.logger = logging.getLogger("client_logger")
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("\n %s \n" % ('-'*40))

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        fh = logging.FileHandler("_client.log")
        fh.setLevel(logging.INFO)

        fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt = "%d %B %Y - %H:%M:%S")
        fh.setFormatter(fh_formatter)
        ch_formatter =  logging.Formatter('%(asctime)s - %(message)s', datefmt = "%H:%M:%S")
        ch.setFormatter(ch_formatter)

        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def _accept_connection(self, reader, writer):

        task = asyncio.Task(self._handle_connection(reader, writer))
        def client_done(task):
            self.logger.info("Task done: {}".format(task))

        task.add_done_callback(client_done)

    async def _handle_connection(self, reader, writer):
        self.logger.info("Connecned to {}".format(addr))
        i = 0
        while True:
            i += 1
            data = await reader.read(100)
            if not data:
                break
            message = data.decode()
            self.logger.info("Received {} from {}".format(message, addr))
            
            writer.write(b"hi {}".format(i))
            await writer.drain()
        self.logger.debug("---------Client is not active")

    def start(self):
        sock = socket.socket()
        port = 17117
        while True:
            host = input("Enter IP to connect: ")
            if not host or host == '\n':
                host = 'localhost'
            try:
                sock.connect((host,port))
            except ConnectionRefusedError:
                self.logger.info("Cant reach server. Shutting down")
                return
            except Exception:
                self.logger.info("{}".format(traceback.format_exc()))
                continue
            else:
                break
        self.logger.debug("-------------everything is good now")
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self._accept_connection, sock = sock, loop = loop)
        self.logger.debug("-------------still going good[1]")
        server = loop.run_until_complete(coro)
        self.logger.debug("-------------still going good[2]")

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

client = Client()
client.start()
