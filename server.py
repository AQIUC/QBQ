import select
import socket


def start_server():
    host = '0.0.0.0'
    port = 0000
    Server = socket.socket()
    Server.bind((host, port))
    Server.listen(5)
    print("等待接入......")
    return Server


# while True:
num = 0
server = start_server()
soc_list = [server]


def all_send(con_mes):
    if len(soc_list) == 1:
        pass
    else:
        for i in range(len(soc_list) - 1):
            soc_list[i + 1].send(con_mes.encode())


while True:
    rs, ws, es = select.select(soc_list, [], [])
    for r in rs:
        if r is server:
            c, addr = server.accept()
            soc_list.append(c)
            num += 1
            conn_mes = "F" + "新连接用户" + str(addr)
            all_send(conn_mes)
            all_send(str(num))
            print("已连接" + str(num) + "个用户")
            print(len(soc_list))
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
                all_send(str(num))
                print("一个用户已断开")
            else:
                all_send(data)
                print(data)
