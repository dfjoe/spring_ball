import sys
import time
import math
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

'''
코드 실행하실때 csv 파일 주소 변경하셔야 프로그램이 정상적으로 작동합니다.
10,112번에 'score.scv'파일 주소
24번에 'ProjectileMotion.csv'파일 주소를 입력하셔야 합니다.
'''

#스코어 이름 저장
def save_csv_score(_listname, _listscore):
    outfp = open("D:/ICT/최종/score.csv", "w")

    temp = "등수, 이름, 점수" + ", \n"
    outfp.writelines(temp)

    for i in range(len(_listname)):
        t = (i * 1) + 1
        temp = str(t) + "," + str(_listname[i]) + "," + str(_listscore[i]) + "\n"
        outfp.writelines(temp)

    outfp.close()

#이동경로 저장
def save_csv(_listX, _listY):
    outfp = open("D:/ICT/최종/ProjectileMotion.csv", "w")

    temp = "시간, x좌표, y좌표\n"
    outfp.writelines(temp)

    for i in range(len(_listX)):
        t = i * 0.05
        temp = str(t) + "," + str(_listX[i]) + "," + str(_listY[i]) + "\n"
        outfp.writelines(temp)

    outfp.close()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self._x = 200
        self._y = 75
        self.velocity = 0
        self.mass = 0
        self.modulus = 0
        self.list_x = []
        self.list_y = []
        self.listname = []
        self.listscore = []

    # 창 중앙정렬
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 배치
    def setupUI(self):
        self.setGeometry(100, 50, 1500, 900)
        self.setWindowTitle("Ball Survival Game v0.1")
        self.setFixedSize(1500, 1000)
        self.center()

        self.statusBar().showMessage("변수를 입력 후 게임을 시작하세요.")

        # 상단 메뉴
        menu = self.menuBar()
        menu_file = menu.addMenu("File")

        file_exit = QAction("Exit", self)
        file_exit.setShortcut("ctrl+E")
        file_exit.setStatusTip("end")

        file_exit.triggered.connect(QCoreApplication.instance().quit)

        menu_file.addAction(file_exit)

        self.lbl_img = QLabel("image", self)
        self.lbl_img.move(50, 50)
        self.pixmap = QPixmap("spring1.jpg")
        self.pixmap = self.pixmap.scaledToWidth(150)
        self.lbl_img.setPixmap(self.pixmap)
        self.lbl_img.setFixedSize(self.pixmap.size())

        pixmap = QPixmap("")
        pixmap = pixmap.scaledToHeight(500)
        _img = QLabel()
        _img.setPixmap(pixmap)

        self.rule = QLabel("RULE", self)
        self.rule.move(1070, 80)
        self.rule.resize(500, 100)
        font = self.rule.font()
        font.setPointSize(25)
        self.rule.setFont(font)

        self.rule1 = QLabel("최대 탄성계수 : 100000", self)
        self.rule1.move(1030, 160)
        self.rule1.resize(500, 40)

        self.rule2 = QLabel("최대 수축률 : 100", self)
        self.rule2.move(1030, 200)
        self.rule2.resize(500, 40)

        self.rule2 = QLabel("공의 최소 무게 : 5", self)
        self.rule2.move(1030, 240)
        self.rule2.resize(500, 40)

        # 스코어 저장 scv
        infp = open("D:/ICT/최종/score.csv", "r")

        listnum = []
        listname = []
        listscore = []

        instr = infp.read()
        infp.close()

        instrlist = instr.splitlines()
        del instrlist[0]

        for str in instrlist:
            strlist = str.split(",")
            listnum.append(strlist[0])
            listname.append(strlist[1])
            listscore.append(strlist[2])

        self.score = QLabel("Score", self)
        self.score.move(1070, 350)
        self.score.resize(500, 100)
        font = self.score.font()
        font.setPointSize(30)
        self.score.setFont(font)

        self.num1 = QLabel(listnum[0], self)
        self.num1.move(970, 440)
        self.num2 = QLabel(listnum[1], self)
        self.num2.move(970, 480)
        self.num3 = QLabel(listnum[2], self)
        self.num3.move(970, 520)
        self.num4 = QLabel(listnum[3], self)
        self.num4.move(970, 560)
        self.num5 = QLabel(listnum[4], self)
        self.num5.move(970, 600)

        self.name1 = QLabel(listname[0], self)
        self.name1.move(1100, 440)
        self.name2 = QLabel(listname[1], self)
        self.name2.move(1100, 480)
        self.name3 = QLabel(listname[2], self)
        self.name3.move(1100, 520)
        self.name4 = QLabel(listname[3], self)
        self.name4.move(1100, 560)
        self.name5 = QLabel(listname[4], self)
        self.name5.move(1100, 600)

        self.score1 = QLabel(listscore[0], self)
        self.score1.move(1250, 440)
        self.score2 = QLabel(listscore[1], self)
        self.score2.move(1250, 480)
        self.score3 = QLabel(listscore[2], self)
        self.score3.move(1250, 520)
        self.score4 = QLabel(listscore[3], self)
        self.score4.move(1250, 560)
        self.score5 = QLabel(listscore[4], self)
        self.score5.move(1250, 600)

        self.label_name = QLabel("이름", self)
        self.lineEdit_name = QLineEdit(self)
        self.label_name.move(900, 710)
        self.lineEdit_name.move(980, 710)
        self.lineEdit_name.resize(300, 30)

        self.label_modulus = QLabel("탄성계수", self)
        self.lineEdit_modulus = QLineEdit("90000", self)
        self.label_modulus.move(900, 750)
        self.lineEdit_modulus.move(980, 750)
        self.lineEdit_modulus.resize(300, 30)

        self.label_shrinkage = QLabel("수축률", self)
        self.lineEdit_shrinkage = QLineEdit("20", self)
        self.label_shrinkage.move(900, 790)
        self.lineEdit_shrinkage.move(980, 790)
        self.lineEdit_shrinkage.resize(300, 30)

        self.label_mass = QLabel("무게", self)
        self.lineEdit_mass = QLineEdit("5", self)
        self.label_mass.move(900, 830)
        self.lineEdit_mass.move(980, 830)
        self.lineEdit_mass.resize(300, 30)

        self.shrinkButton = QPushButton("준비", self)
        self.shrinkButton.clicked.connect(self.shrinkedButtonClicked)
        self.shrinkButton.move(900, 880)
        self.shrinkButton.resize(170, 40)

        self.pushButton = QPushButton("발사", self)
        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.pushButton.move(1080, 880)
        self.pushButton.resize(170, 40)

        self.saveButton = QPushButton("저장", self)
        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.saveButton.move(1260, 880)
        self.saveButton.resize(170, 40)

    # 준비 버튼
    def shrinkedButtonClicked(self):
        self.shrinkage = int(self.lineEdit_shrinkage.text())
        self.shrinkage_s = int(150 * (self.shrinkage / 100))

        if (0 < self.shrinkage <= 10):
            self.pixmap = QPixmap("810.jpg")
            self.pixmap = self.pixmap.scaledToWidth(135)
            self.lbl_img.setPixmap(self.pixmap)
            self.lbl_img.setFixedSize(self.pixmap.size())

        elif (10 < self.shrinkage <= 20):
            self.pixmap = QPixmap("720.jpg")
            self.pixmap = self.pixmap.scaledToWidth(120)
            self.lbl_img.setPixmap(self.pixmap)
            self.lbl_img.setFixedSize(self.pixmap.size())

        elif (20 < self.shrinkage <= 30):
            self.pixmap = QPixmap("630.jpg")
            self.pixmap = self.pixmap.scaledToWidth(105)
            self.lbl_img.setPixmap(self.pixmap)
            self.lbl_img.setFixedSize(self.pixmap.size())

        elif (30 < self.shrinkage <= 40):
            self.pixmap = QPixmap("540.jpg")
            self.pixmap = self.pixmap.scaledToWidth(90)
            self.lbl_img.setPixmap(self.pixmap)
            self.lbl_img.setFixedSize(self.pixmap.size())

        elif (40 < self.shrinkage <= 50):
            self.pixmap = QPixmap("450.jpg")
            self.pixmap = self.pixmap.scaledToWidth(75)
            self.lbl_img.setPixmap(self.pixmap)
            self.lbl_img.setFixedSize(self.pixmap.size())

        elif (50 < self.shrinkage <= 60):
            self.pixmap = QPixmap("360.jpg")
            self.pixmap = self.pixmap.scaledToWidth(60)
            self.lbl_img.setPixmap(self.pixmap)
            self.lbl_img.setFixedSize(self.pixmap.size())

        elif (60 < self.shrinkage <= 70):
            self.pixmap = QPixmap("270.jpg")
            self.pixmap = self.pixmap.scaledToWidth(45)
            self.lbl_img.setPixmap(self.pixmap)
            self.lbl_img.setFixedSize(self.pixmap.size())

        elif (70 < self.shrinkage <= 80):
            self.pixmap = QPixmap("180.jpg")
            self.pixmap = self.pixmap.scaledToWidth(30)
            self.lbl_img.setPixmap(self.pixmap)
            self.lbl_img.setFixedSize(self.pixmap.size())

        elif (80 < self.shrinkage <= 90):
            self.pixmap = QPixmap("90.jpg")
            self.pixmap = self.pixmap.scaledToWidth(15)
            self.lbl_img.setPixmap(self.pixmap)
            self.lbl_img.setFixedSize(self.pixmap.size())

        elif (90 < self.shrinkage <= 100):
            self.pixmap = QPixmap("90.jpg")
            self.pixmap = self.pixmap.scaledToWidth(0)
            self.lbl_img.setPixmap(self.pixmap)
            self.lbl_img.setFixedSize(self.pixmap.size())

    # 발사 버튼
    def pushButtonClicked(self):
        # 변수 입력
        self.modulus = float(self.lineEdit_modulus.text())
        self.shrinkage = float(self.lineEdit_shrinkage.text())
        self.mass = float(self.lineEdit_mass.text())

        # 속도 계산
        self.shrinkage_a = self.shrinkage / 100
        velocity = int(math.sqrt((self.modulus * (self.shrinkage_a * self.shrinkage_a)) / self.mass))

        # 스프링 크기 복구
        self.pixmap = QPixmap("spring1.jpg")
        self.pixmap = self.pixmap.scaledToWidth(150)
        self.lbl_img.setPixmap(self.pixmap)
        self.lbl_img.setFixedSize(self.pixmap.size())

        self.list_x = []
        self.list_y = []

        self.name = self.lineEdit_name.text()
        self.listname.append(self.name)

        self.statusBar().showMessage("")

        # 초기값
        x0 = 200
        y0 = 75
        v0_x = velocity
        v0_y = 0

        # 시작
        i = 0
        while True:
            if self.shrinkage > 100:
                break
            if self.modulus > 100000:
                break
            if self.mass < 5:
                break

            i += 1
            t = i * 0.05
            x = x0 + (v0_x * t)
            y = y0 - (v0_y * t) + (0.5 * 9.81 * t * t)

            self.list_x.append(x)
            self.list_y.append(y)
            self._x = x
            self._y = y
            QWidget.repaint(self)
            time.sleep(0.005)

            # 1번
            if (500 < self._x < 650) and (250 < self._y < 260):
                v0_y = (9.81 * t)
                i = 0
                while True:
                    i += 1
                    t = i * 0.05
                    x_1 = x + (v0_x * t)
                    y_1 = y - (0.7 * v0_y * t) + (0.5 * 9.81 * t * t)

                    self.list_x.append(x_1)
                    self.list_y.append(y_1)
                    self._x = x_1
                    self._y = y_1
                    QWidget.repaint(self)
                    time.sleep(0.005)

                    # 오른쪽 벽
                    if self._x > 800:
                        v0_y = (9.81 * t) - 0.7 * v0_y
                        i = 0
                        while True:
                            i += 1
                            t = i * 0.05
                            x_2 = x_1 - (v0_x * t)
                            y_2 = y_1 + (v0_y * t) + (0.5 * 9.81 * t * t)

                            self.list_x.append(x_2)
                            self.list_y.append(y_2)
                            self._x = x_2
                            self._y = y_2
                            QWidget.repaint(self)
                            time.sleep(0.005)

                            # 1번
                            if (500 < self._x < 650) and (250 < self._y < 260):
                                v0_y = (9.81 * t) - v0_y
                                i = 0
                                while True:
                                    i += 1
                                    t = i * 0.05
                                    x_3 = x_2 - (v0_x * t)
                                    y_3 = y_2 - (0.7 * v0_y * t) + (0.5 * 9.81 * t * t)

                                    self.list_x.append(x_3)
                                    self.list_y.append(y_3)
                                    self._x = x_3
                                    self._y = y_3
                                    QWidget.repaint(self)
                                    time.sleep(0.005)

                                    # 왼쪽 벽
                                    if self._x < 200:
                                        v0_y = (9.81 * t) - 0.7 * v0_y
                                        i = 0
                                        while True:
                                            i += 1
                                            t = i * 0.05
                                            x_4 = x_3 + (v0_x * t)
                                            y_4 = y_3 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                            self.list_x.append(x_4)
                                            self.list_y.append(y_4)
                                            self._x = x_4
                                            self._y = y_4
                                            QWidget.repaint(self)
                                            time.sleep(0.005)

                                            # 오른쪽 아래 블랙홀
                                            if (798 < self._x < 803) and (730 < self._y < 800):
                                                break

                                            # 2번
                                            if (300 < self._x < 480) and (424 < self._y < 428):
                                                v0_y = (9.81 * t) + v0_y
                                                i = 0
                                                while True:
                                                    i += 1
                                                    t = i * 0.05
                                                    x_5 = x_4 + (v0_x * t)
                                                    y_5 = y_4 - (0.7 * v0_y * t) + (0.5 * 9.81 * t * t)

                                                    self.list_x.append(x_5)
                                                    self.list_y.append(y_5)
                                                    self._x = x_5
                                                    self._y = y_5
                                                    QWidget.repaint(self)
                                                    time.sleep(0.005)

                                                    # 오른쪽 벽
                                                    if self._x > 800:
                                                        v0_y = (9.81 * t) - 0.7 * v0_y
                                                        i = 0
                                                        while True:
                                                            i += 1
                                                            t = i * 0.05
                                                            x_6 = x_5 - (v0_x * t)
                                                            y_6 = y_5 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                                            self.list_x.append(x_6)
                                                            self.list_y.append(y_6)
                                                            self._x = x_6
                                                            self._y = y_6
                                                            QWidget.repaint(self)
                                                            time.sleep(0.005)

                                                            if self._y > 900:
                                                                break

                                                    # 오른쪽 위 블랙홀
                                                    if (798 < self._x < 803) and (390 < self._y < 480):
                                                        break

                                                    if self._y > 900:
                                                        break

                                            # 3번
                                            if (550 < self._x < 700) and (625 < self._y < 630):
                                                v0_y = (9.81 * t) - v0_y
                                                i = 0
                                                while True:
                                                    i += 1
                                                    t = i * 0.05
                                                    x_5 = x_4 + (v0_x * t)
                                                    y_5 = y_4 - (0.7 * v0_y * t) + (0.5 * 9.81 * t * t)

                                                    self.list_x.append(x_5)
                                                    self.list_y.append(y_5)
                                                    self._x = x_5
                                                    self._y = y_5
                                                    QWidget.repaint(self)
                                                    time.sleep(0.005)

                                                    # 오른쪽 벽
                                                    if self._x > 800:
                                                        v0_y = (9.81 * t) - 0.7 * v0_y
                                                        i = 0
                                                        while True:
                                                            i += 1
                                                            t = i * 0.05
                                                            x_6 = x_5 - (v0_x * t)
                                                            y_6 = y_5 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                                            self.list_x.append(x_6)
                                                            self.list_y.append(y_6)
                                                            self._x = x_6
                                                            self._y = y_6
                                                            QWidget.repaint(self)
                                                            time.sleep(0.005)

                                                            # 3번
                                                            if (550 < self._x < 700) and (625 < self._y < 630):
                                                                v0_y = (9.81 * t) - v0_y
                                                                i = 0
                                                                while True:
                                                                    i += 1
                                                                    t = i * 0.05
                                                                    x_7 = x_6 - (v0_x * t)
                                                                    y_7 = y_6 - (0.7 * v0_y * t) + (0.5 * 9.81 * t * t)

                                                                    self.list_x.append(x_7)
                                                                    self.list_y.append(y_7)
                                                                    self._x = x_7
                                                                    self._y = y_7
                                                                    QWidget.repaint(self)
                                                                    time.sleep(0.005)

                                                                    # 왼쪽 벽
                                                                    if self._x < 200:
                                                                        v0_y = (9.81 * t) - 0.7 * v0_y
                                                                        i = 0
                                                                        while True:
                                                                            i += 1
                                                                            t = i * 0.05
                                                                            x_8 = x_7 + (v0_x * t)
                                                                            y_8 = y_7 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                                                            self.list_x.append(x_8)
                                                                            self.list_y.append(y_8)
                                                                            self._x = x_8
                                                                            self._y = y_8
                                                                            QWidget.repaint(self)
                                                                            time.sleep(0.005)

                                                                            if self._y > 900:
                                                                                break
                                                                    if self._y > 900:
                                                                        break
                                                            if self._y > 900:
                                                                break

                                                            # 왼쪽 벽
                                                            if self._x < 200:
                                                                v0_y = (9.81 * t) - 0.7 * v0_y
                                                                i = 0
                                                                while True:
                                                                    i += 1
                                                                    t = i * 0.05
                                                                    x_7 = x_6 + (v0_x * t)
                                                                    y_7 = y_6 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                                                    self.list_x.append(x_7)
                                                                    self.list_y.append(y_7)
                                                                    self._x = x_7
                                                                    self._y = y_7
                                                                    QWidget.repaint(self)
                                                                    time.sleep(0.005)

                                                                    if self._y > 900:
                                                                        break
                                                            if self._y > 900:
                                                                break
                                                    if self._y > 900:
                                                        break

                                            # 오른쪽 위 블랙홀
                                            if (798 < self._x < 803) and (390 < self._y < 485):
                                                break

                                            if self._y > 900:
                                                break

                                        # 오른쪽 위 블랙홀
                                        if (798 < self._x < 803) and (390 < self._y < 485):
                                            break

                                        # 오른쪽 아래 블랙홀
                                        if (798 < self._x < 803) and (730 < self._y < 800):
                                            break

                                        if self._y > 900:
                                            break

                                    # 오른쪽 위 블랙홀
                                    if (798 < self._x < 803) and (390 < self._y < 485):
                                        break

                                    # 오른쪽 아래 블랙홀
                                    if (798 < self._x < 803) and (730 < self._y < 800):
                                        break

                                    if self._y > 900:
                                        break

                            # 오른쪽 위 블랙홀
                            if (798 < self._x < 803) and (390 < self._y < 485):
                                break

                            # 오른쪽 아래 블랙홀
                            if (798 < self._x < 803) and (730 < self._y < 800):
                                break

                            if self._y > 900:
                                break

                            # 왼쪽 벽
                            if self._x < 200:
                                v0_y = (9.81 * t) - 0.7 * v0_y
                                i = 0
                                while True:
                                    i += 1
                                    t = i * 0.05
                                    x_3 = x_2 + (v0_x * t)
                                    y_3 = y_2 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                    self.list_x.append(x_3)
                                    self.list_y.append(y_3)
                                    self._x = x_3
                                    self._y = y_3
                                    QWidget.repaint(self)
                                    time.sleep(0.005)

                                    # 2번
                                    if (300 < self._x < 450) and (424 < self._y < 426):
                                        v0_y = (9.81 * t) - v0_y
                                        i = 0
                                        while True:
                                            i += 1
                                            t = i * 0.05
                                            x_4 = x_3 + (v0_x * t)
                                            y_4 = y_3 - (0.7 * v0_y * t) + (0.5 * 9.81 * t * t)

                                            self.list_x.append(x_4)
                                            self.list_y.append(y_4)
                                            self._x = x_4
                                            self._y = y_4
                                            QWidget.repaint(self)
                                            time.sleep(0.005)

                                            if self._y > 900:
                                                break

                                    # 오른쪽 위 블랙홀
                                    if (798 < self._x < 803) and (400 < self._y < 480):
                                        break

                                    if self._y > 900:
                                        break

                            # 오른쪽 위 블랙홀
                            if (798 < self._x < 803) and (390 < self._y < 485):
                                break

                            # 오른쪽 아래 블랙홀
                            if (798 < self._x < 803) and (730 < self._y < 800):
                                break

                            if self._y > 900:
                                break

                    # 오른쪽 위 블랙홀
                    if (798 < self._x < 803) and (390 < self._y < 485):
                        break

                    # 오른쪽 아래 블랙홀
                    if (798 < self._x < 803) and (730 < self._y < 800):
                        break

                    if self._y > 900:
                        break

            # 오른쪽 위 블랙홀
            if (798 < self._x < 803) and (390 < self._y < 485):
                break

            # 오른쪽 아래 블랙홀
            if (798 < self._x < 803) and (730 < self._y < 800):
                break

            if self._y > 900:
                break
            #1번 끝

            # 2번
            if (300 < self._x < 450) and (424 < self._y < 426):
                v0_y = (9.81 * t)
                i = 0
                while True:
                    i += 1
                    t = i * 0.05
                    x_1 = x + (v0_x * t)
                    y_1 = y - (0.7 * v0_y * t) + (0.5 * 9.81 * t * t)

                    self.list_x.append(x_1)
                    self.list_y.append(y_1)
                    self._x = x_1
                    self._y = y_1
                    QWidget.repaint(self)
                    time.sleep(0.005)

                    # 오른쪽 벽
                    if self._x > 800:
                        v0_y = (9.81 * t) - 0.7 * v0_y
                        i = 0
                        while True:
                            i += 1
                            t = i * 0.05
                            x_2 = x_1 - (v0_x * t)
                            y_2 = y_1 + (v0_y * t) + (0.5 * 9.81 * t * t)

                            self.list_x.append(x_2)
                            self.list_y.append(y_2)
                            self._x = x_2
                            self._y = y_2
                            QWidget.repaint(self)
                            time.sleep(0.005)

                            if self._y > 900:
                                break

                            # 오른쪽 아래 블랙홀
                            if (798 < self._x < 803) and (730 < self._y < 800):
                                break

                        if self._y > 900:
                            break

                        # 오른쪽 아래 블랙홀
                        if (798 < self._x < 803) and (730 < self._y < 800):
                            break

                    # 3번
                    if (550 < self._x < 700) and (625 < self._y < 630):
                        v0_y = (9.81 * t) - v0_y
                        i = 0
                        while True:
                            i += 1
                            t = i * 0.05
                            x_2 = x_1 + (v0_x * t)
                            y_2 = y_1 - (0.7 * v0_y * t) + (0.5 * 9.81 * t * t)

                            self.list_x.append(x_2)
                            self.list_y.append(y_2)
                            self._x = x_2
                            self._y = y_2
                            QWidget.repaint(self)
                            time.sleep(0.005)

                            # 오른쪽 벽
                            if self._x > 800:
                                v0_y = (9.81 * t) - 0.7 * v0_y
                                i = 0
                                while True:
                                    i += 1
                                    t = i * 0.05
                                    x_3 = x_2 - (v0_x * t)
                                    y_3 = y_2 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                    self.list_x.append(x_3)
                                    self.list_y.append(y_3)
                                    self._x = x_3
                                    self._y = y_3
                                    QWidget.repaint(self)
                                    time.sleep(0.005)

                                    # 오른쪽 위 블랙홀
                                    if (798 < self._x < 803) and (400 < self._y < 480):
                                        break

                                    if self._y > 900:
                                        break

                            # 오른쪽 위 블랙홀
                            if (798 < self._x < 803) and (400 < self._y < 480):
                                break

                            # 오른쪽 아래 블랙홀
                            if (798 < self._x < 803) and (730 < self._y < 800):
                                break

                            if self._y > 900:
                                break

                    # 오른쪽 위 블랙홀
                    if (798 < self._x < 803) and (400 < self._y < 480):
                        break

                    # 오른쪽 아래 블랙홀
                    if (798 < self._x < 803) and (730 < self._y < 800):
                        break

                    if self._y > 900:
                        break

            # 오른쪽 위 블랙홀
            if (798 < self._x < 803) and (390 < self._y < 485):
                break

            # 오른쪽 아래 블랙홀
            if (798 < self._x < 803) and (730 < self._y < 800):
                break

            if self._y > 900:
                break
            #2번 끝

            # 3번
            if (550 < self._x < 700) and (625 < self._y < 630):
                v0_y = (9.81 * t)
                i = 0
                while True:
                    i += 1
                    t = i * 0.05
                    x_1 = x + (v0_x * t)
                    y_1 = y - (0.7 * v0_y * t) + (0.5 * 9.81 * t * t)

                    self.list_x.append(x_1)
                    self.list_y.append(y_1)
                    self._x = x_1
                    self._y = y_1
                    QWidget.repaint(self)
                    time.sleep(0.005)

                    # 오른쪽 벽
                    if self._x > 800:
                        v0_y = (9.81 * t) - 0.7 * v0_y
                        i = 0
                        while True:
                            i += 1
                            t = i * 0.05
                            x_2 = x_1 - (v0_x * t)
                            y_2 = y_1 + (v0_y * t) + (0.5 * 9.81 * t * t)

                            self.list_x.append(x_2)
                            self.list_y.append(y_2)
                            self._x = x_2
                            self._y = y_2
                            QWidget.repaint(self)
                            time.sleep(0.005)

                            # 2번
                            if (300 < self._x < 450) and (424 < self._y < 426):
                                v0_y = (9.81 * t) + v0_y
                                i = 0
                                while True:
                                    i += 1
                                    t = i * 0.05
                                    x_3 = x_2 - (v0_x * t)
                                    y_3 = y_2 - (0.7 * v0_y * t) + (0.5 * 9.81 * t * t)

                                    self.list_x.append(x_3)
                                    self.list_y.append(y_3)
                                    self._x = x_3
                                    self._y = y_3
                                    QWidget.repaint(self)
                                    time.sleep(0.005)

                                    # 좌측벽
                                    if self._x < 200:
                                        v0_y = (9.81 * t) - v0_y
                                        i = 0

                                        while True:
                                            i += 1
                                            t = i * 0.05
                                            x_4 = x_3 + (v0_x * t)
                                            y_4 = y_3 - ((0.7 * v0_y * t) - (0.5 * 9.81 * t * t))

                                            self.list_x.append(x_4)
                                            self.list_y.append(y_4)
                                            self._x = x_4
                                            self._y = y_4
                                            QWidget.repaint(self)
                                            time.sleep(0.005)

                                            # 2번
                                            if (300 < self._x < 450) and (424 < self._y < 426):
                                                v0_y = (9.81 * t) - v0_y
                                                i = 0

                                                while True:
                                                    i += 1
                                                    t_5 = i * 0.05
                                                    x_5 = x_4 + v0_x * t_5
                                                    y_5 = y_4 - ((0.7 * v0_y * t_5) - (0.5 * 9.81 * t_5 * t_5))

                                                    self.list_x.append(x_5)
                                                    self.list_y.append(y_5)
                                                    self._x = x_5
                                                    self._y = y_5
                                                    QWidget.repaint(self)
                                                    time.sleep(0.005)

                                                    # 2번
                                                    if (300 < self._x < 450) and (424 < self._y < 426):
                                                        v0_y = (9.81 * t) - (0.7 * v0_y)
                                                        i = 0

                                                        while True:
                                                            i += 1
                                                            t = i * 0.05
                                                            x_6 = x_5 + v0_x * t
                                                            y_6 = y_5 - ((0.7 * v0_y * t) - (0.5 * 9.81 * t * t))

                                                            self.list_x.append(x_6)
                                                            self.list_y.append(y_6)
                                                            self._x = x_6
                                                            self._y = y_6
                                                            QWidget.repaint(self)
                                                            time.sleep(0.005)

                                                            # 3번
                                                            if (550 < self._x < 700) and (625 < self._y < 630):
                                                                v0_y = (9.81 * t) - (0.7 * v0_y)
                                                                i = 0
                                                                while True:
                                                                    i += 1
                                                                    t = i * 0.05
                                                                    x_7 = x_6 - (v0_x * t)
                                                                    y_7 = y_6 + (0.7 * v0_y * t) + (0.5 * 9.81 * t * t)

                                                                    self.list_x.append(x_7)
                                                                    self.list_y.append(y_7)
                                                                    self._x = x_7
                                                                    self._y = y_7
                                                                    QWidget.repaint(self)
                                                                    time.sleep(0.005)

                                                                    if self._y > 900:
                                                                        break

                                                            # 오른쪽 아래 블랙홀
                                                            if (798 < self._x < 803) and (730 < self._y < 800):
                                                                break

                                                            if self._y > 900:
                                                                break

                                                    # 오른쪽 아래 블랙홀
                                                    if (798 < self._x < 803) and (730 < self._y < 800):
                                                        break

                                                    if self._y > 900:
                                                        break

                                            # 오른쪽 아래 블랙홀
                                            if (798 < self._x < 803) and (730 < self._y < 800):
                                                break

                                            if self._y > 900:
                                                break

                                    # 오른쪽 아래 블랙홀
                                    if (798 < self._x < 803) and (730 < self._y < 800):
                                        break

                                    if self._y > 900:
                                        break

                            # 오른쪽 아래 블랙홀
                            if (798 < self._x < 803) and (730 < self._y < 800):
                                break

                            if self._y > 900:
                                break

                    # 오른쪽 위 블랙홀
                    if (798 < self._x < 803) and (400 < self._y < 480):
                        break

                    # 오른쪽 아래 블랙홀
                    if (798 < self._x < 803) and (730 < self._y < 800):
                        break

                    if self._y > 900:
                        break

            # 오른쪽 위 블랙홀
            if (798 < self._x < 803) and (390 < self._y < 485):
                break

            if self._y > 900:
                break
            #3번 끝

            # 오른쪽 벽
            if self._x > 800:
                v0_y = (9.81 * t)
                i = 0
                while True:
                    i += 1
                    t_1 = i * 0.05
                    x_1 = x - (v0_x * t_1)
                    y_1 = y + (v0_y * t_1) + (0.5 * 9.81 * t_1 * t_1)

                    self.list_x.append(x_1)
                    self.list_y.append(y_1)
                    self._x = x_1
                    self._y = y_1
                    QWidget.repaint(self)
                    time.sleep(0.005)

                    # 1번
                    if (500 < self._x < 650) and (250 < self._y < 260):
                        v0_y = (9.81 * t) * 0.7
                        i = 0
                        while True:
                            i += 1
                            t = i * 0.05
                            x_2 = x_1 - (v0_x * t)
                            y_2 = y_1 - (v0_y * t) + (0.5 * 9.81 * t * t)

                            self.list_x.append(x_2)
                            self.list_y.append(y_2)
                            self._x = x_2
                            self._y = y_2
                            QWidget.repaint(self)
                            time.sleep(0.005)

                            # 왼쪽 벽
                            if self._x < 200:
                                v0_y = (9.81 * t) * 0.7
                                i = 0
                                while True:
                                    i += 1
                                    t = i * 0.05
                                    x_3 = x_2 + (v0_x * t)
                                    y_3 = y_2 - (v0_y * t) + (0.5 * 9.81 * t * t)

                                    self.list_x.append(x_3)
                                    self.list_y.append(y_3)
                                    self._x = x_3
                                    self._y = y_3
                                    QWidget.repaint(self)
                                    time.sleep(0.005)

                                    # 오른쪽 벽
                                    if self._x > 800:
                                        v0_y = (9.81 * t) - 0.7 * v0_y
                                        i = 0
                                        while True:
                                            i += 1
                                            t = i * 0.05
                                            x_4 = x_3 - (v0_x * t)
                                            y_4 = y_3 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                            self.list_x.append(x_4)
                                            self.list_y.append(y_4)
                                            self._x = x_4
                                            self._y = y_4
                                            QWidget.repaint(self)
                                            time.sleep(0.005)

                                            # 3번
                                            if (550 < self._x < 700) and (625 < self._y < 630):
                                                v0_y = (9.81 * t) - v0_y
                                                i = 0
                                                while True:
                                                    i += 1
                                                    t = i * 0.05
                                                    x_5 = x_4 - (v0_x * t)
                                                    y_5 = y_4 + (0.7 * v0_y * t) + (0.5 * 9.81 * t * t)

                                                    self.list_x.append(x_5)
                                                    self.list_y.append(y_5)
                                                    self._x = x_5
                                                    self._y = y_5
                                                    QWidget.repaint(self)
                                                    time.sleep(0.005)

                                                    if self._y > 900:
                                                        break

                                            # 왼쪽 벽
                                            if self._x < 200:
                                                v0_y = (9.81 * t) * 0.7
                                                i = 0
                                                while True:
                                                    i += 1
                                                    t = i * 0.05
                                                    x_5 = x_4 + (v0_x * t)
                                                    y_5 = y_4 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                                    self.list_x.append(x_5)
                                                    self.list_y.append(y_5)
                                                    self._x = x_5
                                                    self._y = y_5
                                                    QWidget.repaint(self)
                                                    time.sleep(0.005)

                                                    # 3번
                                                    if (550 < self._x < 700) and (625 < self._y < 630):
                                                        v0_y = (9.81 * t) - v0_y
                                                        i = 0
                                                        while True:
                                                            i += 1
                                                            t = i * 0.05
                                                            x_6 = x_5 + (v0_x * t)
                                                            y_6 = y_5 - (0.7 * v0_y * t) + (0.5 * 9.81 * t * t)

                                                            self.list_x.append(x_6)
                                                            self.list_y.append(y_6)
                                                            self._x = x_6
                                                            self._y = y_6
                                                            QWidget.repaint(self)
                                                            time.sleep(0.005)

                                                    # 오른쪽 벽
                                                    if self._x > 800:
                                                        v0_y = (9.81 * t) - 0.7 * v0_y
                                                        i = 0
                                                        while True:
                                                            i += 1
                                                            t = i * 0.05
                                                            x_6 = x_5 - (v0_x * t)
                                                            y_6 = y_5 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                                            self.list_x.append(x_6)
                                                            self.list_y.append(y_6)
                                                            self._x = x_6
                                                            self._y = y_6
                                                            QWidget.repaint(self)
                                                            time.sleep(0.005)

                                                            # 왼쪽 벽
                                                            if self._x < 200:
                                                                v0_y = (9.81 * t) * 0.7
                                                                i = 0
                                                                while True:
                                                                    i += 1
                                                                    t = i * 0.05
                                                                    x_7 = x_6 + (v0_x * t)
                                                                    y_7 = y_6 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                                                    self.list_x.append(x_7)
                                                                    self.list_y.append(y_7)
                                                                    self._x = x_7
                                                                    self._y = y_7
                                                                    QWidget.repaint(self)
                                                                    time.sleep(0.005)

                                                                    if self._y > 900:
                                                                        break

                                                            if self._y > 900:
                                                                break

                                                    if self._y > 900:
                                                        break

                                            if self._y > 900:
                                                break

                                    if self._y > 900:
                                        break

                                    # 오른쪽 위 블랙홀
                                    if (798 < self._x < 803) and (400 < self._y < 480):
                                        break

                            if self._y > 900:
                                break

                            # 오른쪽 위 블랙홀
                            if (798 < self._x < 803) and (400 < self._y < 480):
                                break

                    # 2번
                    if (300 < self._x < 450) and (425 < self._y < 430):
                        v0_y = (9.81 * t) * 0.7
                        i = 0
                        while True:
                            i += 1
                            t = i * 0.05
                            x_2 = x_1 - (v0_x * t)
                            y_2 = y_1 - (v0_y * t) + (0.5 * 9.81 * t * t)

                            self.list_x.append(x_2)
                            self.list_y.append(y_2)
                            self._x = x_2
                            self._y = y_2
                            QWidget.repaint(self)
                            time.sleep(0.005)

                            # 왼쪽 벽
                            if self._x < 200:
                                v0_y = (9.81 * t) * 0.7
                                i = 0
                                while True:
                                    i += 1
                                    t = i * 0.05
                                    x_3 = x_2 + (v0_x * t)
                                    y_3 = y_2 - (v0_y * t) + (0.5 * 9.81 * t * t)

                                    self.list_x.append(x_3)
                                    self.list_y.append(y_3)
                                    self._x = x_3
                                    self._y = y_3
                                    QWidget.repaint(self)
                                    time.sleep(0.005)

                                    # 오른쪽 벽
                                    if self._x > 800:
                                        v0_y = (9.81 * t) * 0.7
                                        i = 0
                                        while True:
                                            i += 1
                                            t = i * 0.05
                                            x_4 = x_3 - (v0_x * t)
                                            y_4 = y_3 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                            self.list_x.append(x_4)
                                            self.list_y.append(y_4)
                                            self._x = x_4
                                            self._y = y_4
                                            QWidget.repaint(self)
                                            time.sleep(0.005)

                                            # 왼쪽 벽
                                            if self._x < 200:
                                                v0_y = (9.81 * t) * 0.7
                                                i = 0
                                                while True:
                                                    i += 1
                                                    t = i * 0.05
                                                    x_5 = x_4 + (v0_x * t)
                                                    y_5 = y_4 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                                    self.list_x.append(x_5)
                                                    self.list_y.append(y_5)
                                                    self._x = x_5
                                                    self._y = y_5
                                                    QWidget.repaint(self)
                                                    time.sleep(0.005)

                                                    if self._y > 900:
                                                        break

                                            if self._y > 900:
                                                break

                                    # 오른쪽 위 블랙홀
                                    if (797 < self._x < 802) and (400 < self._y < 480):
                                        break

                                    if self._y > 900:
                                        break

                            # 오른쪽 위 블랙홀
                            if (797 < self._x < 802) and (400 < self._y < 480):
                                break

                            if self._y > 900:
                                break

                    # 오른쪽 위 블랙홀
                    if (797 < self._x < 802) and (400 < self._y < 480):
                        break

                    if self._y > 900:
                        break

                    # 3번
                    if (550 < self._x < 700) and (625 < self._y < 630):
                        v0_y = (9.81 * (t + t_1))
                        i = 0
                        while True:
                            i += 1
                            t = i * 0.05
                            x_2 = x_1 - (v0_x * t)
                            y_2 = y_1 - (0.7 * v0_y * t) + (0.5 * 9.81 * t * t)

                            self.list_x.append(x_2)
                            self.list_y.append(y_2)
                            self._x = x_2
                            self._y = y_2
                            QWidget.repaint(self)
                            time.sleep(0.005)

                            # 왼쪽 벽
                            if self._x < 200:
                                v0_y = (9.81 * t) * 0.7
                                i = 0
                                while True:
                                    i += 1
                                    t = i * 0.05
                                    x_3 = x_2 + (v0_x * t)
                                    y_3 = y_2 - (v0_y * t) + (0.5 * 9.81 * t * t)

                                    self.list_x.append(x_3)
                                    self.list_y.append(y_3)
                                    self._x = x_3
                                    self._y = y_3
                                    QWidget.repaint(self)
                                    time.sleep(0.005)

                                    # 오른쪽 위 블랙홀
                                    if (797 < self._x < 802) and (400 < self._y < 480):
                                        break

                                    if self._y > 900:
                                            break

                            # 오른쪽 위 블랙홀
                            if (797 < self._x < 802) and (400 < self._y < 480):
                                break

                            if self._y > 900:
                                break

                    # 오른쪽 위 블랙홀
                    if (797 < self._x < 802) and (400 < self._y < 480):
                        break

                    if self._y > 900:
                        break

                    # 왼쪽 벽
                    if self._x < 200:
                        v0_y = (9.81 * t) * 0.7
                        i = 0
                        while True:
                            i += 1
                            t = i * 0.05
                            x_2 = x_1 + (v0_x * t)
                            y_2 = y_1 + (v0_y * t) + (0.5 * 9.81 * t * t)

                            self.list_x.append(x_2)
                            self.list_y.append(y_2)
                            self._x = x_2
                            self._y = y_2
                            QWidget.repaint(self)
                            time.sleep(0.005)

                            # 오른쪽 벽
                            if self._x > 800:
                                v0_y = (9.81 * t) * 0.7
                                i = 0
                                while True:
                                    i += 1
                                    t = i * 0.05
                                    x_3 = x_2 - (v0_x * t)
                                    y_3 = y_2 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                    self.list_x.append(x_3)
                                    self.list_y.append(y_3)
                                    self._x = x_3
                                    self._y = y_3
                                    QWidget.repaint(self)
                                    time.sleep(0.005)

                                    # 왼쪽 블랙홀
                                    if (198 < self._x < 203) and (700 < self._y < 780):
                                        break

                                    # 왼쪽 벽
                                    if self._x < 200:
                                        v0_y = (9.81 * t) * 0.7
                                        i = 0
                                        while True:
                                            i += 1
                                            t = i * 0.05
                                            x_4 = x_3 + (v0_x * t)
                                            y_4 = y_3 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                            self.list_x.append(x_4)
                                            self.list_y.append(y_4)
                                            self._x = x_4
                                            self._y = y_4
                                            QWidget.repaint(self)
                                            time.sleep(0.005)

                                            # 오른쪽 벽
                                            if self._x > 800:
                                                v0_y = (9.81 * t) * 0.7
                                                i = 0
                                                while True:
                                                    i += 1
                                                    t = i * 0.05
                                                    x_5 = x_4 - (v0_x * t)
                                                    y_5 = y_4 + (v0_y * t) + (0.5 * 9.81 * t * t)

                                                    self.list_x.append(x_5)
                                                    self.list_y.append(y_5)
                                                    self._x = x_5
                                                    self._y = y_5
                                                    QWidget.repaint(self)
                                                    time.sleep(0.005)

                                                    if self._y > 900:
                                                        break
                                            if self._y > 900:
                                                break
                                    if self._y > 900:
                                        break

                            # 왼쪽 블랙홀
                            if (198 < self._x < 203) and (700 < self._y < 780):
                                break

                            if self._y > 900:
                                break

                    # 오른쪽 위 블랙홀
                    if (797 < self._x < 802) and (400 < self._y < 480):
                        break

                    # 왼쪽 블랙홀
                    if (198 < self._x < 203) and (700 < self._y < 780):
                        break

                    if self._y > 900:
                        break

            # 오른쪽 위 블랙홀
            if (797 < self._x < 802) and (400 < self._y < 480):
                break

            # 오른쪽 아래 블랙홀
            if (798 < self._x < 803) and (730 < self._y < 800):
                break

            # 왼쪽 블랙홀
            if (198 < self._x < 203) and (700 < self._y < 780):
                break

            if self._y > 900:
                break
            #오른쪽 벽 끝

        #스코어 계산
        score = round(len(self.list_x) * 0.05, 3)
        self.listscore.append(score)

        self.statusBar().showMessage("GAME OVER 점수는 " + str(score) + "점 입니다.")


    # 저장 버튼
    def saveButtonClicked(self):
        save_csv_score(self.listname, self.listscore)
        save_csv(self.list_x, self.list_y)
        self.statusBar().showMessage("파일로 저장 완료 하였습니다.")
        return

    # 종료시
    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, "종료확인", "종료 하시겠습니까?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_point(qp, self._x, self._y)
        qp.end()

    def draw_point(self, qp, _x, _y):
        # 외벽
        qp.setPen(QPen(Qt.black, 4))
        qp.drawLine(50, 50, 800, 50)
        qp.drawLine(800, 50, 800, 900)
        qp.drawLine(800, 900, 200, 900)
        qp.drawLine(200, 900, 200, 100)
        qp.drawLine(200, 100, 50, 100)
        qp.drawLine(50, 100, 50, 50)

        # 장애물
        qp.setPen(QPen(Qt.black, 7))
        qp.drawLine(500, 250, 650, 250)
        qp.drawLine(300, 425, 450, 425)
        qp.drawLine(550, 625, 700, 625)

        # 블랙홀
        qp.setPen(QPen(Qt.red, 15))
        qp.drawLine(200, 700, 200, 780)
        qp.drawLine(800, 400, 800, 480)
        qp.drawLine(800, 730, 800, 800)
        qp.drawLine(795, 900, 205, 900)

        qp.setPen(QPen(Qt.black, 4))
        qp.drawLine(900, 100, 1400, 100)
        qp.drawLine(900, 300, 1400, 300)

        qp.drawLine(900, 350, 1400, 350)
        qp.drawLine(900, 650, 1400, 650)

        qp.setPen(QPen(Qt.blue, 15))
        _x = self._x
        _y = self._y
        qp.drawPoint(_x, _y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec()