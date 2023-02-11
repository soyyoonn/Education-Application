import pymysql as ms
import json
from socket import *
from threading import *
from datetime import datetime
import time
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtWidgets import *

class MultiChatServer:
    # 소켓을 생성하고 연결되면 accept_client() 호출
    def __init__(self):
        self.clients = []   # 접속된 클라이언트 소켓 목록
        self.final_received_message = ""   # 최종 수신 메시지
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip ='10.10.21.101'
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
                # now = datetime.now()
                # self.now_time = now.strftime('%Y-%m-%d %H:%M:%S')
                incoming_message = c_socket.recv(9999)
                print(incoming_message.decode(),41)
                if not incoming_message:  # 연결이 종료됨
                    break
            except:
                continue

            else:
                self.incoming_message = incoming_message.decode()

                if self.incoming_message[-3:] == '000':
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

                # self.send_all_clients(c_socket)
                    # except:
                    #     pass
        c_socket.close()



    # 모든 클라이언트에게 메시지 전송
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