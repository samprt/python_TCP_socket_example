import select
import socket
import time


class TestServer:
    def __init__(self, hostname: str, read_port: int, write_port: int) -> None:
        self.hostname = hostname
        self.read_port = read_port
        self.write_port = write_port
        self.read_server = socket.create_server(
            (self.hostname, self.read_port))
        self.write_server = socket.create_server(
            (self.hostname, self.write_port))
        self.read_server.setblocking(False)
        self.write_server.setblocking(False)
        self.read_server.listen()
        self.write_server.listen()

    def run(self) -> None:
        sending_clients: list[socket.socket] = []
        receiving_clients: list[socket.socket] = []

        rlist: list[socket.socket] = [self.read_server, self.write_server]
        wlist: list[socket.socket] = []

        messages_received: list[bytes] = []

        last_write_time = time.time()
        while True:
            r, w, err = select.select(rlist, wlist, [], 0.1)
            for sock in r:
                if sock == self.read_server:
                    sending_client, addr = sock.accept()
                    print(f"[read_server] Connection from {addr}")
                    sending_client.setblocking(False)
                    sending_clients.append(sending_client)
                    rlist.append(sending_client)
                elif sock == self.write_server:
                    receiving_client, addr = sock.accept()
                    print(f"[write_server] Connection from {addr}")
                    receiving_client.setblocking(False)
                    receiving_clients.append(receiving_client)
                    wlist.append(receiving_client)
                else:
                    data = sock.recv(1024)
                    if not data:
                        print(f"[server] One read client disconnected")
                        sock.shutdown(socket.SHUT_RDWR)
                        sock.close()
                        sending_clients.remove(sock)
                        rlist.remove(sock)
                    else:
                        messages_received.append(data)

            for sock in w:
                if sock in receiving_clients:
                    if time.time() - last_write_time > 1:
                        try:
                            sock.send("hello from server".encode())
                        except BrokenPipeError:
                            print("[server] One write client disconnected")
                            receiving_clients.remove(sock)
                            wlist.remove(sock)
                        last_write_time = time.time()
            if len(messages_received) > 0:
                for msg in messages_received:
                    print(f"[server] Received: {msg.decode()}")
            messages_received = []


if __name__ == "__main__":
    server = TestServer("127.0.0.1", 29200, 29201)
    server.run()
