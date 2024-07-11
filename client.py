import socket
import select
import time
import sys


class TestClient:
    def __init__(self, id: str, hostname: str, send_port: int, recv_port: int) -> None:
        self.id = id
        self.hostname = hostname
        self.send_port = send_port
        self.recv_port = recv_port
        self.send_connection: socket.socket
        self.recv_connection: socket.socket
        self.send_connection_ok: bool = False
        self.recv_connection_ok: bool = False

    def connect(self, timeout: int = 10) -> bool:
        try:
            self.send_connection = socket.create_connection(
                (self.hostname, self.send_port), timeout=timeout
            )
            self.send_connection_ok = True
        except Exception as error:
            print("[client] Could not connect to to read_server.")
            return False
        try:
            self.recv_connection = socket.create_connection(
                (self.hostname, self.recv_port), timeout=timeout
            )
            self.recv_connection_ok = True
        except Exception as error:
            print("[client] Could not connect to to write_server.")
            return False
        return True

    def run(self) -> None:
        while True:
            if not self.connect():
                print("[client] Could not connect to server. Retrying in 1s...")
                time.sleep(1)
                continue
            last_send = time.time()
            while self.send_connection_ok or self.recv_connection_ok:
                rlist = []
                wlist = []
                if self.recv_connection_ok:
                    rlist.append(self.recv_connection)
                if self.send_connection_ok:
                    wlist.append(self.send_connection)
                readable, writable, _ = select.select(rlist, wlist, [])
                if readable:
                    data = self.recv_connection.recv(1024)
                    if data:
                        print("[client] Received: ", data)
                    else:
                        print("[client] Sending server disconnected")
                        self.recv_connection_ok = False
                if writable and time.time() - last_send > 2:
                    s = f"hello from client {self.id}"
                    try:
                        self.send_connection.sendall(s.encode())
                    except BrokenPipeError:
                        print("[client] Receiving server disconnected")
                        self.send_connection_ok = False
                    last_send = time.time()


if __name__ == "__main__":
    client = TestClient(sys.argv[1], "127.0.0.1", 29200, 29201)
    client.run()
