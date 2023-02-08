# threading 모듈을 이용한 TCP 멀티 채팅 서버 프로그램

import pymysql as ms
from socket import *
from threading import *
from datetime import datetime
import time
import json
import random
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtWidgets import *

class MultiChatServer:
    # 소켓을 생성하고 연결되면 accept_client() 호출
    def __init__(self):
        self.clients = []  # 접속된 클라이언트 소켓 목록
        self.final_received_message = ""  # 최종 수신 메시지
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip ='10.10.21.119'
        self.port = 9999
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s_sock.bind((self.ip, self.port))
        print("클라이언트 대기 중...")
        self.s_sock.listen(100)
        self.accept_client()

    # 연결 클라이언트 소켓을 목록에 추가하고 스레드를 생성하여 데이터를 수신한다
    def accept_client(self):
        while True:
            client = c_socket, (ip, port) = self.s_sock.accept()
            if client not in self.clients:
                self.clients.append(client)   # 접속된 소켓을 목록에 추가
            print(ip, ':', str(port), ' 가 연결되었습니다')
            cth = Thread(target=self.receive_messages, args=(c_socket,))  # 수신 스레드
            cth.start()   # 스레드 시작

    # 데이터를 수신하여 모든 클라이언트에게 전송한다

    def receive_messages(self, c_socket):

        while True:
            try:
                now = datetime.now()
                self.now_time = now.strftime('%Y-%m-%d %H:%M:%S')
                incoming_message = c_socket.recv(9999)
                k = json.loads(incoming_message.decode())
                # print(incoming_message.decode(),41)
                if not incoming_message:  # 연결이 종료됨
                    break
            except:
                continue
            else:
                self.incoming_message = k
                print(self.incoming_message)
                if self.incoming_message[-1] == '로그인':
                    # id = incoming_message.decode()[:-3]
                    # id_check = id.split(":")
                    # print(id_check, 55)
                    # self.incoming_message[0] 아이디
                    # self.incoming_message[1] 비번
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    sql = f"SELECT * FROM yh.join where id = '{self.incoming_message[0]}' and pw = '{self.incoming_message[1]}'"
                    cursor.execute(sql)
                    self.log = cursor.fetchall()
                    # print(self.log, 70)
                    conn.close()
                    if self.log != ():
                        self.final_received_message = self.log[0][1] + "로그인"
                        print(self.final_received_message,"gh")

                    else:
                        print('아이디가 없음')
                        self.final_received_message = "오류"
                    self.send_all_clients(c_socket)
                    c_socket.send(self.final_received_message.encode())

                elif self.incoming_message[-1] == 'QnA_page':
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    sql = f"SELECT * FROM yh.qna"
                    cursor.execute(sql)
                    self.qna_page = cursor.fetchall()
                    conn.close()

                    if self.qna_page != ():
                        self.qq = json.dumps(self.qna_page) + "QnA_page"
                        c_socket.send(self.qq.encode())

                elif self.incoming_message[0] == 'consult_page':
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    sql = f"SELECT * FROM yh.consult "
                    cursor.execute(sql)
                    self.consult_page = cursor.fetchall()
                    print(self.consult_page,101)
                    conn.close()

                    if self.consult_page != ():
                        self.consult_page_check = json.dumps(self.consult_page) + "consult_page"
                        c_socket.send(self.consult_page_check.encode())
                        self.send_all_clients(c_socket)

                elif self.incoming_message[0] == 'quiz_page':
                    # print(self.incoming_message[0],111)
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    sql = f"SELECT * FROM yh.quiz"
                    cursor.execute(sql)
                    # k = random.randint(0,3)
                    # a = random.sample(range(8),4)
                    # print(a,119)
                    self.quiz_page = cursor.fetchall()
                    # print(self.quiz_page,119)
                    # print(self.quiz_page[k],120)
                    sql = f"SELECT * FROM yh.quiz ORDER BY RAND() LIMIT 4"
                    cursor.execute(sql)
                    self.quiz_count_four = cursor.fetchall()
                    print(self.quiz_count_four,127)
                    conn.close()

                    if self.quiz_page != ():
                        print(131)
                        self.quiz_page_check = json.dumps(self.quiz_count_four[0]) + "quiz_page1"
                        c_socket.send(self.quiz_page_check.encode())
                        self.send_all_clients(c_socket)
                    if self.quiz_page != ():
                        self.quiz_page_check = json.dumps(self.quiz_count_four[1]) + "quiz_page2"
                        c_socket.send(self.quiz_page_check.encode())
                        self.send_all_clients(c_socket)
                    if self.quiz_page != ():
                        self.quiz_page_check = json.dumps(self.quiz_count_four[2]) + "quiz_page3"
                        c_socket.send(self.quiz_page_check.encode())
                        self.send_all_clients(c_socket)
                    if self.quiz_page != ():
                        self.quiz_page_check = json.dumps(self.quiz_count_four[3]) + "quiz_page4"
                        c_socket.send(self.quiz_page_check.encode())
                        self.send_all_clients(c_socket)

                elif self.incoming_message[-1] == 'QnA':
                    # qna = incoming_message.decode()[:-1]
                    # self.qna_check = qna.split(":")
                    # self.incoming_message[0]  이름
                    # self.incoming_message[1]  큐앤에이내용
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    sql = f"INSERT INTO yh.qna (name, qna, time) VALUES ('{self.incoming_message[0]}','{self.incoming_message[1]}',{'now()'})"
                    cursor.execute(sql)
                    conn.commit()
                    # sql = f"SELECT * FROM yh.qna where name = '{self.incoming_message[0]}'"
                    sql = f"SELECT * FROM yh.qna"
                    cursor.execute(sql)
                    self.qna_all_check = cursor.fetchall()
                    conn.close()

                    if self.qna_all_check != ():
                        print(self.qna_all_check,129)
                        self.q = json.dumps(self.qna_all_check) + "QnA"
                        c_socket.send(self.q.encode())
                        self.send_all_clients(c_socket)


                elif self.incoming_message[-1] == 'QnA':
                    # qna = incoming_message.decode()[:-1]
                    # self.qna_check = qna.split(":")
                    # self.incoming_message[0]  이름
                    # self.incoming_message[1]  큐앤에이내용
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    sql = f"INSERT INTO yh.qna (name, qna, time) VALUES ('{self.incoming_message[0]}','{self.incoming_message[1]}',{'now()'})"
                    cursor.execute(sql)
                    conn.commit()
                    # sql = f"SELECT * FROM yh.qna where name = '{self.incoming_message[0]}'"
                    sql = f"SELECT * FROM yh.qna"
                    cursor.execute(sql)
                    self.qna_all_check = cursor.fetchall()
                    conn.close()

                    if self.qna_all_check != ():
                        print(self.qna_all_check,129)
                        self.q = json.dumps(self.qna_all_check) + "QnA"
                        c_socket.send(self.q.encode())
                        self.send_all_clients(c_socket)

                elif self.incoming_message[-1] == 'consult':
                    # self.incoming_message[0] 아이디
                    # self.incoming_message[1] 상담내용
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    # self.consult = incoming_message.decode()[:-7]
                    sql = f"INSERT INTO yh.consult (name, content, time) VALUES ('{self.incoming_message[0]}','{self.incoming_message[1]}',{'now()'})"
                    cursor.execute(sql)
                    conn.commit()
                    sql = f"SELECT * FROM yh.consult where name = '{self.incoming_message[0]}'"
                    cursor.execute(sql)
                    self.consult_check = cursor.fetchall()
                    conn.close()
                    i = self.consult_check
                    if self.consult_check != ():
                        cons = self.consult_check
                        for i in cons:
                            self.final_received_message = i[1] + ':' + i[2] + "consult"
                        self.send_all_clients(c_socket)

                elif self.incoming_message[-3:] == '000':
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh', charset='utf8')
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM yh.qna")
                    self.qnalist = cursor.fetchall()
                    print(self.qnalist)
                    conn.close()
                    qnalist = json.dumps(self.qnalist)
                    print(qnalist)
                    c_socket.sendall((qnalist + '000').encode())  # 클라이언트에 전송

                elif self.incoming_message[-3:] == ':답변':
                    # try:
                    number = self.incoming_message.split(":")[0]
                    answer = self.incoming_message.split(":")[1]
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh', charset='utf8')
                    cursor = conn.cursor()
                    sql = f"UPDATE yh.qna SET respond={answer} WHERE respond = 'N' and num ='{number}' "
                    cursor.execute(sql)
                    conn.commit()
                    sql = f"SELECT * FROM yh.qna where num = '{number}'"
                    cursor.execute(sql)
                    self.qna_answer= cursor.fetchall()
                    print(self.qna_answer, 152)
                    qna_answer = json.dumps(self.qna_answer)
                    c_socket.sendall((qna_answer + ':답변').encode())
                    conn.close()

                elif self.incoming_message[-1] == 'quiz_1':
                    # self.incoming_message[0]  이름
                    # self.incoming_message[1]  문제
                    # self.incoming_message[2]  선택한 답
                    # self.incoming_message[3]  시작시간
                    # self.incoming_message[4]  제출시간
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    sql = f"INSERT INTO yh.quiz_solving (name, quiz, answer, start_time, end_time) VALUES ('{self.incoming_message[0]}','{self.incoming_message[1]}','{self.incoming_message[2]}','{self.incoming_message[3]}','{self.incoming_message[4]}')"
                    cursor.execute(sql)
                    conn.commit()
                    sql = f"SELECT * FROM yh.quiz_solving"
                    cursor.execute(sql)
                    self.quiz_solving_check = cursor.fetchall()
                    # sql = f"SELECT * FROM yh.quiz_solving WHERE quiz  in (select quiz from yh.quiz) order by num desc limit 2"
                    # cursor.execute(sql)
                    # self.quiz_solving = cursor.fetchall()
                    conn.close()
                    print(self.quiz_solving_check,249)
                    # print(self.quiz_solving,250)
                    #
                    # if self.qna_all_check != ():
                    #     print(self.qna_all_check,129)
                    #     self.q = json.dumps(self.qna_all_check) + "QnA"
                    #     c_socket.send(self.q.encode())
                    #     self.send_all_clients(c_socket)

        c_socket.close()



    # 송신 클라이언트를 제외한 모든 클라이언트에게 메시지 전송
    def send_all_clients(self, senders_socket):
        for client in self.clients: # 목록에 있는 모든 소켓에 대해
            socket, (ip, port) = client
            try:
                socket.sendall(self.final_received_message.encode())
            except:  # 연결 종료
                self.clients.remove(client)   # 소켓 제거
                print("{}, {} 연결이 종료되었습니다".format(ip, port))


if __name__ == "__main__":
    MultiChatServer()