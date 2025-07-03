import socket
import threading

HOST = '127.0.0.1'
PORT = 3456
LISTENER_LIMIT = 5
active_clients = []  # List of tuples (username, client_socket)

def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                if message == "DISCONNECT":
                    remove_client(client, username)
                    break
                final_msg = username + '~' + message
                send_messages_to_all(final_msg, client)
            else:
                remove_client(client, username)
                break
        except:
            remove_client(client, username)
            break

def send_message_to_client(client, message):
    try:
        client.sendall(message.encode())
    except:
        remove_client(client, None)

def send_messages_to_all(message, sender_socket):
    for user in active_clients[:]:  # Use copy to avoid modification during iteration
        if user[1] != sender_socket:  # Don't send back to the sender
            send_message_to_client(user[1], message)

def remove_client(client, username):
    if (username, client) in active_clients:
        active_clients.remove((username, client))
        if username:
            prompt_message = "SERVER~" + f"{username} left the chat"
            send_messages_to_all(prompt_message, client)

def client_handler(client):
    # Receive username immediately
    try:
        username = client.recv(2048).decode('utf-8')
        if username:
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message, client)
            client.send(f"SERVER~Connected to server".encode('utf-8'))
            threading.Thread(target=listen_for_messages, args=(client, username,)).start()
        else:
            client.close()
    except:
        client.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")
        return

    server.listen(LISTENER_LIMIT)
    while True:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        threading.Thread(target=client_handler, args=(client,)).start()

if __name__ == '__main__':
    main()