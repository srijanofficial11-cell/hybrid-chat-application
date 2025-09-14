import socket
import threading

# Function to handle receiving messages
def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            break

# Server code
def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12345))
    server.listen()
    print("Server started... Waiting for clients")

    clients = []

    def broadcast(message, conn):
        for c in clients:
            if c != conn:
                try:
                    c.send(message)
                except:
                    c.close()
                    clients.remove(c)

    def handle_client(conn, addr):
        print(f"Connected: {addr}")
        while True:
            try:
                msg = conn.recv(1024)
                if not msg:
                    break
                print(f"{addr}: {msg.decode()}")
                broadcast(msg, conn)
            except:
                break
        conn.close()
        clients.remove(conn)

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# Client code
def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 12345))
    print("Connected to server. Type messages (type 'exit' to quit)")

    # Thread for receiving messages
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    while True:
        msg = input("")
        client.send(msg.encode())
        if msg.lower() == "exit":
            client.close()
            break

# Entry point
if __name__ == "__main__":
    print("Choose mode:\n1. Server\n2. Client")
    choice = input("Enter choice (1/2): ")

    if choice == "1":
        run_server()
    else:
        run_client()
