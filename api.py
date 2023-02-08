import json
from socket import *
from threading import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets

form_class = uic.loadUiType('student.ui')[0]

class Student(QWidget, form_class):
    client_socket = None

    def __init__(self, ip, port):
        super().__init__()
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_2.setCurrentIndex(5)
        self.show()
        self.initialize_socket(ip, port)
        self.listen_thread()
        self.join_btn.clicked.connect(self.join_page)
        self.log_btn.clicked.connect(self.Login)
        self.login_btn.clicked.connect(self.login_page)
        self.qna_btn.clicked.connect(self.QnA_page)
        self.qna_send_btn.clicked.connect(self.QnA)
        self.consult_btn.clicked.connect(self.Consult_page)
        self.consult_send_btn.clicked.connect(self.Consult)


    def Consult(self):
        self.consult = self.consult_send.text()
        consultor = (self.log + ":" + self.consult + ":" + 'consult').encode()
        print(consultor.decode(),39)
        self.client_socket.send(consultor)
        self.consult_send.clear()
    def Consult_page(self):
        consult_page = ('consult_page').encode()
        self.client_socket.send(consult_page)
        self.stackedWidget_2.setCurrentIndex(4)
    def QnA_page(self):
        qna_page = ('QnA_page').encode()
        self.client_socket.send(qna_page)
        self.stackedWidget_2.setCurrentIndex(3)

    def QnA(self):
        self.qna = self.qna_send.text()
        print(self.qna,34)
        qna = (self.log + ":" + self.qna + ":" + 'QnA').encode()
        print(qna.decode(),36)
        self.client_socket.send(qna)
    def login_page(self):
        self.stackedWidget.setCurrentIndex(0)
        self.login_btn.setText("로그아웃")

    def join_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def Login(self):
        self.id = self.log_id.text()
        self.pw = self.log_pw.text()
        id = (self.id +":" + self.pw + '로그인').encode()
        self.client_socket.send(id)
        self.receive_log(self.client_socket,)


    def receive_log(self, so):
        buf = so.recv(8192).decode()
        print(buf)
        if not buf:
            pass
        if buf[-3:] == '로그인':
            self.log = buf[:-3]
            QMessageBox.information(self,"로그인",f"{self.log}님 로그인 하셨습니다.")
            self.stackedWidget.setCurrentIndex(1)
            self.log_name.setText(f"{self.log}님 반갑습니다.")

        elif buf == '오류':
            log = buf
            QMessageBox.critical(self, "오류", f"정보가 일치하지 않습니다.")

    def receive_message(self, so):
        while True:
            buf = so.recv(8192).decode()
            if not buf:
                break
            if buf[-12:] == 'consult_page':
                self.consult_page = buf
                self.con = json.loads(self.consult_page[:-12])
                for i in range(len(self.con)):
                    self.consultWidget.addItem(self.con[i][1] + ':' + self.con[i][2])
            if buf[-8:] == 'QnA_page':
                self.qna_page = buf
                self.qq = json.loads(self.qna_page[:-8])
                Row = 0
                self.qna_tableWidget.setRowCount(len(self.qq))
                for i in self.qq:
                    self.qna_tableWidget.setItem(Row, 0, QTableWidgetItem(i[1]))  # 이름
                    self.qna_tableWidget.setItem(Row, 1, QTableWidgetItem(i[2]))  # 내용
                    self.qna_tableWidget.setItem(Row, 2, QTableWidgetItem(i[3]))  # 시간
                    self.qna_tableWidget.setItem(Row, 3, QTableWidgetItem(i[4]))  # 답변여부
                    Row += 1

            if buf[-3:] == 'QnA':
                print(buf)
                self.qna_all_check = buf[:-3]
                self.q = json.loads(self.qna_all_check)

                Row = 0
                self.qna_tableWidget.setRowCount(len(self.q))
                for i in self.q:
                    self.qna_tableWidget.setItem(Row, 0, QTableWidgetItem(i[1]))  # 이름
                    self.qna_tableWidget.setItem(Row, 1, QTableWidgetItem(i[2]))  # 내용
                    self.qna_tableWidget.setItem(Row, 2, QTableWidgetItem(i[3]))  # 시간
                    self.qna_tableWidget.setItem(Row, 3, QTableWidgetItem(i[4]))  # 답변여부
                    Row += 1

            elif buf[-7:] == 'consult':
                self.cons = buf[:-7]
                print(self.cons)
                self.consultWidget.addItem(str(self.cons))


        so.close()


    def initialize_socket(self, ip, port):
        ''' tcp socket을 생성하고 server와 연결 '''
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))

    def listen_thread(self):
         ''' 데이터 수신 Thread를 생성하고 시작한다 '''
         t = Thread(target=self.receive_message, args=(self.client_socket,), daemon=True)
         t.start()


if __name__ == "__main__":
    ip = '10.10.21.119'
    port = 9000
    app = QApplication(sys.argv)
    mainWindow = Student(ip, port)
    app.exec_()