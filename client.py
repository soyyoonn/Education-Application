# gui 채팅 클라이언트

from socket import *
from threading import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets
form_class = uic.loadUiType('./fa.ui')[0]

class Main(QMainWindow, form_class):
    client_socket = None

    def __init__(self, ip, port):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.stackedWidget.setCurrentIndex(0)
        self.initialize_socket(ip, port)
        self.listen_thread()
        self.check_btn.clicked.connect(self.check)
        self.main_btn.clicked.connect(self.main_page)
        self.chat_room_2.itemDoubleClicked.connect(self.move_chat_page)
        self.pushButton.clicked.connect(self.send_chat)
        self.chat_register.clicked.connect(self.make_room)
        self.main_btn_2.clicked.connect(self.enter)

    def move_chat_page(self):
        chat = self.chat_room_2.currentItem().text()
        self.client_socket.send((chat + "방번호").encode())
        print(chat)
        self.receivemessage.clear()
        print(34)
        self.stackedWidget.setCurrentIndex(1)

    def enter(self):
        self.chat_room_2.clear()
        self.stackedWidget.setCurrentIndex(0)

    def main_page(self):
        self.stackedWidget.setCurrentIndex(2)

    def check(self):
        self.user_Name = self.user_name.text()
        name = (self.user_Name + '입장').encode()
        QMessageBox.information(self,'알림',f"{self.user_Name}님 입장하셨습니다.")
        self.client_socket.send(name)
        self.stackedWidget.setCurrentIndex(2)
        self.user_name.clear()

    def make_room(self):
        chat_room_name = self.chat_name.text()
        room = (chat_room_name + '채팅방만듬').encode()
        QMessageBox.information(self,'알림',f"채팅방 {room.decode()[:-5]}이(가) 생성되었습니다.")
        self.client_socket.send(room)
        self.chat_name.clear()
        return

    def send_chat(self):
        senders_name = self.user_Name
        chat = self.chat_room_2.currentItem().text()
        data = self.sendmessage.text()
        datalist = f"['{senders_name}','{data}','{chat}']" # 송신자 , 메세지 , 채팅방
        message = datalist +"채팅중"
        message = message.encode()
        self.name.setText(f'{senders_name}')
        self.client_socket.send(message)
        self.sendmessage.clear()
        return

    def initialize_socket(self, ip, port):
        ''' tcp socket을 생성하고 server와 연결 '''
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))

    def listen_thread(self):
        ''' 데이터 수신 Thread를 생성하고 시작한다 '''
        t = Thread(target=self.receive_message, args=(self.client_socket,))
        t.start()

    def receive_message(self, so):
        while True:
            buf = so.recv(256).decode('utf-8')
            chat_room_buf = buf
            if not buf:
                break
            if chat_room_buf[-5:] == '채팅방만듬':
                self.receivemessage.clear()
                self.chat_room_2.addItem(chat_room_buf[:-5])
            elif buf[-3:] == '채팅중':
                self.receivemessage.addItem(buf[:-3])
                # print(self.receive_message())
            # elif buf[-5:] == '채팅방지움':
            #     self.chat_room_2.clear()
            elif buf[-3:] == '방번호':
                self.receivemessage.addItem(buf[:-3])
        so.close()

if __name__ == "__main__":
    ip = '10.10.21.111'
    port = 9000
    app = QApplication(sys.argv)
    mainWindow = Main(ip, port)
    app.exec_()