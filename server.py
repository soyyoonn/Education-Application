# threading 모듈을 이용한 TCP 멀티 채팅 서버 프로그램

import pymysql as ms
from socket import *
from threading import *
from datetime import datetime
import time

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

                if not incoming_message:  # 연결이 종료됨
                    break
            except:
                continue
            else:
                if incoming_message.decode()[-3:] == '아이디':
                    id = incoming_message[:-3].decode()
                    print(id)
                    id = incoming_message.decode()[:-3]
                    print(id)
                    # kk = eval(a)
                    # print(kk)
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    self.id = incoming_message.decode()[:-3]
                    sql = f"INSERT INTO join (name,id,pw,nickname,tel,division) VALUES ('{kk[0]}:{kk[1]}',{'now()'},'{kk[2]}')"
                    cursor.execute(sql)
                    sql2 = f"SELECT * FROM CHAT"
                    cursor.execute(sql2)
                    conn.commit()
                    self.chat_check = cursor.fetchall()
                    conn.close()
                    self.final_received_message = kk[0] + " : " + kk[1] + "채팅중"
                    self.send_all_clients(c_socket)

                elif incoming_message.decode()[-3:] == '방번호':
                    chat_room_name = incoming_message.decode()[:-3]

                    conn = ms.connect(host='10.10.21.116', port=3306, user='talk_admin', password='admin1234',
                                      db='talk',
                                      charset='utf8')
                    cursor = conn.cursor()
                    sql = f"SELECT message from chat where chat_room_name = '{chat_room_name}'"
                    cursor.execute(sql)
                    self.room_name_check = cursor.fetchall()
                    print(self.room_name_check)
                    conn.close()
                    for x in self.room_name_check:
                        time.sleep(0.001)
                        self.final_received_message = x[0] + '방번호'
                        # self.send_all_clients(c_socket)
                        c_socket.send(self.final_received_message.encode())

                elif incoming_message.decode()[-5:] == '채팅방만듬':

                    conn = ms.connect(host='10.10.21.116', port=3306, user='talk_admin', password='admin1234',
                                      db='talk',
                                      charset='utf8')
                    cursor = conn.cursor()
                    self.room_name = incoming_message.decode()[:-5]
                    sql = f"INSERT INTO room (name) VALUES ('{self.room_name}')"
                    cursor.execute(sql)
                    conn.commit()
                    sql = f"SELECT * from room where name ='{self.room_name}'"
                    cursor.execute(sql)
                    self.room_check = cursor.fetchall()
                    print(self.room_check)
                    conn.close()
                    for x in self.room_check:
                        print(x)
                        time.sleep(0.001)
                        self.final_received_message = x[1] + '채팅방만듬'
                        self.send_all_clients(c_socket)

                elif incoming_message.decode()[-2:] == '입장':

                    conn = ms.connect(host='10.10.21.116', port=3306, user='talk_admin', password='admin1234',
                                      db='talk',
                                      charset='utf8')
                    cursor = conn.cursor()
                    self.join_name = incoming_message.decode()[:-2]
                    sql = f"INSERT INTO member (uname) VALUES ('{self.join_name}')"
                    cursor.execute(sql)
                    conn.commit()
                    sql = f"SELECT * from room"
                    cursor.execute(sql)
                    self.join_check = cursor.fetchall()
                    conn.close()
                    for x in self.join_check:
                        print(x)
                        time.sleep(0.001)
                        self.final_received_message = x[1] + '채팅방만듬'
                        c_socket.send(self.final_received_message.encode())
                        # self.send_all_clients(c_socket)
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