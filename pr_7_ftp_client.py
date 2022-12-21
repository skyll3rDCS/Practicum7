import socket, re, os
from pathlib import Path
sock = ''
host = 'localhost'
curr_dir = "\\"
port = 9090
main_dir = Path(os.getcwd(), 'system_home')

def msg_ft_user(login, password, curr_dir, msg, c = 0):
    return f"{login}=login, {password}=password, {curr_dir}=curr_dir, {c}=len, {msg}=message".encode()

def sc_send(login, password, curr_dir, req):
    global sock
    name = re.split("[ \\/]+", req)[-1]
    curr_path_file = Path(main_dir, name)
    sock.send(f'send {name}'.encode())
    with open(curr_path_file, 'r') as file:
        text = file.read()
    print(text.encode())
    sock.send(msg_ft_user(login, password, curr_dir, text.encode(), len(text)))
    return

def sc_res(req):
    global sock, f1, f2, main_dir, curr_dir
    name = re.split("[ \\/]+", req)[-1]
    print(name)
    length = sock.recv(1024).decode()
    text = sock.recv(len(length)).decode()
    curr_path_file = Path(main_dir, name)
    with open(curr_path_file, 'w') as file:
        file.write(text)
    return

def clnt_main():
    global sock
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    curr_dir = login
    print(f"Присоединились к {host} {port}")
    print('help - список команд, exit - выход')
    while True:
        req = input(curr_dir+'$').strip()
        if req == 'exit':
            break
        sock = socket.socket()
        sock.connect((host, port))
        if req.find("send_from") == 0:
            if req == "send_":
                print("Нет файла")
            else: sc_send(login, password, curr_dir, req)
        else:
            sock.send(msg_ft_user(login, password, curr_dir, req))
            if req.find("get_to") == 0 or req == "get_to":
                sc_res(req)
            else:
                response = sock.recv(1024).decode()
                if req.find("cd") == 0:
                    if ".." in req:
                        curr_dir = login
                    else: curr_dir = response[response.find("\\", response.find(login)):]
                else: print(response)

if __name__ == '__main__':
    clnt_main()
