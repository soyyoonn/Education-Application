import sys
import pymysql
import json
from socket import *
from threading import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
form_class = uic.loadUiType('./client_forteacher.ui')[0]

class Main(QMainWindow, form_class):
    client_socket = None
    def __init__(self, ip, port):
        super().__init__()
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)
        self.initialize_socket(ip, port)
        self.listen_thread()
        self.btn_home.clicked.connect(self.move_home)
        self.btn_home2.clicked.connect(self.move_home)
        self.btn_home3.clicked.connect(self.move_home)
        self.btn_home4.clicked.connect(self.move_home)
        self.btn_update.clicked.connect(self.move_update)
        # self.btn_enter.clicked.connect(self.quiz_update)
        self.btn_check.clicked.connect(self.move_check)
        self.btn_qna.clicked.connect(self.move_qna)
        self.btn_chat.clicked.connect(self.move_chat)
        self.btn_send.clicked.connect(self.send_chat)

    def move_home(self):
        self.stackedWidget.setCurrentIndex(0)

    def move_update(self):
        self.stackedWidget.setCurrentIndex(1)

    def move_check(self):
        self.stackedWidget.setCurrentIndex(2)

    def move_qna(self):
        self.stackedWidget.setCurrentIndex(3)
        self.client_socket.send('000'.encode())

    def move_chat(self):
        self.stackedWidget.setCurrentIndex(4)

    # def quiz_update(self):
    #
    #     for i in range(len(self.result)):
    #         print(self.result[i])
    #     self.quizupdatetable.setRowCount(len(self.result))
    #     Row = 0
    #
    #     for k in self.result:
    #         self.covid_table.setItem(Row, 0, QTableWidgetItem(k[0]))         # 번호
    #         self.covid_table.setItem(Row, 1, QTableWidgetItem(k[2]))         # 문제
    #         self.covid_table.setItem(Row, 2, QTableWidgetItem(k[4]))    # 정답
    #         Row += 1

    def send_qna(self):
        self.qnatable.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.data = self.showqna[self.qnatable.currentRow()]
        self.row = self.qnatable.selectedItems()
        print(self.data, self.row)
        answer = self.row[3].text()  # 답변
        print(answer)
        qna_answer= (answer + ':답변').encode()
        self.client_socket.send(qna_answer)


    def initialize_socket(self, ip, port):
        ''' tcp socket을 생성하고 server와 연결 '''
        self.client_socket = socket(AF_INET, SOCK_STREAM)  # 클라이언트 소켓 생성
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))  # 서버와 소켓 연결

    def send_chat(self):
        ''' message를 전송하는 버튼 콜백 함수 '''
        data = self.sendmessage.text()
        if data == '':
            return
        message = (self.senders_name + ':' + data + ':' + self.roomname + ':' + '001').encode()  # 서버로 보낼 메시지
        self.client_socket.send(message)  # 서버로 전송
        self.sendmessage.clear()  # 메시지 보내는 창 클리어
        return 'break'

    def listen_thread(self):
        ''' 데이터 수신 Thread를 생성하고 시작한다 '''
        t = Thread(target=self.receive_message, args=(self.client_socket,), daemon=True)
        t.start()

    def receive_message(self, so):  # 서버에서 메시지를 받는다
        while True:
            try:
                buf = so.recv(9999)  # 서버로부터 문자열 수신
                msg = buf.decode()
                if not buf:  # 문자열 없으면 연결이 종료됨
                    break

                if msg[-3:] == '000':
                    self.showqna = json.loads(msg[:-3])
                    print(self.showqna, 84)
                    print(len(self.showqna))
                    Row = 0
                    self.qnatable.setRowCount(len(self.showqna))
                    for i in self.showqna:
                        self.qnatable.setItem(Row, 0, QTableWidgetItem(str(i[0])))  # 번호
                        self.qnatable.setItem(Row, 1, QTableWidgetItem(i[1]))       # 학생
                        self.qnatable.setItem(Row, 2, QTableWidgetItem(i[2]))       # 질문
                        self.qnatable.setItem(Row, 3, QTableWidgetItem(i[4]))       # 답변
                        Row += 1

                elif msg[-2:] == '답변':
                    self.answer_check = json.loads(msg[:-2])
                    print(self.answer_check, 1561231)
                    Row = 0
                    self.qnatable.setRowCount(len(self.answer_check))
                    for i in self.q:
                        self.qnatable.setItem(Row, 0, QTableWidgetItem(str(i[0])))  # 번호
                        self.qnatable.setItem(Row, 1, QTableWidgetItem(i[1]))       # 학생
                        self.qnatable.setItem(Row, 2, QTableWidgetItem(i[2]))       # 질문
                        self.qnatable.setItem(Row, 3, QTableWidgetItem(i[4]))       # 답변
                        Row += 1
                so.close()

            except:
                pass
        so.close()


if __name__ == "__main__":
    ip = '10.10.21.101'
    port = 9180
    app = QApplication(sys.argv)
    mainWindow = Main(ip, port)
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainWindow)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1060)
    widget.show()
    app.exec_()