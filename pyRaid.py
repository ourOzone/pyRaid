import sys
import time
import os
import random
import numpy as np
from pynput.keyboard import Key, Listener
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QMainWindow, QVBoxLayout, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtCore import Qt, QCoreApplication
import math
import threading

random.seed()
timeSpeed = 1
miliTime = timeSpeed / 1000
app = QApplication(sys.argv)
desktop = QDesktopWidget().screenGeometry()
lastHit = 0


onA = False
onD = False


DB = {
    "player": {
        "location": [int(desktop.width() / 2) - 10, int(desktop.height() / 1.3)],
        "size": 10,
        "lineColor": [114 ,9, 183, 4],
        "fillIn": [0, 0, 0],
        "speed": 0.7,
        "gravity": [0, 9.8 * miliTime],
        "onGround": False,
        "heart": 3
    },
    
    "floor": [
        {
            "location": [150,1150],
            "size": [700,0],
            "lineColor": [114 ,9, 183, 10],
            "fillIn": [],
        },
        
        {
            "location": [1750,1150],
            "size": [700,0],
            "lineColor": [114 ,9, 183, 10],
            "fillIn": [],
        },
        
        {
            "location": [950,950],
            "size": [700,0],
            "lineColor": [114 ,9, 183, 10],
            "fillIn": [],
        },
        
        {
            "location": [150,750],
            "size": [700,0],
            "lineColor": [114 ,9, 183, 10],
            "fillIn": [],
        },
        
        {
            "location": [1750,750],
            "size": [700,0],
            "lineColor": [114 ,9, 183, 10],
            "fillIn": [],
        },
        
        ],
    
    
    "ground": [
        [0, int(desktop.height() / 1.3) + 70]
    ],
    
    "boss": {
        "location": [int(desktop.width() / 2) - 30, int(desktop.height() / 7)],
        "size": 60,
        "lineColor":[114 ,9, 183, 4],
        "fillIn":[0, 0, 0],
        "speed": 1.5
        },
    
    "laser": {
        "location":[0,0,0,0],
        "lineColor":[114 ,9, 183, 2],
        "speed": 300,
        },
    
    
    "spear": [
        {
            "location": [500, 100],
            "length": 800,
            "lineColor":[0, 119, 182, 3],
            }
        ],
    
    "boomb": [
        
        ],
    
    "boombInfo": 
        {
            "size": (20, 30),
            "lineColor":[114 ,9, 183, 0],
            "fillIn":[0, 0, 0],
            },
        
    "bullet":
        [],
        
}

    
class Bullet:
    def __init__(self):
        pass
    
    def add_bullet(self, address):
        speed = 4
        DB["bullet"] = []
        
        bullet_obj = {
            "size": [10, 10],
            "lineColor": [114 ,9, 183, 4],
            "location": address,
            }
        temp = speed * math.cos(math.pi / 4)
        speeds = [(speed, 0), (-speed, 0), (0, speed), (0, -speed), (temp, temp), (temp, -temp), (-temp, temp), (-temp, -temp)]
        
        
        for speed in speeds:
            new_bullet_obj = bullet_obj.copy()
            new_bullet_obj["speed"] = speed
            DB["bullet"].append(new_bullet_obj)
        
    def move_bullet(self):
        for i in DB["bullet"]:
            i["location"] = [x + y for x, y in zip(i["location"], i["speed"])]
    
    def is_hit(self):
        for i in DB["bullet"]:
            dx = i["location"][0] - DB["player"]["location"][0]
            dy = i["location"][1] - DB["player"]["location"][1]
            bullet_distance = math.sqrt(dx **2 + dy **2)
            if bullet_distance <= DB["player"]["size"] + DB["bullet"]["size"][0]:
                return True
            
            return False
            
        




def distance(point, line):
    x, y = point[0], point[1]
    x1, y1, x2, y2 = line[0], line[1], line[2], line[3]

    # 두 점을 지나는 직선의 기울기 계산
    m = (y2 - y1) / (x2+0.1 - x1)

    # y절편 계산
    b = y1 - m * x1

    # 직선으로부터의 거리를 계산하는 공식을 사용
    distance = abs(m * x - y + b) / math.sqrt(m**2 + 1)

    return distance


class QWidget_(QWidget):
    def endGame(self):
        if DB["player"]["heart"] <= 0:
            self.close()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QBrush(QColor(0, 0, 0)))
        
        #발판 그리기
        for i in DB["floor"]:
            pen = QPen(QColor(i["lineColor"][0],i["lineColor"][1],i["lineColor"][2]))
            pen.setWidth(i["lineColor"][3])
            painter.setPen(pen)

            painter.drawLine(i["location"][0]-self.pos().x(), i["location"][1]-self.pos().y() ,i["location"][0] + i["size"][0]-self.pos().x(), i["location"][1]+i["size"][1]-self.pos().y())  # 막대 그리기

        #보스 그리기
        pen = QPen(QColor(DB["boss"]["lineColor"][0],DB["boss"]["lineColor"][1], DB["boss"]["lineColor"][2]))
        pen.setWidth(DB["boss"]["lineColor"][3])
        painter.setPen(pen)
        painter.drawEllipse(int(DB["boss"]["location"][0])-self.pos().x(),int(DB["boss"]["location"][1])-self.pos().y(), 2*DB["boss"]["size"], 2*DB["boss"]["size"])
        
        #레이저 그리기
        pen = QPen(QColor(DB["laser"]["lineColor"][0],DB["laser"]["lineColor"][1], DB["laser"]["lineColor"][2]))
        pen.setWidth(DB["laser"]["lineColor"][3])
        painter.setPen(pen)
        painter.drawLine(int(DB["laser"]["location"][0])-self.pos().x(), int(DB["laser"]["location"][1])-self.pos().y(), int(DB["laser"]["location"][2])-self.pos().x(), int(DB["laser"]["location"][3]))
    
        #플레이어 그리기
        pen = QPen(QColor(DB["player"]["lineColor"][0], DB["player"]["lineColor"][1], DB["player"]["lineColor"][2]))
        pen.setWidth(DB["player"]["lineColor"][3])
        brush = QBrush(QColor(DB["player"]["fillIn"][0], DB["player"]["fillIn"][1], DB["player"]["fillIn"][2]))
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(int(DB["player"]["location"][0]) - self.pos().x(), int(DB["player"]["location"][1]) - self.pos().y(), 2 * DB["player"]["size"], 2 * DB["player"]["size"])
        
        #폭탄 그리기
        if len(DB["boomb"]) != 0:
            painter.setPen(QColor(DB["boombInfo"]["lineColor"][0], DB["boombInfo"]["lineColor"][1], DB["boombInfo"]["lineColor"][2]))
            painter.setBrush(QColor(DB["boombInfo"]["fillIn"][0], DB["boombInfo"]["fillIn"][1], DB["boombInfo"]["fillIn"][2]))
            #painter.setWidth(DB["boombInfo"]["lineColor"][3])
            painter.drawRect(DB["boomb"][0][0] - self.pos().x(), DB["boomb"][0][1] - self.pos().y(), 20, 30)
        
        #총알 그리기
        for i in DB["bullet"]:
            pen = QPen(QColor(i["lineColor"][0],i["lineColor"][1],i["lineColor"][2]))
            pen.setWidth(i["lineColor"][3])
            painter.setPen(pen)

            painter.drawEllipse(int(i["location"][0]-self.pos().x()), int(i["location"][1]-self.pos().y()) , i["size"][0], i["size"][1])


            
            
class GameOver(QWidget_):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(-500, 4000, 600, 300)
        self.label = QLabel("GAME OVER", self)
        
        rage_against_the_machine = [
            "Killing In The Name",
            "Sleep Now In The Fire",
            "Take The Power Back",
            "Wake Up",
            "Bulls On Parade",
            "Testify",
            "Bombtrack",
            "Bullet In Your Head",
            "Know Your Enemy",
            "Freedom",
            "Guerrilla Radio"
        ]

        text = random.choice(rage_against_the_machine)
        
        self.label.setStyleSheet("color: rgb(114, 9, 183);")
        self.extra_label = QLabel(text, self)
        self.extra_label.setStyleSheet("color: rgb(114, 9, 183);")

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.extra_label)
        self.setLayout(layout)
        self.label.setAlignment(Qt.AlignCenter)
        self.extra_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        self.show()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tictaktoc)
        self.timer.start(1000)  # 1초마다 업데이트

    def tictaktoc(self):
        if DB["player"]["heart"] > 0:
            self.setGeometry(-1100,-1100,600,300)
        else:
            self.moveCenter()
            #time.sleep(3)
            #os.system("shutdown /s /t 1") 

    def moveCenter(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(int(x), int(y))   



class Player(QWidget_):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel('', self)
        self.label.setGeometry(5, 5, 200, 50)
        self.setWindowTitle('PyRaid')
        self.setGeometry(DB["player"]["location"][0] - 350, DB["player"]["location"][1] - 200, 700, 350)
        self.show()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tikTacTok)
        self.timer.start(timeSpeed)
        self.label.setStyleSheet("color: rgb(114, 9, 183);")


    def tikTacTok(self):
        heart = str(DB['player']['heart'])
        self.label.setText( "남은 목숨: "+heart)
        #중력
        ground = DB["ground"][0][1]
        if DB["player"]["onGround"] == False:
            DB["player"]["location"][1] += DB["player"]["gravity"][0]
            DB["player"]["gravity"][0] += DB["player"]["gravity"][1]
        else:
            DB["player"]["gravity"][0]=0
            
            
        if DB["player"]["location"][1] >= ground and DB["player"]["onGround"] == False:
            DB["player"]["onGround"] = True
            DB["player"]["gravity"][0] = 0
            DB["player"]["location"][1] = ground
            
            
        #키보드 입력    
        if onA:
            DB["player"]["location"][0]-= DB["player"]["speed"]

        if onD:
            DB["player"]["location"][0] += DB["player"]["speed"]  
            
            
        #화면 이동
        if self.pos().x() + 200 >= DB["player"]["location"][0]:
            self.move(self.pos().x()-1, self.pos().y())
        if self.pos().x() + 500 <= DB["player"]["location"][0]:
            self.move(self.pos().x()+1, self.pos().y())
            
        if self.pos().y() + 80 >= DB["player"]["location"][1]:
            self.move(self.pos().x(), self.pos().y()-1)
        if self.pos().y() + 270  <= DB["player"]["location"][1]:
            self.move(self.pos().x(), self.pos().y()+1)
        
        self.endGame()
        self.update()
        

class Floor(QWidget_):
    def __init__(self,floor):
        super().__init__()
        self.temp0=False
        self.floor = floor
        self.onThis = False 
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tikTacTok)
        self.timer.start(timeSpeed)

    def initUI(self):
        self.setWindowTitle('floor')
        self.setGeometry(self.floor["location"][0]-50, self.floor["location"][1]-50, self.floor["size"][0]+100, 200)  # 창 위치와 크기 설정
        self.show()


    def tikTacTok(self):
        
        temp = self.temp0
        if DB["player"]["location"][1] >self.floor["location"][1] - 2*DB["player"]["size"]:
            self.temp0 = False
        else:
            self.temp0 = True
            
            
        if self.onThis == True and (DB["player"]["location"][0] < self.floor["location"][0] or DB["player"]["location"][0] > self.floor["location"][0]+self.floor["size"][0]):
            DB["player"]["onGround"] = False
            self.onThis = False
            
            
        if temp==True and self.isUndereGround():
            self.onThis = True
            DB["player"]["onGround"] = True
            DB["player"]["location"][1] = self.floor["location"][1] - 2*DB["player"]["size"]
            DB["player"]["gravity"][0] = 0
        self.endGame()
        self.update()
        
        
    def isUndereGround(self):
        x,y = DB["player"]["location"][0], DB["player"]["location"][1]
        if x >= self.floor["location"][0] and x<= self.floor["location"][0]+self.floor["size"][0] and y>= self.floor["location"][1] - 2*DB["player"]["size"]:
            return True
        return False
    
class Boss(QWidget_):
    def __init__(self):
        super().__init__()
        self.initUI()    
        self.bul = Bullet()
        
    
    def initUI(self):
        self.a = 0
        self.hitTimmer = 0
        self.temp =[]
        self.laserOn = True
        self.laserLocation = [0,0,0,0]
        self.setWindowTitle("Boss1's name")
        self.setGeometry(DB["boss"]["location"][0]-250+DB["boss"]["size"], DB["boss"]["location"][1]-250+3*DB["boss"]["size"], 500, 500)
        self.debounceTimer = time.time()
        self.show()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tikTacTok)
        self.timer.start(timeSpeed)

    def tikTacTok(self):
        self.bul.move_bullet()
        self.laser()
        self.attack1()
        self.endGame()
        
        if self.pos().x() + 200 >= DB["boss"]["location"][0]:
            self.move(self.pos().x()-3, self.pos().y())
        if self.pos().x() + 210 <= DB["boss"]["location"][0]:
            self.move(self.pos().x()+3, self.pos().y())
            
        if self.pos().y() + 200 >= DB["boss"]["location"][1]:
            self.move(self.pos().x(), self.pos().y()-3)
        if self.pos().y() + 210  <= DB["boss"]["location"][1]:
            self.move(self.pos().x(), self.pos().y()+3)
            
            
        self.pPoint = (DB["player"]["location"][0]+DB["player"]["size"],DB["player"]["location"][1]+DB["player"]["size"])
        self.bPoint = (DB["boss"]["location"][0]+DB["boss"]["size"],DB["boss"]["location"][1]+DB["boss"]["size"])

        x1, y1 = self.pPoint
        x2, y2 = self.bPoint
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        if distance <= DB["player"]["size"] + DB["boss"]["size"]:
            self.hitCompute()
        self.update()
    
    def locOn(self):
        ans = [DB["boss"]["location"][0]+DB["boss"]["size"], DB["boss"]["location"][1]+DB["boss"]["size"], DB["player"]["location"][0]+DB["player"]["size"], DB["player"]["location"][1]+DB["player"]["size"]]
        ans[3] = 1000 * ans[3] - 999 * ans[1]
        ans[2] = 1000 * ans[2] - 999 * ans[0]
        return ans
    
    def laser(self):
        if self.laserOn == True:
            DB["laser"]["location"] = self.locOn()

    def circular(self, line, theta_degrees):
        point = np.array([line[2], line[3]])
        center = np.array([line[0], line[1]])
        theta_radians = np.radians(theta_degrees)
        relative_point = point - center
        rotation_matrix = np.array([[np.cos(theta_radians), -np.sin(theta_radians)],[np.sin(theta_radians), np.cos(theta_radians)]])
        new_relative_point = np.dot(rotation_matrix, relative_point)
        new_point = new_relative_point + center

        return new_point[0], new_point[1]
        
    def attack1(self):
        self.now = time.time()
        self.now = (self.now- self.debounceTimer) % 20
        if self.now < 3: #따라다니기    
            self.laserOn = True
        elif self.now < 4: #잠깐 꺼지기
            self.laserOn = False
            if DB["laser"]["location"] !=[0,0,0,0]:
                self.temp = DB["laser"]["location"]
            DB["laser"]["location"] = [0,0,0,0]
        elif self.now < 7: #쏘기
            self.laserOn = False
            if self.checkPosition(self.temp, DB["player"]["location"]) != 1:
                self.temp[2], self.temp[3] = self.circular(self.temp, 0.025)
            else:
                self.temp[2], self.temp[3] = self.circular(self.temp, -0.025)
                
            DB["laser"]["location"] = self.temp
            if  DB["laser"]["lineColor"][3] < 60:
                DB["laser"]["lineColor"][3] +=1
            
            if distance(DB["player"]["location"], self.temp) < 60 - DB["player"]["size"]:\
                self.hitCompute()
            
        else: #꺼지기
            DB["laser"]["lineColor"][3] = 2
            self.laserOn = False
            DB["laser"]["location"] = [0,0,0,0]
            
            
    def hitCompute(self):
        global lastHit
        now = time.time()
        if now - lastHit >1:
            lastHit = now
            DB["player"]["heart"]-=1
            
            
    def attack2(self):
        endPoint = DB["player"]["location"]
        for _ in range(500):
            totalDist = math.sqrt((endPoint[0]-DB["boss"]["location"][0]) ** 2 + (endPoint[1]-DB["boss"]["location"][1]) ** 2)
            ratio = DB["boss"]["speed"] / totalDist
            DB["boss"]["location"][0] += ratio * (endPoint[0] - DB["boss"]["location"][0])
            DB["boss"]["location"][1] += ratio * (endPoint[1] - DB["boss"]["location"][1])
            
            time.sleep(0.001)
            
        
    
    def start_move_thread(self):
        move_thread = threading.Thread(target=self.move_thread_function)
        move_thread.start()

    def move_thread_function(self):
        while True:
            time.sleep(5)
            if self.now > 7:
                
                if random.choice([True, False]):
                    self.attack2()
                else:
                    self.bul.add_bullet([x + DB["boss"]["size"] for x in DB["boss"]["location"]])

            
    def checkPosition(self, line, point):
        x1, y1 ,x2 ,y2 = line[0], line[1], line[2], line[3]
        x, y = point[0], point[1]
        line_equation = (y2 - y1) * (x - x1) - (x2 - x1) * (y - y1)
        if line_equation > 0:
            return +1
        elif line_equation < 0:
            return -1
        else:
            return 0
        
        
        
class Boomb(QWidget_):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.boombOn = False
        self.explodeFlag = False
        self.setWindowTitle('Boom')
        self.setGeometry(100,100,100,100)
        layout = QVBoxLayout()
        self.label = QLabel(self)
        self.label.setStyleSheet("background-color: red;")
        self.label.setText("BOOM!")
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.boombOner)
        self.timer.start(timeSpeed)
        
    def boombOner(self):
        
        if not self.boombOn:
            self.boombOn = True
            self.setLoc()
            self.setGeometry(DB["boomb"][0][0]-150, DB["boomb"][0][1] - 50, 350, 300)
            
        
        else:
            self.tikTacTok()
        
    def setLoc(self):
        fNum = random.randint(0, len(DB["floor"])-1)
        floor = DB["floor"][fNum]
        xLoc = random.randint(100, floor["size"][0] - 100)
        loc = (floor["location"][0] + xLoc, floor["location"][1] - 40)
        DB["boomb"] = [loc]
        
    def tikTacTok(self):
        if self.inBox((DB["player"]["location"][0], DB["player"]["location"][1]), DB["boomb"][0], DB["boombInfo"]["size"]):
            self.explode()
            
        if self.explodeFlag:
            
            if time.time() - self.now > 3:
                self.close()
                self.explodeFlag = False
                self.boombOn = False
                
                
            if self.inBox((DB["player"]["location"][0] + DB["player"]["size"], DB["player"]["location"][1] + DB["player"]["size"]), (self.pos().x(), self.pos().y()), (350, 300)):
                self.hitCompute()

    def inBox(self, point, loc, size):
        x, y = point
        if x > loc[0] and x < loc[0] + size[0]:
            if y > loc[1] and y < loc[1] + size[1]:
                return True  
        return False
    
    def explode(self):
        self.now = time.time()
        self.explodeFlag = True
        self.show()
        
    def hitCompute(self):
        global lastHit
        now = time.time()
        if now - lastHit >1:
            lastHit = now
            DB["player"]["heart"]-=1
        
    def paintEvent(self, event):
        pass
            

        



def on_key_press(key):
    global onA
    global onD
    if key == Key.esc:
        return False  # 이벤트 리스너 종료
    try:
        if key.char == 'a':
            onA=True
        if key.char == 'd':
            onD=True
            
            
        if key.char == 'w':
            if DB["player"]["onGround"] == True:
                DB["player"]["location"][1]-=1
                DB["player"]["onGround"] = False
                DB["player"]["gravity"][0] = -2

    except AttributeError:
        pass
    
def on_key_release(key):
    global onA
    global onD
    try:
        if key.char == 'a':
            onA=False
        if key.char == 'd':
            onD=False
    except AttributeError:
        pass



if __name__ == '__main__':
    end = GameOver()
    floor0 = Floor(DB["floor"][0])
    floor1 = Floor(DB["floor"][1])
    floor2 = Floor(DB["floor"][2])
    floor3 = Floor(DB["floor"][3])
    floor4 = Floor(DB["floor"][4])
    boss = Boss()
    boss.start_move_thread()
    player = Player()
    boomb = Boomb()
    
    listener = Listener(on_press=on_key_press, on_release=on_key_release) 
    listener.start()

    exit_code = app.exec_()
    listener.stop()
    sys.exit(exit_code)
