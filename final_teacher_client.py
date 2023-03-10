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
        self.btn_home4.clicked.connect(self.chat_out)
        self.btn_update.clicked.connect(self.move_update)
        self.btn_enter.clicked.connect(self.quiz_update)
        self.btn_check.clicked.connect(self.move_check)
        self.btn_qna.clicked.connect(self.move_qna)
        self.btn_chat.clicked.connect(self.move_chat)
        self.btn_send.clicked.connect(self.send_chat)
        self.sendline.returnPressed.connect(self.send_chat)
        self.qnatable.cellChanged.connect(self.send_qna)
        self.qnatable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.quizupdatetable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def move_home(self):
        self.stackedWidget.setCurrentIndex(0)

    def move_update(self):
        self.stackedWidget.setCurrentIndex(1)

    def move_check(self):
        self.stackedWidget.setCurrentIndex(2)
        a = ['문제확인']
        b = json.dumps(a)
        self.client_socket.send(b.encode())

    def move_qna(self):
        self.stackedWidget.setCurrentIndex(3)
        b = ['000']
        table_qna = json.dumps(b)
        self.client_socket.send(table_qna.encode())

    def move_chat(self):
        self.stackedWidget.setCurrentIndex(4)
        user = ['접속자']
        userlist = json.dumps(user)
        self.client_socket.send(userlist.encode())

    def chat_out(self):
        self.stackedWidget.setCurrentIndex(0)
        self.chatlist.clear()

    def send_qna(self):
        self.data = self.showqna[self.qnatable.currentRow()]
        print(self.qnatable.currentRow())
        print(self.showqna[self.qnatable.currentRow()])
        self.row = self.qnatable.selectedItems()
        print(self.data, self.row, 5987561)
        number = self.row[0].text()    # 번호
        answer = self.row[-1].text()   # 답변
        print(answer, 321564)
        # qna_answer = number + ':' + answer + ':답변'
        a = [number, answer, '답변']
        qna_answer = json.dumps(a)
        self.client_socket.send(qna_answer.encode())

    def quiz_update(self):
        kind = self.kindline.text()
        quiz = self.quizline.text()
        answer = self.answerline.text()
        up = [kind, quiz, answer,'25','문제등록']
        update = json.dumps(up)
        self.client_socket.send(update.encode())

    def initialize_socket(self, ip, port):
        ''' tcp socket을 생성하고 server와 연결 '''
        self.client_socket = socket(AF_INET, SOCK_STREAM)  # 클라이언트 소켓 생성
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))  # 서버와 소켓 연결

    def send_chat(self):
        ''' message를 전송하는 버튼 콜백 함수 '''
        data = self.sendline.text()
        name = self.namebox.currentText()
        if data == '':
            return
        # message = ('교사' + ':' + data + ':' + '100').encode()  # 서버로 보낼 메시지
        message = ['교사', data, name , '100']
        msg = json.dumps(message)
        self.client_socket.send(msg.encode())  # 서버로 전송
        self.sendline.clear()  # 메시지 보내는 창 클리어
        # return 'break'


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
                print(msg,55555555)
                print(msg[-3:],88888)
                sibal_port = msg[:-2]



                if msg[-3:] == '000':
                    self.showqna = json.loads(msg[:-3])
                    print(self.showqna, 84)
                    Row = 0
                    self.qnatable.setRowCount(len(self.showqna))
                    for i in self.showqna:
                        self.qnatable.setItem(Row, 0, QTableWidgetItem(str(i[0])))  # 번호
                        self.qnatable.setItem(Row, 1, QTableWidgetItem(i[1]))       # 학생
                        self.qnatable.setItem(Row, 2, QTableWidgetItem(i[2]))       # 질문
                        self.qnatable.setItem(Row, 3, QTableWidgetItem(i[4]))       # 답변
                        Row += 1
                elif  buf[-2:] == "포트":
                    print("왔따")
                    print(buf[:-2])
                    self.sibal_port = buf[:-2]

                elif msg[-2:] == '답변':
                    answer_check = json.loads(msg[:-2])
                    print(answer_check, 1561231)
                    Row = 0
                    self.qnatable.setRowCount(len(answer_check))
                    for i in self.q:
                        self.qnatable.setItem(Row, 0, QTableWidgetItem(str(i[0])))  # 번호
                        self.qnatable.setItem(Row, 1, QTableWidgetItem(i[1]))       # 학생
                        self.qnatable.setItem(Row, 2, QTableWidgetItem(i[2]))       # 질문
                        self.qnatable.setItem(Row, 3, QTableWidgetItem(i[4]))       # 답변
                        Row += 1

                elif msg[-4:] == '문제등록':
                    update = json.loads(msg[:-4])
                    print(update, 999)
                    Row = 0
                    self.quizupdatetable.setRowCount(len(update))
                    for i in update:
                        self.quizupdatetable.setItem(Row, 0, QTableWidgetItem(i[1]))  # 종류
                        self.quizupdatetable.setItem(Row, 1, QTableWidgetItem(i[2]))  # 문제
                        self.quizupdatetable.setItem(Row, 2, QTableWidgetItem(i[3]))  # 정답
                        self.quizupdatetable.setItem(Row, 3, QTableWidgetItem(i[4]))  # 점수
                        Row += 1
                    self.kindline.clear()
                    self.quizline.clear()
                    self.answerline.clear()

                elif msg[-7:] == 'consult':
                    print(msg,5748956)
                    a = msg[:-10]
                    print(msg, "-7데이터")
                    if '교사' in msg:
                        self.chatlist.addItem(msg[:-10])  # 채팅창에 메시지 추가

                    elif self.namebox.currentText() in msg:
                        self.chatlist.addItem(msg[:-7])
                    # self.chatlist.scrollToBottom(])

                elif msg[-3:] == '접속자':
                    self.namebox.clear()
                    userlist = json.loads(msg[:-3])
                    print(userlist, 98989898)
                    for i in range(len(userlist)):
                        self.namebox.addItem(userlist[i])

                elif msg[-4:] == '문제확인':

                    solving_quiz_data = json.loads(msg[:-4])
                    print("Aasdfasdfsadf")
                    print(solving_quiz_data[0][4])

                    Row = 0
                    self.quizchecktable.setRowCount(len(solving_quiz_data))
                    for i in solving_quiz_data:
                        self.quizchecktable.setItem(Row, 0, QTableWidgetItem(i[1]))  # 학생ID
                        self.quizchecktable.setItem(Row, 1, QTableWidgetItem(str(i[4])))  # 문제번호
                        self.quizchecktable.setItem(Row, 2, QTableWidgetItem(i[5]))  # 정답확인
                        self.quizchecktable.setItem(Row, 3, QTableWidgetItem(i[6]))  # 소요시간
                        Row += 1


            except:
                pass
        so.close()


if __name__ == "__main__":
    ip = '10.10.21.111'
    port = 9999
    app = QApplication(sys.argv)
    mainWindow = Main(ip, port)
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainWindow)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1060)
    widget.show()
    app.exec_()