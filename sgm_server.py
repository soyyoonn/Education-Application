# threading 모듈을 이용한 TCP 멀티 채팅 서버 프로그램

import pymysql as ms
from socket import *
from threading import *
from datetime import datetime
import time
import json
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtWidgets import *

class MultiChatServer:
    # 소켓을 생성하고 연결되면 accept_client() 호출
    def __init__(self):
        self.clients = []  # 접속된 클라이언트 소켓 목록
        self.final_received_message = ""  # 최종 수신 메시지
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip = '10.10.21.101'
        self.port = 9180
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
                print(incoming_message.decode(),41)
                if not incoming_message:  # 연결이 종료됨
                    break
            except:
                continue
            else:
                self.incoming_message = k

                if self.incoming_message[-1] == '로그인':
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
                    print(self.incoming_message[0],94)
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    sql = f"SELECT * FROM yh.consult"
                    cursor.execute(sql)
                    self.consult_page = cursor.fetchall()
                    print(self.consult_page,101)
                    conn.close()

                    if self.consult_page != ():
                        self.consult_page_check = json.dumps(self.consult_page) + "consult_page"
                        c_socket.send(self.consult_page_check.encode())
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

                elif self.incoming_message[-1] == '000':
                    print(self.incoming_message, 3564231)
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

                elif self.incoming_message[-1] == '답변':
                    print(self.incoming_message, 56546)
                    number = self.incoming_message[0]
                    answer = self.incoming_message[1]
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh', charset='utf8')
                    cursor = conn.cursor()
                    sql = f"UPDATE yh.qna SET respond= '{answer}' WHERE num = '{number}' "  # respond = 'n' 삭제
                    cursor.execute(sql)
                    conn.commit()
                    sql = f"SELECT * FROM yh.qna"
                    cursor.execute(sql)
                    self.qna_answer= cursor.fetchall()
                    print(self.qna_answer, 152)
                    qna_answer = json.dumps(self.qna_answer)
                    c_socket.sendall((qna_answer + '답변').encode())
                    conn.close()

                # elif self.incoming_message[-1] == '100': # 상담 채팅
                #     now = datetime.now()
                #     self.now_time = now.strftime('%Y-%m-%d %H:%M:%S')
                #     self.m = self.final_received_message.split(':')
                #     print(self.m)
                #     conn = ms.connect(host='10.10.21.111', port=3306, user='chat', password='0000', db='network')
                #     cursor = conn.cursor()
                #     # DB에 데이터 저장
                #     cursor.execute(
                #         f"INSERT INTO chat (send, message, time, IP, PORT, roomname) VALUES('{self.m[0]}','{self.m[1]}', '{self.now_time}','{self.add[0]}','{self.add[1]}','{self.m[2]}')")
                #     conn.commit()
                #     conn.close()

                elif self.incoming_message[-1] == '문제등록':
                    print(self.incoming_message, 2222233333)
                    kind = self.incoming_message[0]
                    quiz = self.incoming_message[1]
                    answer = self.incoming_message[2]
                    points = self.incoming_message[3]
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='sy_sgm', charset='utf8')
                    cursor = conn.cursor()
                    sql = f"INSERT INTO sy_sgm.quiz_update (kind, quiz, answer, points) VALUES ('{kind}','{quiz}','{answer}','{points}')"
                    cursor.execute(sql)
                    conn.commit()
                    sql = f"SELECT * FROM sy_sgm.quiz_update"
                    cursor.execute(sql)
                    self.update = cursor.fetchall()
                    print(self.update, 152555555)
                    quiz_update = json.dumps(self.update)
                    c_socket.sendall((quiz_update + '문제등록').encode())
                    conn.close()



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