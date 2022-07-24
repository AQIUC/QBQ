import select
import socket
import threading
import time
import datetime


class LY(object):
    def __init__(self, mes, date):
        self.mes = mes
        self.date = date


def start_server():
    host = '0.0.0.0'
    port = 0000
    Server = socket.socket()
    Server.bind((host, port))
    Server.listen(5)
    print("等待接入......")
    return Server


def LY_date():
    while True:
        for i in LY_list:
            if i.date == 0:
                continue
            if i.date == 1:
                LY_list.remove(i)
                print("留言删除：" + i.mes)
            else:
                i.date = i.date-1
                continue
        time.sleep(864)


# while True:
num = 0
server = start_server()
user_ip_list = []
now_time = str(datetime.datetime.now().strftime('%Y-%m-%d'))
ly_head = LY("L(" + now_time + ")以下是留言信息：", 0)
LY_list = [ly_head]
threading.Thread(target=LY_date).start()
# had_get_ip_user_list = []
soc_list = [server]


def all_send(con_mes):
    if len(soc_list) == 1:
        pass
    else:
        for i in range(len(soc_list) - 1):
            soc_list[i + 1].send(con_mes.encode())


def send_LY(conn):
    time.sleep(0.2)
    for i in LY_list:
        conn.send(i.mes.encode())
        time.sleep(0.1)


while True:
    rs, ws, es = select.select(soc_list, [], [])
    for r in rs:
        if r is server:
            c, addr = server.accept()
            soc_list.append(c)
            num += 1
            addr0 = addr[0]
            conn_mes = "F" + "新连接用户" + str(addr)
            all_send(conn_mes)
            time.sleep(1)
            all_send(str(num))
            print("已连接" + str(num) + "个用户")
            print(len(soc_list))
            if addr0 in user_ip_list:
                send_LY(c)
            else:
                user_ip_list.append(addr0)
        else:
            try:
                data = r.recv(1024).decode()
                disconnected = not data
            except socket.error:
                disconnected = True
            if disconnected:
                num -= 1
                soc_list.remove(r)
                dis_conn_mes = "F" + "用户断开" + str(addr)
                all_send(dis_conn_mes)
                time.sleep(1)
                all_send(str(num))
                print("一个用户已断开")
            else:
                if data[0] == "L":
                    new_LY = LY(data, 101)
                    LY_list.append(new_LY)
                    print("留言存入：" + data)
                else:
                    all_send(data)
                    print(data)
