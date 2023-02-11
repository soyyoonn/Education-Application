import pymysql
import sys

import timer as timer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import *
from socket import *
from threading import *
import json
import requests
import xmltodict
from datetime import datetime, timedelta
from timeit import default_timer as timer
from datetime import timedelta

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

        ####이범규
        self.btn_go_contents.clicked.connect(self.contents)  # 학습버튼 클릭시 컨텐츠 함수
        self.btn_search_contents.clicked.connect(self.search_contents)
        self.table_contents.cellClicked.connect(self.detail_contents)  # 학습컨텐츠 테이블의 셀을 클릭했을때 함수연결
        self.btn_search_page_up.clicked.connect(self.search_pageup)
        self.btn_search_page_down.clicked.connect(self.search_pagedown)
        self.btn_study_save.clicked.connect(self.study_save)  # 학습 저장
        self.btn_study_load.clicked.connect(self.study_load)  # 학슴 불러오기
        ####이범규

        self.score_btn.clicked.connect(self.score_page1)
        self.quiz_btn.clicked.connect(self.quiz_page1)
        self.timestart_1.clicked.connect(self.start_time)
        self.submit_1.clicked.connect(self.end_time)
        self.timestart_2.clicked.connect(self.start_time2)
        self.submit_2.clicked.connect(self.end_time2)
        self.timestart_3.clicked.connect(self.start_time3)
        self.submit_3.clicked.connect(self.end_time3)
        self.timestart_4.clicked.connect(self.start_time4)
        self.submit_4.clicked.connect(self.end_time4)
        self.next_btn.clicked.connect(self.next1)
        self.next_btn_2.clicked.connect(self.next2)
        self.next_btn_3.clicked.connect(self.next3)
        self.before_btn_2.clicked.connect(self.before1)
        self.before_btn_3.clicked.connect(self.before2)
        self.before_btn_4.clicked.connect(self.before3)

        self.key = "gV%2B27zS6BAEbMXogg3rkskTVPQNhXDS7TNrjbm8g2gjAdeJm4lfzO4xpmLt4xTgqrv3i8eUYDMvanmwmwiumKQ%3D%3D"  # 인증키저장



    def start_time(self):
        self.start = timer()
        print('시작시간', self.start)
        self.timestart_1.setEnabled(False)

    def closeEvent(self, event):
        # QMessageBox.information(self,'알림','fh')
        msg = [self.log, 'log_out']
        print(msg, '메시지')
        self.client_socket.send(json.dumps(msg).encode())

    def study_load(self):  # 로그인한 학생의 id를 서버로 전송하는 함수
        load_file = [self.id, '로드']
        load_string = json.dumps(load_file, ensure_ascii=False)
        self.client_socket.send(load_string.encode())
        print('되니')

        # self.receive_load(self.client_socket, )

    def study_save(self):  ##학습중 검색단어, 페이지를 서버로 전송하여 저장하는 함수
        # qna = (self.id + ":" + self.pw + 'QnA').encode()
        # save_file = (str(self.search_result_page) + '세이브').encode()
        save_file = [self.search_result_page, self.search_word, self.id, "세이브"]
        save_string = json.dumps(save_file, ensure_ascii=False)
        self.client_socket.send(save_string.encode())

    def search_pagedown(self):  # 다음페이지 버튼
        if self.search_result_page > 1:
            self.table_contents.clearContents()
            self.search_result_page -= 1
            url = f"http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctIlstrSearch?serviceKey={self.key}&st=1&sw={self.search_word}&numOfRows=10&pageNo={self.search_result_page}"

            content = requests.get(url).content  # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
            dict = xmltodict.parse(content)  # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
            jsonString = json.dumps(dict, ensure_ascii=False)  # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
            jsonObj = json.loads(jsonString)  # 데이터 불러올 때(딕셔너리 형태로 받아옴)
            search_result_toatal_count = jsonObj['response']['body']['totalCount']

            print(search_result_toatal_count)

            i = 0
            for item in jsonObj['response']['body']['items']['item']:
                # print(item)
                print(item['insctOfnmKrlngNm'])
                print(item['familyKorNm'], item['insctOfnmKrlngNm'], item['ordKorNm'], item['insctPilbkNo'])
                self.table_contents.setItem(i, 0, QTableWidgetItem(item['familyKorNm']))
                self.table_contents.setItem(i, 1, QTableWidgetItem(item['insctOfnmKrlngNm']))
                self.table_contents.setItem(i, 2, QTableWidgetItem(item['ordKorNm']))
                self.table_contents.setItem(i, 3, QTableWidgetItem(item['insctPilbkNo']))

                i += 1
            self.label_page.setText(f"{self.search_result_page}")
        else:
            QMessageBox.information(self, 'Information Title', '첫 페이지 입니다')

    def search_pageup(self):  # 이전페이지 버튼
        try:
            self.search_result_page += 1
            url = f"http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctIlstrSearch?serviceKey={self.key}&st=1&sw={self.search_word}&numOfRows=10&pageNo={self.search_result_page}"

            content = requests.get(url).content  # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
            dict = xmltodict.parse(content)  # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
            jsonString = json.dumps(dict, ensure_ascii=False)  # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
            jsonObj = json.loads(jsonString)  # 데이터 불러올 때(딕셔너리 형태로 받아옴)
            search_result_toatal_count = jsonObj['response']['body']['totalCount']

            print(search_result_toatal_count)

            i = 0
            self.table_contents.clearContents()
            for item in jsonObj['response']['body']['items']['item']:
                # print(item)
                print(item['insctOfnmKrlngNm'])
                print(item['familyKorNm'], item['insctOfnmKrlngNm'], item['ordKorNm'], item['insctPilbkNo'])
                self.table_contents.setItem(i, 0, QTableWidgetItem(item['familyKorNm']))
                self.table_contents.setItem(i, 1, QTableWidgetItem(item['insctOfnmKrlngNm']))
                self.table_contents.setItem(i, 2, QTableWidgetItem(item['ordKorNm']))
                self.table_contents.setItem(i, 3, QTableWidgetItem(item['insctPilbkNo']))

                i += 1
            self.label_page.setText(f"{self.search_result_page}")
        except:
            QMessageBox.information(self, 'Information Title', '마지막 페이지 입니다.')

    def detail_contents(self):  # 테이블위젯 행 클릭했을때 상세정보에 텍스트 입력
        # self.tb_detail_contents
        self.currow = self.table_contents.currentRow()
        self.curcol = self.table_contents.currentColumn()
        print(self.currow)
        # self.order_prod_name = self.table_order_management.item(self.a, 2)

        self.dic_num = self.table_contents.item(self.currow, 3)  # 클릭한 행의 사전번호
        # print(self.dic_num)
        # self.order_status = self.table_order_management.item(self.a, 5)

        url = f"http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctIlstrInfo?serviceKey={self.key}&q1={self.dic_num.text()}"

        content = requests.get(url).content  # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
        dict = xmltodict.parse(content)  # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
        jsonString = json.dumps(dict, ensure_ascii=False)  # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
        jsonObj = json.loads(jsonString)  # 데이터 불러올 때(딕셔너리 형태로 받아옴)
        print(jsonObj['response']['body']['item']['cont1'])
        self.tb_detail_contents.setText(jsonObj['response']['body']['item']['cont1'])
        # for item in jsonObj['response']['body']['item']['cont1']:
        #     print(item)

    def search_contents(self):  # 학습 컨텐츠 검색

        # 인증키 정보가 들어간 url 저장
        # url = f'http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctPrtctList?serviceKey=%7Bkey%7D'
        self.search_word = self.lineedit_search_contents.text()
        self.search_result_page = 1
        url = f"http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctIlstrSearch?serviceKey={self.key}&st=1&sw={self.search_word}&numOfRows=10&pageNo={self.search_result_page}"

        content = requests.get(url).content  # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
        dict = xmltodict.parse(content)  # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
        jsonString = json.dumps(dict, ensure_ascii=False)  # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
        jsonObj = json.loads(jsonString)  # 데이터 불러올 때(딕셔너리 형태로 받아옴)

        search_result_toatal_count = jsonObj['response']['body']['totalCount']

        print(search_result_toatal_count)
        self.table_contents.clearContents()
        i = 0
        for item in jsonObj['response']['body']['items']['item']:
            # print(item)
            print(item['insctOfnmKrlngNm'])
            print(item['familyKorNm'], item['insctOfnmKrlngNm'], item['ordKorNm'], item['insctPilbkNo'])
            self.table_contents.setItem(i, 0, QTableWidgetItem(item['familyKorNm']))
            self.table_contents.setItem(i, 1, QTableWidgetItem(item['insctOfnmKrlngNm']))
            self.table_contents.setItem(i, 2, QTableWidgetItem(item['ordKorNm']))
            self.table_contents.setItem(i, 3, QTableWidgetItem(item['insctPilbkNo']))

            i += 1
        # self.label_page.setText(f"{self.search_result_page}")
        self.label_page.setText(f"{self.search_result_page}")

    def contents(self):
        self.stackedWidget_2.setCurrentWidget(self.page_contents)

    def next1(self):
        self.stackedWidget_2.setCurrentIndex(2)

    def next2(self):
        self.stackedWidget_2.setCurrentIndex(3)

    def next3(self):
        self.stackedWidget_2.setCurrentIndex(4)

    def before1(self):
        self.stackedWidget_2.setCurrentIndex(1)

    def before2(self):
        self.stackedWidget_2.setCurrentIndex(2)

    def before3(self):
        self.stackedWidget_2.setCurrentIndex(3)

    def start_time(self):
        self.start = timer()
        print('시작시간', self.start)
        self.timestart_1.setEnabled(False)

    def end_time(self):
        self.time_list = []
        end = timer()
        print('종료시간', end)
        t_time = timedelta(seconds=end - self.start)
        print(t_time, '시간차 계산')
        a = str(t_time).split(':')
        print(a[2][:2])
        print(self.quiz1)
        self.time_list.append(self.quiz1[0])
        self.time_list.append(self.id)  # 아이디
        self.time_list.append(self.quiz1[2])  # 문제 내용
        if self.correct_o_1.isChecked() == True:
            self.b = self.correct_o_1.text()  # 답 체크 o
            self.time_list.append(self.b)
        elif self.correct_x_1.isChecked() == True:
            self.c = self.correct_x_1.text()  # 답 체크 x
            self.time_list.append(self.c)
        self.time_list.append(a[2][:2])  # 시간차 계산
        self.qu = 'quiz_1'
        self.time_list.append(self.qu)
        self.submit_1.setEnabled(False)
        quiz_1 = self.time_list
        print(quiz_1, '94 확인')
        json.dumps(quiz_1)
        self.client_socket.send(json.dumps(quiz_1).encode())

    def start_time2(self):
        self.start = timer()
        print('시작시간', self.start)
        self.timestart_2.setEnabled(False)

    def end_time2(self):
        self.time_list = []
        end = timer()
        print('종료시간', end)
        t_time = timedelta(seconds=end - self.start)
        print(t_time, '시간차 계산')
        a = str(t_time).split(':')
        print(a[2][:2])
        self.time_list.append(self.quiz2[0])
        self.time_list.append(self.id)  # 아이디
        self.time_list.append(self.quiz2[2])  # 문제 내용
        if self.correct_o_2.isChecked() == True:
            self.b = self.correct_o_2.text()  # 답 체크 o
            self.time_list.append(self.b)
        elif self.correct_x_2.isChecked() == True:
            self.c = self.correct_x_2.text()  # 답 체크 x
            self.time_list.append(self.c)
        self.time_list.append(a[2][:2])  # 시간차 계산
        self.qu = 'quiz_2'
        self.time_list.append(self.qu)
        self.submit_2.setEnabled(False)
        quiz_2 = self.time_list
        print(quiz_2, '2번 확인')
        json.dumps(quiz_2)
        self.client_socket.send(json.dumps(quiz_2).encode())

    def start_time3(self):
        self.start = timer()
        print('시작시간', self.start)
        self.timestart_3.setEnabled(False)

    def end_time3(self):
        self.time_list = []
        end = timer()
        print('종료시간', end)
        t_time = timedelta(seconds=end - self.start)
        print(t_time, '시간차 계산')
        a = str(t_time).split(':')
        print(a[2][:2])
        self.time_list.append(self.quiz3[0])
        self.time_list.append(self.id)  # 아이디
        self.time_list.append(self.quiz2[2])  # 문제 내용
        if self.correct_o_3.isChecked() == True:
            self.b = self.correct_o_3.text()  # 답 체크 o
            self.time_list.append(self.b)
        elif self.correct_x_3.isChecked() == True:
            self.c = self.correct_x_3.text()  # 답 체크 x
            self.time_list.append(self.c)
        self.time_list.append(a[2][:2])  # 시간차 계산
        self.qu = 'quiz_3'
        self.time_list.append(self.qu)
        self.submit_3.setEnabled(False)
        quiz_3 = self.time_list
        print(quiz_3, '3번 확인')
        json.dumps(quiz_3)
        self.client_socket.send(json.dumps(quiz_3).encode())

    def start_time4(self):
        self.start = timer()
        print('시작시간', self.start)
        self.timestart_4.setEnabled(False)

    def end_time4(self):
        self.time_list = []
        end = timer()
        print('종료시간', end)
        t_time = timedelta(seconds=end - self.start)
        print(t_time, '시간차 계산')
        a = str(t_time).split(':')
        print(a[2][:2])
        self.time_list.append(self.quiz4[0])
        self.time_list.append(self.id)  # 아이디
        self.time_list.append(self.quiz2[2])  # 문제 내용
        if self.correct_o_4.isChecked() == True:
            self.b = self.correct_o_4.text()  # 답 체크 o
            self.time_list.append(self.b)
        elif self.correct_x_4.isChecked() == True:
            self.c = self.correct_x_4.text()  # 답 체크 x
            self.time_list.append(self.c)
        self.time_list.append(a[2][:2])  # 시간차 계산
        self.qu = 'quiz_4'
        self.time_list.append(self.qu)
        self.submit_4.setEnabled(False)
        quiz_4 = self.time_list
        print(quiz_4, '4번 확인')
        json.dumps(quiz_4)
        self.client_socket.send(json.dumps(quiz_4).encode())

    def quiz_page1(self):
        quiz_page = [self.id, 'quiz_page']
        json.dumps(quiz_page)
        self.client_socket.send(json.dumps(quiz_page).encode())
        self.stackedWidget_2.setCurrentIndex(1)
        self.quiz_btn.setEnabled(False)

    def score_page1(self):
        self.stackedWidget_2.setCurrentIndex(5)

        self.label_name.setText(f"{self.log}")
        score_page = [self.id, 'score_page']
        json.dumps(score_page)
        self.client_socket.send(json.dumps(score_page).encode())

    def Consult(self):
        self.consult = self.consult_send.text()
        consultor = [self.log, self.consult, 'consult']
        json.dumps(consultor).encode()
        self.client_socket.send(json.dumps(consultor).encode())
        self.consult_send.clear()

    def Consult_page(self):
        # consult_page = ['consult_page']
        # json.dumps(consult_page)
        # self.client_socket.send(json.dumps(consult_page).encode())
        self.stackedWidget_2.setCurrentIndex(7)

    def QnA_page(self):
        qna_page = ['QnA_page']
        json.dumps(qna_page)
        self.client_socket.send(json.dumps(qna_page).encode())
        self.stackedWidget_2.setCurrentIndex(6)

    def QnA(self):
        self.qna = self.qna_send.text()
        print(self.qna, 34)
        # qna = (self.log + ":" + self.qna + ":" + 'QnA').encode()
        qna = [self.log, self.qna, 'QnA']
        json.dumps(qna)
        self.client_socket.send(json.dumps(qna).encode())
        # qna.append(self.log)
        # print(qna.decode(),36)

    def login_page(self):
        self.stackedWidget.setCurrentIndex(0)
        self.login_btn.setText("로그아웃")

    def join_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def Login(self):
        self.id = self.log_id.text()
        self.pw = self.log_pw.text()
        id = [self.id, self.pw, '로그인']
        id_string = json.dumps(id).encode()
        self.client_socket.send(id_string)
        self.receive_log(self.client_socket, )

    # def receive_load(self, so):
    #
    #     buf = so.recv(9999).decode()
    #     print('sibal')
    #     a = json.loads(buf)
    #     print(1234)
    #     print(a)

    def receive_log(self, so):
        buf = so.recv(8192).decode()
        print(buf)
        if not buf:
            pass
        if buf[-3:] == '로그인':
            self.log = buf[:-3]
            QMessageBox.information(self, "로그인", f"{self.log}님 로그인 하셨습니다.")
            self.stackedWidget.setCurrentIndex(1)
            self.log_name.setText(f"{self.log}님 반갑습니다.")



        elif buf == '오류':
            log = buf
            QMessageBox.critical(self, "오류", f"정보가 일치하지 않습니다.")

    def receive_message(self, so):
        while True:
            buf = so.recv(9999).decode()
            # print(buf,"확인")
            # print(type(buf))

            # a = json.loads(buf.decode())
            if not buf:
                break

            ###임영효### 시작
            if buf[-12:] == 'consult_page':
                self.consult_page = buf
                self.con = json.loads(self.consult_page[:-12])
                print(self.con, 236)
                # if self.log in
                for i in range(len(self.con)):
                    self.consultWidget.addItem(self.con[i][1] + ':' + self.con[i][2])
            # elif msg[-7:] == 'consult':
            #     print(msg, 5748956)
            #     msg = msg[:-7]
            #     if self.namebox.currentText() in msg:
            #         self.chatlist.addItem(msg)  # 채팅창에 메시지 추가
            #     elif '교사' in msg:
            #         self.chatlist.addItem(msg)
            #     self.chatlist.scrollToBottom()
            if buf[-2:] == "포트":
                print("왔따")
                print(buf[:-2])
                self.sibal_port = buf[:-2]

            if buf[-10:] == 'quiz_page1':
                self.quiz_page = buf
                self.quiz1 = json.loads(self.quiz_page[:-10])
                self.quiz_contents.clear()
                self.quiz_contents.addItem(self.quiz1[2])
                print(272)

            if buf[-10:] == 'quiz_page2':
                self.quiz_page = buf
                self.quiz2 = json.loads(self.quiz_page[:-10])
                self.quiz_contents_2.clear()
                self.quiz_contents_2.addItem(self.quiz2[2])
                print(278)
            if buf[-10:] == 'quiz_page3':
                self.quiz_page = buf
                self.quiz3 = json.loads(self.quiz_page[:-10])
                self.quiz_contents_3.clear()
                self.quiz_contents_3.addItem(self.quiz3[2])
                print(284)
            if buf[-10:] == 'quiz_page4':
                self.quiz_page = buf
                self.quiz4 = json.loads(self.quiz_page[:-10])
                self.quiz_contents_4.clear()
                self.quiz_contents_4.addItem(self.quiz4[2])
                print(290)

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
                print("확인했어요")


                print(buf)
                print(buf[-10:-7])
                print(buf[0:2])
                self.cons = buf[:-7]
                print(self.cons)
                if buf[-10:-7] == self.log and buf[0:2] == "교사":
                    self.consultWidget.addItem(str(buf[:-10]))
                elif buf[0:3] == self.log :
                    self.consultWidget.addItem(str(self.cons))
                self.consultWidget.scrollToBottom()

                # elif msg[-7:] == 'consult':
                #     print(msg,5748956)
                #     msg = msg[:-7]
                #     if self.namebox.currentText() in msg:
                #         self.chatlist.addItem(msg)  # 채팅창에 메시지 추가
                #     elif '교사' in msg:
                #         self.chatlist.addItem(msg)
                #     self.chatlist.scrollToBottom()

                ###임영효#### 끝

                ###이범규### 시작
            if buf[-3:] == ':로드':
                a = buf
                self.load_data = json.loads(a[:-3])

                url = f"http://openapi.nature.go.kr/openapi/service/rest/InsectService/isctIlstrSearch?serviceKey={self.key}&st=1&sw={self.load_data[0][2]}&numOfRows=10&pageNo={int(self.load_data[0][3])}"

                content = requests.get(url).content  # request 모듈을 이용해서 정보 가져오기(byte형태로 가져와지는듯)
                dict = xmltodict.parse(content)  # xmltodict 모듈을 이용해서 딕셔너리화 & 한글화
                jsonString = json.dumps(dict, ensure_ascii=False)  # json.dumps를 이용해서 문자열화(데이터를 보낼때 이렇게 바꿔주면 될듯)
                jsonObj = json.loads(jsonString)  # 데이터 불러올 때(딕셔너리 형태로 받아옴)

                search_result_toatal_count = jsonObj['response']['body']['totalCount']

                print(search_result_toatal_count)
                self.table_contents.clearContents()
                i = 0
                for item in jsonObj['response']['body']['items']['item']:
                    # print(item)
                    print(item['insctOfnmKrlngNm'])
                    print(item['familyKorNm'], item['insctOfnmKrlngNm'], item['ordKorNm'], item['insctPilbkNo'])
                    self.table_contents.setItem(i, 0, QTableWidgetItem(item['familyKorNm']))
                    self.table_contents.setItem(i, 1, QTableWidgetItem(item['insctOfnmKrlngNm']))
                    self.table_contents.setItem(i, 2, QTableWidgetItem(item['ordKorNm']))
                    self.table_contents.setItem(i, 3, QTableWidgetItem(item['insctPilbkNo']))

                    i += 1
                self.label_page.setText(f"{self.load_data[0][3]}")
                self.search_result_page = int(self.load_data[0][3])
                self.search_word = self.load_data[0][2]

            if buf[-3:] == '스코어':
                a = buf
                score_date = json.loads(a[:-3])
                self.label_score.setText(str(int(score_date[0][0] * 25)))

            # elif buf[-3:] == ':로드':
            #     self.quiz_page = buf
            #     self.quiz1 = json.loads(self.quiz_page[:-10])
            #     self.quiz_contents_4.clear()
            #     self.quiz_contents_4.addItem(self.quiz1[2])
            #     print(290)

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
    ip = '10.10.21.111'
    port = 9999
    app = QApplication(sys.argv)
    mainWindow = Student(ip, port)
    app.exec_()