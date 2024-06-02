import socket
import threading
from datetime import datetime
class Manager:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.lock = threading.Lock()

    def start(self):
        self.server.bind((self.ip, self.port))
        self.server.listen(5)
        print(f"Server started on {self.ip}:{self.port}")
        while True:
            client_socket, client_address = self.server.accept()
            print(f"用户{client_address}请求加入群聊:")
            word=input("是否同意(yes/no)：")
            if word=='yes':
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
                print(f"用户{client_address}已进入群聊")
            elif word=='no':
                print(f"用户{client_address}已被拒绝接入")
                client_socket.send("抱歉，您已被拒绝进入".encode())

    def handle_client(self, client_socket):
        username = client_socket.recv(1024).decode()
        self.lock.acquire()
        self.clients[username] = client_socket
        self.lock.release()
        self.broadcast(f"{username} joined the chatroom.")
        chat_log=[]
        while True:
            message = client_socket.recv(1024).decode()
            if message.startswith("@"):
                recipient, message = message.split(" ", 1)
                recpt=recipient.strip('@')
                self.send_to(recpt, f"{username}: {message}")
            elif message=="quit":
                print(f"{username}已退出群聊")
                self.lock.acquire()
                del self.clients[username]
                self.lock.release()
                self.broadcast(f"{username} left the room")
                with open(f"{username}_chat_log.txt",'w') as f:
                    f.write("\n".join(chat_log))
                with open("all_chat_logs.txt",'a') as f:
                    f.write("\n".join(chat_log))
                break
            else:
                now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.broadcast(f"{username}: {message}")
                chat_log.append(f"{now} {username}:{message}")

    def broadcast(self, message):
        self.lock.acquire()
        for client_socket in self.clients.values():
            client_socket.send(message.encode())
        self.lock.release()

    def send_to(self, recipient, message):
        self.lock.acquire()
        if recipient in self.clients:
            self.clients[recipient].send(message.encode())
        self.lock.release()

if __name__ == "__main__":
    manager = Manager("127.0.0.1", 8888)
    manager.start()


class Chatter:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.client_socket.connect((self.host, self.port))
        self.client_socket.send(self.username.encode())
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        send_thread = threading.Thread(target=self.send)
        send_thread.start()

    def receive(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                print(message)
            except:
                self.client_socket.close()
                break

    def send(self):
        while True:
            message = input()
            if message.lower() == "byebye":
                self.client_socket.send(message.encode())
                self.client_socket.close()
                break
            elif message.startswith("@"):
                recipient, message = message.split(" ", 1)
                self.client_socket.send(f"@{recipient} {message}".encode())
            else:
                self.client_socket.send(message.encode())

if __name__ == "__main__":
    username = input("Enter your username: ")
    chatter = Chatter("127.0.0.1", 8888, username)
    chatter.start()
