import socket
import select
import datetime
import tkinter as tk
import threading
import ctypes
import inspect
import httplib2
from urllib.parse import urlencode


def get_ip():
    params = urlencode({'ip': '', 'datatype': 'jsonp', 'callback': 'find'})
    url = 'https://api.ip138.com/ip/?' + params
    headers = {"token": "f7f78c0c4e0a074dd69e87a5a9a72818"}  # token为示例
    http = httplib2.Http()
    response, content = http.request(url, 'GET', headers=headers)
    imformation = str(content.decode("utf-8")).split("\"")
    Ip = imformation[7]
    City = imformation[11] + imformation[13] + imformation[15]
    return Ip, City


def wait():
    win2_is_exit = False

    def login_in():
        global ip, city

        now_time = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        s = socket.socket()
        host = '0.0.0.0'
        port = 0000
        s.connect((host, port))

        if win2_is_exit:
            win2.destroy()
        name = str(en1.get())
        win1.destroy()

        file_chat = open(now_time + "-" + name + "-聊天记录.txt", 'a', encoding="utf-8")
        file_LY = open(now_time + "-" + name + "-留言记录.txt", 'a', encoding="utf-8")

        def send_C():
            send_data2 = "C" + city + "-" + ip + "-" + name + "：" + str(en_chat.get())
            s.send(send_data2.encode())
            en_chat.delete(0, "end")

        def send_L():
            send_data2 = "L" + city + "-" + ip + "-" + name + "：" + str(en_leave.get())
            s.send(send_data2.encode())
            en_leave.delete(0, "end")

        def __async_raise(thread_Id, exctype):
            thread_Id = ctypes.c_long(thread_Id)
            if not inspect.isclass(exctype):
                exctype = type(exctype)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_Id, ctypes.py_object(exctype))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_Id, None)
                raise SystemError("PyThreadState_SEtAsyncExc failed")

        def terminator(thread):
            __async_raise(thread.ident, SystemExit)

        def Th_recv():
            Fn = 0
            Cn = 0
            soc_list = [s]
            while True:
                rs, ws, es = select.select(soc_list, [], [])
                for r in rs:
                    if r is s:
                        if Fn == 8:
                            tx3.delete(0.0, "end")
                            Fn = 0
                        if Cn == 10:
                            tx1.delete(0.0, "end")
                            Cn = 0
                        data = s.recv(1024).decode()
                        if data[0] == "F":
                            tx3.insert("end", data + "\n")
                            Fn = Fn + 1
                        elif data[0] == "C":
                            tx1.insert("end", data + "\n")
                            Cn = Cn + 1
                            file_chat.write(data + "\n")
                        elif data[0] == "L":
                            tx2.insert("end", data + "\n")
                            file_LY.write(data + "\n")
                        else:
                            tx3.insert("end", "当前在线人数：" + data + "\n")
                            Fn = Fn + 1

        win3 = tk.Tk()
        win3.title("欢迎" + name + "来到秋本秋的秘密基地")
        win3.geometry("500x600+500+100")
        tk.Label(win3, text="聊天记录：", font=("楷体", 12)).place(x=5, y=5)
        tk.Label(win3, text="留言：", font=("楷体", 12)).place(x=255, y=5)
        tx1 = tk.Text(win3, width=30, height=19, font=("楷体", 12))
        tx1.place(x=5, y=35)
        tx2 = tk.Text(win3, width=30, height=19, font=("楷体", 12))
        tx2.place(x=255, y=35)
        tx2.insert("end", "暂未开发\n目前功能同聊天功能\n")
        en_chat = tk.Entry(win3, width=30, font=("楷体", 12))
        en_leave = tk.Entry(win3, width=30, font=("楷体", 12))
        en_chat.place(x=5, y=350)
        en_leave.place(x=255, y=350)
        tk.Button(win3, text="发送", font=('楷体', 16), command=send_C).place(x=5, y=380)
        tk.Label(win3, text="查找聊天记录\n见同级文件夹", font=('楷体', 12)).place(x=70, y=380)
        tk.Button(win3, text="留言", font=('楷体', 16), command=send_L).place(x=255, y=380)
        tk.Label(win3, text="查找留言记录\n见同级文件夹", font=('楷体', 12)).place(x=320, y=380)
        tk.Label(win3, text="服务器消息：", font=("楷体", 12)).place(x=8, y=430)
        tx3 = tk.Text(win3, width=60, height=8, font=("楷体", 12))
        tx3.place(x=8, y=460)

        t1 = threading.Thread(target=Th_recv)
        t1.start()

        win3.mainloop()
        terminator(t1)
        s.close()

    if str(en1.get()) == "":
        win2_is_exit = True
        win2 = tk.Tk()
        win2.title("确定么？")
        win2.geometry("240x150+640+320")
        tk.Label(win2, text="未输入称呼，\n别人可能认不得你，\n确定登录么？", font=('楷体', 16)).place(x=20, y=5)
        tk.Button(win2, text="确定", font=('楷体', 16), command=login_in).place(x=85, y=90)
    else:
        login_in()


win1 = tk.Tk()
win1.title("来自秋本秋的秘密频道")
win1.geometry("420x300+550+230")
ip, city = get_ip()
tk.Label(win1, text="当前公网IP:    " + ip, font=('楷体', 16)).place(x=50, y=50)
tk.Label(win1, text="当前城市:      " + city, font=('楷体', 16)).place(x=50, y=100)
tk.Label(win1, text="给个称呼吧：", font=('楷体', 12)).place(x=50, y=150)
en1 = tk.Entry(win1, width=30)
en1.place(x=160, y=150)
tk.Button(win1, text="Link Start!", font=('楷体', 12), height=2, width=23, command=wait).place(x=110, y=200)
win1.mainloop()
