# Example TCP server/client in python

This is an very basic example of a TCP client/server setup using Python sockets
and select OS calls.

This enables bidirectional communication at different frequencies.

Such a setup can be used to communicate between 2 devices for example.

## Installation

1. Clone this repo.\
This example does not require external dependencies as `socket` and `select` are bundled with Python.

2. In a terminal, run the server, the bidirectional client or the broadcasting client:

    ```bash
    python3 server.py
    ```

3. In a second terminal, launch a component you haven't launch in the first terminal.

    ```bash
    python3 client.py "client_name"
    # OR
    python3 broadcasting_client.py "client_name"
    ```

4. You can launch multiple clients/broadcasting_clients if you wish in more terminals.

## Feedback

Please feel free to give your feedback by openning an issue !
