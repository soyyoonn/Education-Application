import pymysql
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
from socket import *
from threading import *


form_class = uic.loadUiType('student.ui')[0]

class Student(QWidget, form_class):
    client_socket = None

    def __init__(self, ip, port):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.stackedWidget.setCurrentIndex(1)
        self.initialize_socket(ip, port)
        self.listen_thread()
        self.join_btn.clicked.connect(self.join_page)
        # self.back_btn.clicked.connect(self.login_page)
        self.log_btn.clicked.connect(self.Login)
        self.login_btn.clicked.connect(self.login_page)

    def login_page(self):
        self.stackedWidget.setCurrentIndex(0)
        self.login_btn.setText("로그아웃")

    def join_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def Login(self):
        self.id = self.log_id.text()
        self.pw = self.log_pw.text()
        id = (self.id + '아이디').encode()
        pw = (self.pw + '아이디').encode()
        self.client_socket.send(id)
        self.client_socket.send(pw)
        # self.id.clear()
        # self.pw.clear()
        self.stackedWidget.setCurrentIndex(1)

    def receive_message(self, so):
        while True:
            print(46)
            buf = so.recv(256).decode('utf-8')
            print(buf,48)
            if not buf:
                break
            if buf[-3:] == '아이디':
                print(52)
                a = buf[:-3]
                print(a,54)
            # elif buf[-4:] == '비밀번호':
            #     print(buf[:-4].decode())
        so.close()


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


if __name__ == "__main__":
    ip = '10.10.21.119'
    port = 9000
    app = QApplication(sys.argv)
    mainWindow = Student(ip, port)
    app.exec_()