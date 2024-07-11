import socket
import select
import time
import sys


class TestBroadcastingClient:
    def __init__(self, id: str, hostname: str, send_port: int) -> None:
        self.id = id
        self.hostname = hostname
        self.send_port = send_port
        self.send_connection: socket.socket

    def connect(self, timeout: int = 10) -> bool:
        try:
            self.send_connection = socket.create_connection(
                (self.hostname, self.send_port), timeout=timeout
            )
        except Exception as error:
            print("[client] Could not connect to to read_server.")
            return False
        return True

    def run(self) -> None:
        while True:
            if not self.connect():
                print("[client] Could not connect to server. Retrying in 1s...")
                time.sleep(1)
                continue
            last_send = time.time()
            while True:
                _, writable, _ = select.select(
                    [], [self.send_connection], [])
                if writable and time.time() - last_send > 2:
                    s = f"hello from client {self.id}"
                    try:
                        self.send_connection.sendall(s.encode())
                    except BrokenPipeError:
                        print("[client] server disconnected")
                        break
                    last_send = time.time()


if __name__ == "__main__":
    client = TestBroadcastingClient(sys.argv[1], "127.0.0.1", 29200)
    client.run()
