import sys
import time
import numpy as np
from pynput.keyboard import Key, Listener
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtCore import Qt, QCoreApplication
import math


timeSpeed = 1
miliTime = timeSpeed / 1000
app = QApplication(sys.argv)
desktop = QDesktopWidget().screenGeometry()



onA = False
onD = False

DB = {
    "player": {
        "location": [int(desktop.width() / 2) - 10, int(desktop.height() / 1.3)],
        "size": 10,
        "lineColor": [0, 119, 182, 4],
        "fillIn": [0, 0, 0],
        "speed": 0.7,
        "gravity": [0, 9.8 * miliTime],
        "onGround": False,
    },
    
    "floor": [
        {
            "location": [150,1150],
            "size": [700,0],
            "lineColor": [0, 119, 182, 10],
            "fillIn": [],
        },
        
        {
            "location": [1750,1150],
            "size": [700,0],
            "lineColor": [0, 119, 182, 10],
            "fillIn": [],
        },
        
        {
            "location": [950,950],
            "size": [700,0],
            "lineColor": [0, 119, 182, 10],
            "fillIn": [],
        },
        
        {
            "location": [150,750],
            "size": [700,0],
            "lineColor": [0, 119, 182, 10],
            "fillIn": [],
        },
        
        {
            "location": [1750,750],
            "size": [700,0],
            "lineColor": [0, 119, 182, 10],
            "fillIn": [],
        },
        
        ],
    
    
    "ground": [
        [0, int(desktop.height() / 1.3) + 70]
    ],
    
    "boss": {
        "location": [int(desktop.width() / 2) - 30, int(desktop.height() / 7)],
        "size": 30,
        "lineColor":[0, 119, 182, 4],
        "fillIn":[0, 0, 0],
        },
    
    "laser": {
        "location":[0,0,0,0],
        "lineColor":[0, 119, 182, 2],
        "speed": 300,
        },
    
    
    
}



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


class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyRaid')
        self.setGeometry(DB["player"]["location"][0] - 350, DB["player"]["location"][1] - 200, 700, 350)
        self.show()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tikTacTok)
        self.timer.start(timeSpeed)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 안티앨리어싱 활성화
        
        
        for i in DB["floor"]:
            pen = QPen(QColor(i["lineColor"][0],i["lineColor"][1],i["lineColor"][2]))  # 선의 색상 (검정색)
            pen.setWidth(i["lineColor"][3])  # 선의 두께 설정
            painter.setPen(pen)

            painter.drawLine(i["location"][0]-self.pos().x(), i["location"][1]-self.pos().y() ,i["location"][0] + i["size"][0]-self.pos().x(), i["location"][1]+i["size"][1]-self.pos().y())  # 막대 그리기
            
        pen = QPen(QColor(DB["laser"]["lineColor"][0],DB["laser"]["lineColor"][1], DB["laser"]["lineColor"][2]))
        pen.setWidth(DB["laser"]["lineColor"][3])
        painter.setPen(pen)
        painter.drawLine(int(DB["laser"]["location"][0])-self.pos().x(), int(DB["laser"]["location"][1])-self.pos().y(), int(DB["laser"]["location"][2])-self.pos().x(), int(DB["laser"]["location"][3]))

        
        #동그라미 그리기
        pen = QPen(QColor(DB["player"]["lineColor"][0], DB["player"]["lineColor"][1], DB["player"]["lineColor"][2]))
        pen.setWidth(DB["player"]["lineColor"][3])
        brush = QBrush(QColor(DB["player"]["fillIn"][0], DB["player"]["fillIn"][1], DB["player"]["fillIn"][2]))
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(int(DB["player"]["location"][0]) - self.pos().x(), int(DB["player"]["location"][1]) - self.pos().y(), 2 * DB["player"]["size"], 2 * DB["player"]["size"])

    def tikTacTok(self):
        
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
        
            
        self.update()
        

class Floor(QWidget,):
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

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(self.floor["lineColor"][0], self.floor["lineColor"][1],self.floor["lineColor"][2]))  # 선의 색상 (검정색)
        pen.setWidth(self.floor["lineColor"][3])  # 선의 두께 설정
        painter.setPen(pen)

        painter.drawLine(self.floor["location"][0]-self.pos().x(), self.floor["location"][1]-self.pos().y() ,self.floor["location"][0] + self.floor["size"][0]-self.pos().x(), self.floor["location"][1]+self.floor["size"][1]-self.pos().y())  # 막대 그리기

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
            
        self.update()
        
        
    def isUndereGround(self):
        x,y = DB["player"]["location"][0], DB["player"]["location"][1]
        if x >= self.floor["location"][0] and x<= self.floor["location"][0]+self.floor["size"][0] and y>= self.floor["location"][1] - 2*DB["player"]["size"]:
            return True
        return False
    
class Boss(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    
    def initUI(self):
        self.onHit = False
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
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(DB["boss"]["lineColor"][0],DB["boss"]["lineColor"][1], DB["boss"]["lineColor"][2]))
        pen.setWidth(DB["boss"]["lineColor"][3])  # 선의 두께 설정
        painter.setPen(pen)
        painter.drawEllipse(DB["boss"]["location"][0]-self.pos().x(),DB["boss"]["location"][1]-self.pos().y(), 2*DB["boss"]["size"], 2*DB["boss"]["size"])
        
        pen = QPen(QColor(DB["laser"]["lineColor"][0],DB["laser"]["lineColor"][1], DB["laser"]["lineColor"][2]))
        pen.setWidth(DB["laser"]["lineColor"][3])
        painter.setPen(pen)
        painter.drawLine(int(DB["laser"]["location"][0])-self.pos().x(), int(DB["laser"]["location"][1])-self.pos().y(), int(DB["laser"]["location"][2])-self.pos().x(), int(DB["laser"]["location"][3]))

    def tikTacTok(self):
        self.laser()
        self.attack1()
        self.update()
        pass
    
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
        now = time.time()
        now = (now- self.debounceTimer) % 10
        if now < 3: #따라다니기    
            self.laserOn = True
        elif now < 3.5: #잠깐 꺼지기
            self.laserOn = False
            if DB["laser"]["location"] !=[0,0,0,0]:
                self.temp = DB["laser"]["location"]
            DB["laser"]["location"] = [0,0,0,0]
        elif now < 7: #쏘기
            self.laserOn = False
            if self.locOn()[2]  < self.temp[2]:
                print(self.circular(self.temp, -1))
                self.temp[2], self.temp[3] = self.circular(self.temp, 0.033)
            else:
                print(self.circular(self.temp, -1))
                self.temp[2], self.temp[3] = self.circular(self.temp, -0.033)
                
            DB["laser"]["location"] = self.temp
            if  DB["laser"]["lineColor"][3] < 60:
                DB["laser"]["lineColor"][3] +=1
            
            if distance(DB["player"]["location"], self.temp) < 60 - DB["player"]["size"]:
                self.onHit = True
                print("맞았습니다")
            
        else: #꺼지기
            DB["laser"]["lineColor"][3] = 2
            self.laserOn = False
            DB["laser"]["location"] = [0,0,0,0]
        
        
   



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
    floor0 = Floor(DB["floor"][0])
    floor1 = Floor(DB["floor"][1])
    floor2 = Floor(DB["floor"][2])
    floor3 = Floor(DB["floor"][3])
    floor4 = Floor(DB["floor"][4])
    boss = Boss()
    player = Player()
    listener = Listener(on_press=on_key_press, on_release=on_key_release) 
    listener.start()

    exit_code = app.exec_()
    listener.stop()
    sys.exit(exit_code)
