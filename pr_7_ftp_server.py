import socket, shutil, os, csv
from pathlib import Path
import logging
port = 9090
main_dir = Path(os.getcwd(), 'system_home')
curr_dir = Path(os.getcwd(), 'system_home')
user_dir =''
path = ''
login = ''
conn =''
size = 0


file_user = Path(os.getcwd(), 'file_user.csv')
def log_inf():
    logging.basicConfig(
        level=logging.DEBUG,
        format="Date: %(asctime)s | %(message)s",
        handlers=[
            logging.FileHandler("logs.log"),
            logging.StreamHandler(),
        ],
    )

def write_user(login, password):
    global file_user
    with open(file_user, "a+", newline="") as f:
        f.seek(0, 0)
        reader = csv.reader(f, delimiter=";")
        for line in reader:
            if line[0] == login:
                if line[1] == password:
                    break
                else:
                    return None
        else:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([login, password])
def write_log(msg):
    logging.info(msg)
def users(msg):
    global main_dir, curr_dir, user_dir, login, size
    login = msg[:msg.find("=login, ")]
    password = msg[msg.find(" "):msg.find("=password, ")].strip()
    curr_dir = msg[msg.find(" ", msg.find("=password, "), msg.find("=curr_dir, ")):msg.find("=curr_dir, ")].strip()
    size = msg[msg.find(" ", msg.find("=curr_dir, "), msg.find("=len, ")):msg.find("=len, ")].strip()
    msg = msg[msg.find(" ", msg.find("=len, "), msg.find("=message")):msg.find("=message")].strip()
    if login == "admin" and password == "qwerty":
        user_dir = main_dir
    else:
        user_dir = Path(main_dir, login)
        write_user(login, password)
        try:
            os.makedirs(user_dir)
        except FileExistsError:
            pass
    return user_dir, curr_dir, msg, login, size

def check_command(req):
    global user_dir, path
    req = users(req)
    if req:
        user_dir, curr_dir, msg, login, size = req
        comm, *args = msg.split()
        if curr_dir != login:
            t = curr_dir.replace("\\", "", 1)
            path = Path(user_dir, t)
        comms = {
            'CDL': CDL,
            'pwd': pwd,
            'mkDir': mkDir,
            'touch': touch,
            'rmDir': rmDir,
            'rename': rename,
            'rm': rm,
            'mv': move,
            'cd': cd,
            'send_from':send_from,
            'DataIn': DataIn,
            'get_to': get_to,
            'help': help
        }

        try:
            return comms[comm](*args)
        except Exception as e:
            return 'Нет такой команды'
    else:
        return 'bad password'
def check():
    global path, user_dir, curr_dir
    if path != "":
        if login == curr_dir:
            return user_dir
        elif path != user_dir:
            return path
        else:
            return user_dir
    return user_dir
def pwd():
    global user_dir, curr_dir, login
    root = check()
    if curr_dir != 'admin':
        s =''
        for i in root.parts[3:]:
            s += "\\"+i
        return s
    else:
        return str(root)
def CDL(name=None):
    global user_dir
    root = check()
    if name:
        name1 = Path(root, name)
        return '; '.join(os.listdir(name1))
    return '; '.join(os.listdir(root))

def mkDir(name):
    global user_dir
    root = check()
    name = Path(root, name)
    try:
        os.mkdir(name)
        return "успешно"
    except Exception:
        return "Ошибка"

def rename(name1, name2):
    global user_dir
    root = check()
    name1 = Path(root, name1)
    name2 = Path(root, name2)
    try:
        os.rename(name1, name2)
        return "успешно"
    except Exception:
        return "Ошибка"

def cd(name):
    global user_dir, curr_dir, path
    root = check()
    try:
        if name == "..":
            name1 = Path(user_dir)
        else: name1 = Path(root, name)
        os.chdir(name1)
    except:
        return curr_dir
    return os.getcwd()

def touch(name, text=''):
    global user_dir
    root = check()
    name = Path(root,name)
    max_size = pow(2, 20) * 10 - getting(root)
    if max_size < int(size):
        return "Нет места"
    else:
        try:
            name.touch()
            name.write_text(text)
            return "успешно"
        except Exception:
            return "Ошибка"

def rmDir(name):
    global user_dir
    root = check()
    name = Path(root,name)
    if name.is_dir():
        shutil.rmtree(name)
        return "успешно"
    else:
        return 'Ошибка'

def rm(name):
    try:
        root = check()
        global user_dir
        name = Path(root,name)
        if name.is_file():
            os.remove(name)
            return "успешно"
        else:
            return 'Вы ввели имя не файла'
    except Exception:
        return "Ошибка"

def move(src, dst):
    global user_dir
    try:
        root = check()
        src = Path(root,src)
        dst = Path(root,dst)
        if src.exists():
            shutil.move(src, dst)
            return "успешно"
        else:
            return "Не существует"
    except Exception:
        return "Ошибка"

def DataIn(name):
    try:
        global user_dir
        root = check()
        name = Path(root,name)
        if name.is_file():
            return name.read_text()
        else:
            return "Не файл"
    except Exception:
        return "Ошибка"

def help():
    return 'pwd - вернёт название рабочей директории\n' \
           'CLD <dirname>- вернёт список файлов в рабочей директории\n' \
           'mkDir <dirname> -  создаёт директорию с указанным именем\n' \
           'rmDir <dirname> -  удаляет директорию с указанным именем\n' \
           'touch <filename> -  создаёт файл с указанным именем\n' \
           'rm <filename> -  удаляет файл с указанным именем\n' \
           'move <filename> <dirname> -  перемещает файл/директорию в другую директорию\n' \
           'rename <filename> <filename2> -  переименновывает файл с указанным именем \n' \
           'DataIn <filename> -  вернёт содержимое файла\n' \
           'help - выводит справку по командам\n' \
           'exit - выход из системы'

def getting(name):
    size = 0
    for dirpath, dirnames, file in os.walk(name):
        for f in file:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                size += os.path.getsize(fp)
    return size

def send_from(name):
    global conn, size
    root = check()
    name = Path(root, name)
    max_size = pow(2, 20) * 10 - getting(root)
    if max_size < int(size):
        return "Нет места"
    else:
        text = conn.recv(int(size)).decode()
        try:
            with open(name, 'w') as file:
                file.write(text)
            write_log("все получено")
            return f'{name}'
        except Exception:
            return 'Ошибка'

def get_to(name):
    global conn
    root = check()
    name = Path(root, name)
    with open(name, 'r') as file:
        text = file.read()
    conn.send(str(len(text)).encode())
    conn.send(text.encode())
    write_log("Отправлено")
    return f'{name}'

def serv_main():
    global conn
    log_inf()
    if not main_dir.is_dir():
        mkDir(main_dir)
    os.chdir(main_dir)
    with socket.socket() as sock:
        sock.bind(('', port))
        sock.listen()
        print("Слушаем порт: ", port)
        write_log(f'Слушаем порт: {port}')
        while True:
            conn, addr = sock.accept()
            with conn:
                req = conn.recv(1024).decode()
                write_log("request:"+req)
                resp = check_command(req)
                write_log("response:"+str(resp))
                if resp is None:
                    resp = ''
                try:
                    conn.send(resp.encode())
                except Exception:
                    conn.send(resp)
        conn.close()
if __name__ == '__main__':
    serv_main()
