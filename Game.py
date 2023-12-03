import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
import random



timeSpeed=1
miliTime = timeSpeed/1000

desktop = QDesktopWidget().availableGeometry()


ground = 1350

DB={
    "player": {
        "location": [desktop.width()/2, desktop.height()/1.3],
        "size": 10,
        "lineColor":[0, 119, 182],
        "fillIn":[0,0,0],
        "speed":3*miliTime,
        "gravity": [0,2*miliTime]
        },
    
    }


class MainWindow(QWidget):
    
    #생성자 입니다
    def __init__(self):
        super().__init__()
        self.initUI()

    #이쪽이 메인입니다
    def initUI(self): 
        self.onGround = False
        #self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        desktop = QDesktopWidget().availableGeometry()
        self.monitor = [desktop.width(), desktop.height()] 
        self.setWindowTitle('메인 창')
        self.setGeometry(300, 300, 800, 500)
        self.move(self.pos().x(),desktop.height()/1.7)
        self.show()
        # Create a QTimer and connect it to a slot
        self.timer = QTimer(self)
        
        self.timer.timeout.connect(self.moveWindow)
        self.timer.timeout.connect(self.update)
        
        # Start the timer with a 1-second interval (1000 milliseconds)
        self.timer.start(timeSpeed)
              
    

    def moveWindow(self):
        DB["player"]["location"][1]+=DB["player"]["gravity"][0]
        if DB["player"]["location"][1] < ground:
            DB["player"]["gravity"][0]+=DB["player"]["gravity"][1]
        else:
            self.onGround = True
            DB["player"]["gravity"][0]
            DB["player"]["location"][1]=1350
                

        if self.pos().x()+200 >= DB["player"]["location"][0]:
            self.move(self.pos().x()-20, self.pos().y())
        if self.pos().x()+600 <= DB["player"]["location"][0]:
            self.move(self.pos().x()+20, self.pos().y())
            
            
            
            
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            DB["player"]["location"][0]-=10
        if event.key() == Qt.Key_D:
            DB["player"]["location"][0]+=10
        if event.key() == Qt.Key_W:
            DB["player"]["location"][1]-=10
        if event.key() == Qt.Key_S:
            DB["player"]["location"]["gravity"][1]=120
        if event.key() == Qt.Key_Space:
            if self.onGround==True:
                self.onGround=False
                DB["player"]["location"]["gravity"][0]=-30
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 안티앨리어싱 활성화
        pen = QPen(QColor(0, 0, 0))  # 선의 색상
        pen.setWidth(2)  # 선의 두께
        brush = QBrush(QColor(255, 0, 0, 127))  # 동그라미 내부의 색상

        painter.setPen(pen)
        painter.setBrush(brush)


        painter.drawEllipse(DB["player"]["location"][0]-self.pos().x(), DB["player"]["location"][1]- self.pos().y(), DB["player"]["size"]*2, DB["player"]["size"]*2)
        
        
        pen = QPen(QColor(255, 0, 0))  # 빨간색 선
        pen.setWidth(4)  # 선의 두께 설정
        painter.setPen(pen)

        # 선 그리기
        lineWhere = self.lineFollow(boss)
        painter.drawLine(lineWhere[0]-self.pos().x(), lineWhere[1]-self.pos().y(), 2000*lineWhere[2]-1999*lineWhere[0]-self.pos().x(), 2000*lineWhere[3]-1999*lineWhere[1]-self.pos().y())
        
        painter.setBrush(QColor(173, 216, 230))  # 직사각형 내부 색상 설정
        painter.setPen(QColor(0, 0, 0))  # 직사각형 테두리 색상 설정 (검정색)
        painter.drawRect(self.floorWhere(fl1)[0]-self.pos().x(), self.floorWhere(fl1)[1]-self.pos().y(), 500, 20)
    
       
   
    def lineFollow(self, anotherwindow):
        return anotherwindow.lineFollow(self)
    
    def floorWhere(self, flower):
        return flower.ego
        
        
        
class Boss1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    
    def initUI(self):
        self.speed=3    #here
        self.radius=10  # here
        self.radius=80
        desktop = QDesktopWidget().availableGeometry()
        self.ego=[desktop.width()/2-self.radius, desktop.height()/7]
        self.monitor = [desktop.width(), desktop.height()]
        self.setWindowTitle("Boss1's name")
        self.setGeometry(self.ego[0]-145, self.ego[1]-135,500, 500)
        self.show()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(timeSpeed)

    def paintEvent(self, event):
        self.ego[0]+=random.randint(-10, 10)
        self.ego[1]+=random.randint(-10, 10)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(0, 0, 0))
        pen = QPen(QColor(255, 0, 0))  # 빨간색 선
        pen.setWidth(4)  # 선의 두께 설정
        painter.setPen(pen)

        # 선 그리기
        #lineWhere = self.lineFollow(player)
        #painter.drawLine(lineWhere[0]-self.pos().x(), lineWhere[1]-self.pos().y(), lineWhere[2]-self.pos().x(), lineWhere[3]-self.pos().y())
        
        pen.setWidth(2)
        brush = QBrush(QColor(148, 0, 211))

        painter.setPen(pen)
        painter.setBrush(brush)

        # 동그라미를 창의 중심에 그립니다.
        center_x = self.width() // 2
        center_y = self.height() // 2
        #painter.drawEllipse(self.whereIs(self.ego)[0], self.whereIs(self.ego)[1], 2 * self.radius, 2 * self.radius)
        painter.drawEllipse(self.whereIs(self.ego)[0], self.whereIs(self.ego)[1], 2 * self.radius, 2 * self.radius)
        
       
    def currPoint(self):
        xSize,ySize=self.width(), self.height()
        x,y = self.pos().x(), self.pos().y()
        return [[x,y],[x,y+ySize],[x+xSize,y],[x+xSize,y+ySize]]
    
    def whereIs(self, arr):
        return [arr[0]-self.pos().x(),arr[1]-self.pos().y()]
    
    #def lineFollow(self,anotherWindow):
        #return [self.ego[0]+self.radius,self.ego[1]+self.radius, anotherWindow.ego[0], anotherWindow.ego[1]+anotherWindow.radius]
    
    
    
class Floor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    
    def initUI(self):
        self.ego = [300, 1220]
        desktop = QDesktopWidget().availableGeometry()
        self.monitor = [desktop.width(), desktop.height()]
        self.setWindowTitle('발판')
        self.setGeometry(250,1200, 600, 90)
        self.show()
    
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setBrush(QColor(173, 216, 230))  # 직사각형 색상을 빨간색으로 설정
        qp.setPen(QColor(0, 0, 0))
        qp.drawRect(self.ego[0]-self.pos().x(), self.ego[1]-self.pos().y(), 500, 20)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fl1 = Floor()
    boss = Boss1()
    player = MainWindow() 
    
    sys.exit(app.exec_())