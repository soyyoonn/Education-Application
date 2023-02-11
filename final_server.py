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
        self.userlist = []  # 접속자 리스트
        self.clients = []  # 접속된 클라이언트 소켓 목록
        self.final_received_message = ""  # 최종 수신 메시지
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip ='10.10.21.111'
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
            self.sibal_port = []
            self.sibal_port.append(str(port))
            sibal = (str(port) + "포트").encode()
            c_socket.send(sibal)
            self.send_all_clients(c_socket)


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
                        print(self.final_received_message, "gh")
                        print(self.log, 898989898)
                        self.userlist.append(self.log[0][1])
                        # client = c_socket, (ip, port) = self.s_sock.accept()
                        print()

                        print(self.userlist, 5656)
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

                # elif self.incoming_message[0] == 'consult_page':
                #     conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                #                       db='yh',
                #                       charset='utf8')
                #     cursor = conn.cursor()
                #     sql = f"SELECT * FROM yh.consult "
                #     cursor.execute(sql)
                #     self.consult_page = cursor.fetchall()
                #     print(self.consult_page,101)
                #     conn.close()

                    if self.consult_page != ():
                        self.consult_page_check = json.dumps(self.consult_page) + "consult_page"
                        c_socket.send(self.consult_page_check.encode())
                        self.send_all_clients(c_socket)

                elif self.incoming_message[-1] == 'quiz_page':
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    print(self.incoming_message[0], '헤헤헤')
                    cursor.execute(f"DELETE FROM yh.quiz_solving WHERE name = '{self.incoming_message[0]}';")
                    conn.commit()
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

                    conn.close()
                    print(self.quiz_count_four,125125125125125125)

                    if self.quiz_count_four != ():
                        self.quiz_page_check = json.dumps(self.quiz_count_four[0]) + "quiz_page1"
                        c_socket.send(self.quiz_page_check.encode())
                        self.send_all_clients(c_socket)
                        time.sleep(0.2)
                        # print(self.quiz_count_four[0],'1번문제')

                        self.quiz_page_check = json.dumps(self.quiz_count_four[1]) + "quiz_page2"
                        c_socket.send(self.quiz_page_check.encode())
                        self.send_all_clients(c_socket)
                        time.sleep(0.2)
                        # print(self.quiz_count_four[1],'2번문제')

                        self.quiz_page_check = json.dumps(self.quiz_count_four[2]) + "quiz_page3"
                        c_socket.send(self.quiz_page_check.encode())
                        self.send_all_clients(c_socket)
                        time.sleep(0.2)
                        # print(self.quiz_count_four[2],'3번문제')

                        self.quiz_page_check = json.dumps(self.quiz_count_four[3]) + "quiz_page4"
                        c_socket.send(self.quiz_page_check.encode())
                        self.send_all_clients(c_socket)
                        time.sleep(0.2)
                        # print(self.quiz_count_four[3],'4번문제')


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

                  if self.incoming_message != ():
                        cons = self.incoming_message
                        print(cons)
                        print(cons[0][0])
                        print(cons[0])
                        for i in cons:
                            self.final_received_message = self.incoming_message[0] + ':' + self.incoming_message[1] +  self.incoming_message[2]
                        print(self.final_received_message, "확인")
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

                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',

                                      db='yh',

                                      charset='utf8')

                    cursor = conn.cursor()
                    print(self.incoming_message, "확인해보까")
                    sql = f"SELECT * FROM yh.quiz where number = '{self.incoming_message[0]}';"

                    print(sql)
                    print(self.incoming_message)
                    cursor.execute(sql)  # 문제번호로 quiz테이블 조회

                    sol_check_row = cursor.fetchall()

                    print(sol_check_row[0][3], self.incoming_message[3])

                    if sol_check_row[0][3] == self.incoming_message[
                        3]:  ##quiz테이블의 solution 값과 클라이언트에서 제출클릭하여 전송한 o,x의 값이 같으면

                        cursor.execute(
                            f"INSERT INTO yh.quiz_solving (name, quiz, answer, quiz_num, checkci, count_time) VALUES ('{self.incoming_message[1]}','{self.incoming_message[2]}','{self.incoming_message[3]}',{sol_check_row[0][0]},'correct','{self.incoming_message[4]}')")

                    else:  # 틀리면

                        cursor.execute(
                            f"INSERT INTO yh.quiz_solving (name, quiz, answer, quiz_num, checkci, count_time) VALUES ('{self.incoming_message[1]}','{self.incoming_message[2]}','{self.incoming_message[3]}',{sol_check_row[0][0]},'incorrect','{self.incoming_message[4]}')")

                    conn.commit()

                    sql = f"SELECT * FROM yh.quiz_solving order by num desc limit 1"

                    cursor.execute(sql)

                    self.a = cursor.fetchall()

                    print(self.a, 'self.a 확인')

                    # self.quiz_solving = cursor.fetchall()

                    conn.close()


                elif self.incoming_message[-1] == 'quiz_2':

                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',

                                      db='yh',

                                      charset='utf8')

                    cursor = conn.cursor()

                    sql = f"SELECT * FROM yh.quiz where number = '{self.incoming_message[0]}';"

                    print(sql)

                    cursor.execute(sql)  # 문제번호로 quiz테이블 조회

                    sol_check_row = cursor.fetchall()

                    if sol_check_row[0][3] == self.incoming_message[
                        3]:  ##quiz테이블의 solution 값과 클라이언트에서 제출클릭하여 전송한 o,x의 값이 같으면

                        cursor.execute(
                            f"INSERT INTO yh.quiz_solving (name, quiz, answer, quiz_num, checkci, count_time) VALUES ('{self.incoming_message[1]}','{self.incoming_message[2]}','{self.incoming_message[3]}',{sol_check_row[0][0]},'correct','{self.incoming_message[4]}')")

                    else:  # 틀리면

                        cursor.execute(
                            f"INSERT INTO yh.quiz_solving (name, quiz, answer, quiz_num, checkci, count_time) VALUES ('{self.incoming_message[1]}','{self.incoming_message[2]}','{self.incoming_message[3]}',{sol_check_row[0][0]},'incorrect','{self.incoming_message[4]}')")

                    conn.commit()
                    sql = f"SELECT * FROM yh.quiz_solving order by num desc limit 1"

                    cursor.execute(sql)

                    self.a2 = cursor.fetchall()

                    # self.quiz_solving = cursor.fetchall()

                    conn.close()

                    print(self.a2, 'a2')



                elif self.incoming_message[-1] == 'quiz_3':

                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',

                                      db='yh',

                                      charset='utf8')

                    cursor = conn.cursor()

                    sql = f"SELECT * FROM yh.quiz where number = '{self.incoming_message[0]}';"

                    print(sql)

                    cursor.execute(sql)  # 문제번호로 quiz테이블 조회

                    sol_check_row = cursor.fetchall()

                    if sol_check_row[0][3] == self.incoming_message[
                        3]:  ##quiz테이블의 solution 값과 클라이언트에서 제출클릭하여 전송한 o,x의 값이 같으면

                        cursor.execute(
                            f"INSERT INTO yh.quiz_solving (name, quiz, answer, quiz_num, checkci, count_time) VALUES ('{self.incoming_message[1]}','{self.incoming_message[2]}','{self.incoming_message[3]}',{sol_check_row[0][0]},'correct','{self.incoming_message[4]}')")

                    else:  # 틀리면

                        cursor.execute(
                            f"INSERT INTO yh.quiz_solving (name, quiz, answer, quiz_num, checkci, count_time) VALUES ('{self.incoming_message[1]}','{self.incoming_message[2]}','{self.incoming_message[3]}',{sol_check_row[0][0]},'incorrect','{self.incoming_message[4]}')")

                    conn.commit()
                    sql = f"SELECT * FROM yh.quiz_solving order by num desc limit 1"

                    cursor.execute(sql)

                    self.a3 = cursor.fetchall()

                    print(self.a3, 'a3')

                    # self.quiz_solving = cursor.fetchall()

                    conn.close()


                elif self.incoming_message[-1] == 'quiz_4':

                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',

                                      db='yh',

                                      charset='utf8')

                    cursor = conn.cursor()

                    sql = f"SELECT * FROM yh.quiz where number = '{self.incoming_message[0]}';"

                    print(sql)

                    cursor.execute(sql)  # 문제번호로 quiz테이블 조회

                    sol_check_row = cursor.fetchall()

                    if sol_check_row[0][3] == self.incoming_message[
                        3]:  ##quiz테이블의 solution 값과 클라이언트에서 제출클릭하여 전송한 o,x의 값이 같으면

                        cursor.execute(
                            f"INSERT INTO yh.quiz_solving (name, quiz, answer, quiz_num, checkci, count_time) VALUES ('{self.incoming_message[1]}','{self.incoming_message[2]}','{self.incoming_message[3]}',{sol_check_row[0][0]},'correct','{self.incoming_message[4]}')")

                    else:  # 틀리면

                        cursor.execute(
                            f"INSERT INTO yh.quiz_solving (name, quiz, answer, quiz_num, checkci, count_time) VALUES ('{self.incoming_message[1]}','{self.incoming_message[2]}','{self.incoming_message[3]}',{sol_check_row[0][0]},'incorrect','{self.incoming_message[4]}')")

                    conn.commit()

                    # cursor.execute(sql)

                    # sql = f"SELECT * FROM yh.quiz_solving WHERE quiz  in (select quiz from yh.quiz) order by num desc limit 1"

                    sql = f"SELECT * FROM yh.quiz_solving order by num desc limit 1"

                    cursor.execute(sql)

                    self.a4 = cursor.fetchall()

                    print(self.a4, 'a4')

                    # self.quiz_solving = cursor.fetchall()

                    conn.close()
                elif self.incoming_message[-1] == '세이브':

                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh', charset='utf8')
                    cursor = conn.cursor()



                    # print(self.incoming_message)
                    sql = f"insert into yh.study_save (id, word, page) values ('{self.incoming_message[2]}', '{self.incoming_message[1]}', {self.incoming_message[0]}); "
                    cursor.execute(sql)
                    conn.commit()
                    conn.close()

                elif self.incoming_message[-1] == '로드':

                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh', charset='utf8')
                    cursor = conn.cursor()
                    cursor.execute(f"select * \
                                                   from yh.study_save \
                                                   where id = '{self.incoming_message[0]}';")  # 입력한id와 같은것을 조회
                    rows = cursor.fetchall()

                    # print(rows[0])

                    conn.close()

                    rows_string = json.dumps(rows , ensure_ascii=False )
                    # c_socket.sendall(rows.encode())  # 클라이언트에 전송
                    c_socket.sendall((rows_string + ':로드').encode())

                elif self.incoming_message[-1] == 'score_page':

                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh', charset='utf8')
                    cursor = conn.cursor()
                    print(self.incoming_message)
                    cursor.execute(f"select count(num) \
                                                   from yh.quiz_solving \
                                                   where name = '{self.incoming_message[0]}' and checkci = 'correct';")  # id로 맞춘문제가 몇개인지 표시



                    rows = cursor.fetchall()
                    print(rows)
                    # print(rows[])
                    # print(rows[0])

                    conn.close()

                    rows_string = json.dumps(rows , ensure_ascii=False )
                    # c_socket.sendall(rows.encode())  # 클라이언트에 전송
                    c_socket.sendall((rows_string + '스코어').encode())

                elif self.incoming_message[-1] == '100':  # 상담
                    now = datetime.now()
                    self.now_time = now.strftime('%Y-%m-%d %H:%M:%S')
                    teacher = self.incoming_message[0]
                    message = self.incoming_message[1]
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789', db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    # DB에 데이터 저장
                    cursor.execute(
                        f"INSERT INTO yh.consult (name, content, time) VALUES('{teacher}','{message}','{self.now_time}')")
                    conn.commit()
                    conn.close()
                    self.final_received_message = (teacher + ':' + message + self.incoming_message[2] +  'consult')
                    self.send_all_clients(c_socket)

                elif self.incoming_message[-1] == '문제등록':
                    print(self.incoming_message, 2222233333)
                    kind = self.incoming_message[0]
                    quiz = self.incoming_message[1]
                    answer = self.incoming_message[2]
                    points = self.incoming_message[3]
                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789',
                                      db='yh', charset='utf8')
                    cursor = conn.cursor()
                    sql = f"INSERT INTO yh.quiz (kind, quiz, solution, points) VALUES ('{kind}','{quiz}','{answer}','{points}')"
                    cursor.execute(sql)
                    conn.commit()
                    sql = f"SELECT * FROM yh.quiz"
                    cursor.execute(sql)
                    self.update = cursor.fetchall()
                    print(self.update, 152555555)
                    quiz_update = json.dumps(self.update)
                    c_socket.sendall((quiz_update + '문제등록').encode())
                    conn.close()

                elif self.incoming_message[-1] == '접속자':
                    user = json.dumps(self.userlist)
                    c_socket.sendall((user + '접속자').encode())

                elif self.incoming_message[-1] == 'log_out':
                    # json.loads()
                    self.userlist.remove(self.incoming_message[0])
                    print(self.incoming_message[0], 174174174174174)

                elif self.incoming_message[-1] == '문제확인':  # 상담

                    conn = ms.connect(host='10.10.21.111', port=3306, user='beom', password='123456789', db='yh',
                                      charset='utf8')
                    cursor = conn.cursor()
                    # DB에 데이터 저장
                    cursor.execute(f"SELECT * FROM yh.quiz_solving")
                    solving_quiz_data = cursor.fetchall()
                    print(solving_quiz_data)
                    conn.commit()
                    conn.close()

                    # c_socket.sendall((solving_quiz_data + '문제확인').encode())

                    solving_quiz_data2 = json.dumps(solving_quiz_data) + "문제확인"
                    c_socket.send(solving_quiz_data2.encode())
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