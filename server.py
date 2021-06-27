import socket
import json
from threading import Thread
from client import Client
from database import conn

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 5000))
server.listen(10)

clients = []
lobbies = []
commands = []


def start():
    while True:
        try:
            connection, address = server.accept()
            print(f"Connected {address}!")
            check_clients = [x for x in clients if x.address == address]

            if not check_clients:
                client = Client(connection, address)
                client.id = len(clients) + 1
                clients.append(client)
            else:
                client = check_clients[0]

            client_thread = Thread(target=client_thread_routine, args=[client])
            client_thread.setDaemon(True)
            client_thread.start()
        except:
            print("Couldn't accept client!")


def client_thread_routine(client):
    while True:
        print(f"Client thread {client.address} started")
        connection = client.connection
        try:
            buff = connection.recv(1024)
            data = str(buff, encoding="utf-8")
            json_dict = json.loads(data)
            command_text = json_dict.get("command")
            command_data = json_dict.get("data")
            for command in commands:
                if command.check_command(command_text):
                    response = command.execute(**command_data)
                    response_json = json.loads(response)
                    if response_json.get("account_id") and not client.account_id:
                        client.account_id = response_json.get("account_id")
                    connection.send(bytes(response, "utf-8"))
                    break
        except:
            print(f"Client {client.address} disconnected!")
            break


if __name__ == "__main__":
    thread = Thread(target=start)
    thread.setDaemon(True)
    thread.start()
    input("Press enter to exit\n")
    server.close()
    conn.close()
