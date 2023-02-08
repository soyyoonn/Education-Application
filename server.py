# threading 모듈을 이용한 TCP 멀티 채팅 서버 프로그램

import pymysql as ms
from socket import *
from threading import *
from datetime import datetime
import time
import json

from PyQt5.QtWidgets import QTableWidgetItem


class MultiChatServer:
    # 소켓을 생성하고 연결되면 accept_client() 호출
    def __init__(self):
        self.clients = []  # 접속된 클라이언트 소켓 목록
        self.final_received_message = ""  # 최종 수신 메시지
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip ='10.10.21.119'
        self.port = 9000
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
                incoming_message = c_socket.recv(256)
                print(incoming_message.decode(),41)
                if not incoming_message:  # 연결이 종료됨
                    break
            except:
                continue
            else:
                if incoming_message.decode()[-3:] == '로그인':
                    id = incoming_message.decode()[:-3]
                    id_check = id.split(":")
                    print(id_check, 55)
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    self.id = incoming_message.decode()[:-3]
                    sql = f"SELECT * FROM yh.join where id = '{id_check[0]}' and pw = '{id_check[1]}'"
                    cursor.execute(sql)
                    self.log = cursor.fetchall()
                    print(self.log, 70)
                    conn.close()
                    if self.log != ():
                        self.final_received_message = self.log[0][1] + "로그인"
                        print(self.final_received_message,"gh")

                    else:
                        print('아이디가 없음')
                        self.final_received_message = "오류"
                    self.send_all_clients(c_socket)
                    c_socket.send(self.final_received_message.encode())

                elif incoming_message.decode()[-8:] == 'QnA_page':
                    qna = incoming_message.decode()
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    # self.qna = incoming_message.decode()
                    sql = f"SELECT * FROM yh.qna"
                    cursor.execute(sql)
                    self.qna_page = cursor.fetchall()
                    conn.close()
                    print(self.qna_page,87)

                    if self.qna_page != ():
                        print(self.qna_page,156)
                        self.qq = json.dumps(self.qna_page) + "QnA_page"
                        c_socket.send(self.qq.encode())
                elif incoming_message.decode()[-12:] == 'consult_page':
                    # consult = incoming_message.decode()
                    # print(consult)
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    # self.qna = incoming_message.decode()
                    sql = f"SELECT * FROM yh.consult"
                    cursor.execute(sql)
                    self.consult_page = cursor.fetchall()
                    conn.close()
                    print(self.consult_page,104)

                    if self.consult_page != ():
                        self.consult_page_check = json.dumps(self.consult_page) + "consult_page"
                        c_socket.send(self.consult_page_check.encode())


                elif incoming_message.decode()[-3:] == 'QnA':
                    qna = incoming_message.decode()[:-3]
                    self.qna_check = qna.split(":")
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    self.qna = incoming_message.decode()[:-3]
                    sql = f"INSERT INTO yh.qna (name, qna, time) VALUES ('{self.qna_check[0]}','{self.qna_check[1]}',{'now()'})"
                    cursor.execute(sql)
                    conn.commit()
                    # sql = f"SELECT * FROM yh.qna where name = '{self.qna_check[0]}'"
                    sql = f"SELECT * FROM yh.qna"
                    cursor.execute(sql)
                    self.qna_all_check = cursor.fetchall()
                    conn.close()

                    if self.qna_all_check != ():
                        print(self.qna_all_check,156)
                        self.q = json.dumps(self.qna_all_check) + "QnA"
                        c_socket.send(self.q.encode())
                        # self.send_all_clients(c_socket)

                elif incoming_message.decode()[-7:] == 'consult':
                    consult = incoming_message.decode()[:-7]
                    self.consult = consult.split(":")
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    # self.consult = incoming_message.decode()[:-7]
                    sql = f"INSERT INTO yh.consult (name, content, time) VALUES ('{self.consult[0]}','{self.consult[1]}',{'now()'})"
                    cursor.execute(sql)
                    conn.commit()
                    sql = f"SELECT * FROM yh.consult where name = '{self.consult[0]}'"
                    cursor.execute(sql)
                    self.consult_check = cursor.fetchall()
                    conn.close()
                    i = self.consult_check
                    if self.consult_check != ():
                        cons = self.consult_check
                        for i in cons:
                            self.final_received_message = i[1] + ':' + i[2] + "consult"
                        self.send_all_clients(c_socket)

        c_socket.close()



    # 송신 클라이언트를 제외한 모든 클라이언트에게 메시지 전송
    def send_all_clients(self, senders_socket):
        for client in self.clients: # 목록에 있는 모든 소켓에 대해
            socket, (ip, port) = client
            # if socket is not senders_socket:  # 송신 클라이언트는 제외
            try:
                socket.sendall(self.final_received_message.encode())
            except:  # 연결 종료
                self.clients.remove(client)   # 소켓 제거
                print("{}, {} 연결이 종료되었습니다".format(ip, port))


if __name__ == "__main__":
    MultiChatServer()