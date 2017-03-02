from ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor,QPen,QFont
from proc import *
import time
import random

class CPU(QtCore.QThread):
    _cpu_infor_signal=QtCore.pyqtSignal(dict)
    def __init__(self):
        super(CPU,self).__init__()

    def run(self):
        for result in get_cpu_infor():
            self._cpu_infor_signal.emit(result)
            time.sleep(1)

class Memory(QtCore.QThread):
    _mem_infor_signal=QtCore.pyqtSignal(dict)
    def __init__(self):
        super(Memory,self).__init__()

    def run(self):
        while True:
            infor=get_memory_infor()
            self._mem_infor_signal.emit(infor)
            time.sleep(1)

class Process(QtCore.QThread):
    _proc_infor_signal=QtCore.pyqtSignal(list)
    def __init__(self):
        super(Process,self).__init__()

    def run(self):
        while True:
            infor=get_process_infor()
            self._proc_infor_signal.emit(infor)
            time.sleep(1)

class Network(QtCore.QThread):
    _net_infor_signal=QtCore.pyqtSignal(dict)
    def __init__(self):
        super(Network,self).__init__()

    def run(self):
        for infor in get_network_infor():
            self._net_infor_signal.emit(infor)
            time.sleep(1)

class DrawMemory(QtWidgets.QWidget):
    def __init__(self,mem_infor):
        super(DrawMemory,self).__init__()

    def paintEvent(self,event):
        painter=QtGui.QPainter()
        painter.begin(self)
        self.draw_mem(painter)
        painter.end()

    def draw_mem(self,painter):
        pass

class DrawNetwork(QtWidgets.QWidget):
    def __init__(self,network_data):
        super(DrawNetwork,self).__init__()
        self.network_data=network_data
        self.colors=[QColor(255,160,90),QColor(255,100,90),QColor(200,100,200),QColor(100,100,100)]

    def paintEvent(self,event):
        painter=QtGui.QPainter()
        painter.begin(self)
        self.draw_network(painter)
        painter.end()

    def draw_network(self,painter):
        net_now=self.network_data[0]
        text_font=QFont()
        text_font.setPointSize(10)
        text_font.setItalic(True)
        for i in range(2):
            painter.setPen(QPen(QColor(100,120,30),2))
            painter.setBrush(self.colors[i]);
            painter.drawRect(30+i*300,400,80,40)
        for key in net_now:
            if key=='lo':
                continue
            painter.setPen(QColor(50,50,50))
            painter.setFont(text_font)
            download=(net_now[key][0]/1024)/1024
            painter.drawText(115,415,"已下载:%.2f MB"%download)
            download_speed=net_now[key][2]
            painter.drawText(115,435,"Speed:%.2f KB/s"%download_speed)
            up=(net_now[key][2]/1024)/1024
            up_speed=net_now[key][3]
            painter.drawText(415,415,"已上传:%.2f MB"%up)
            painter.drawText(415,435,"Speed:%.2f KB/s"%up_speed)
            break
        painter.setPen(QColor(50,50,50))
        painter.drawLine(30,30,30,330)
        painter.drawLine(30,330,630,330)
        length=len(self.network_data[:40])
        for i in range(length-1):
            for key in self.network_data[i]:
                if key=='lo':
                    continue
                painter.setPen(QPen(self.colors[0],2))
                try:
                    y1=330-(self.network_data[i][key][2]/2048)*300
                except:
                    y1=320
                try:
                    y2=330-(self.network_data[i+1][key][2]/2048)*300
                except:
                    y2=320
                painter.drawLine(i*15+30,y1,i*15+45,y2)

                painter.setPen(QPen(self.colors[1],2))
                try:
                    y1=330-(self.network_data[i][key][3]/3072)*300
                except:
                    y1=320
                try:
                    y2=330-(self.network_data[i+1][key][3]/3072)*300
                except:
                    y2=320
                painter.drawLine(i*15+30,y1,i*15+45,y2)

class DrawCPU(QtWidgets.QWidget):
    def __init__(self,cpu_data):
        super(DrawCPU,self).__init__()
        self.cpu_data=cpu_data
        self.colors=[QColor(255,160,90),QColor(255,100,90),QColor(200,100,200),QColor(100,100,100)]

    def paintEvent(self,event):
        painter=QtGui.QPainter()
        painter.begin(self)
        self.draw_cpus(painter)
        painter.end()

    def draw_cpus(self,painter):
        cpus=self.cpu_data[0]
        cpus=sorted(cpus.items(),key=lambda x:x[0])
        cpus=cpus[1:]
        length=len(cpus)
        width=int(750/length)
        text_font=QFont()
        text_font.setPointSize(20-2*length)
        text_font.setItalic(True)
        line_colors={}
        for i in range(length):
            painter.setPen(QPen(QColor(100,120,30),2))
            painter.setBrush(self.colors[i]);
            if cpus[i][0] not in line_colors:
                line_colors[cpus[i][0]]=self.colors[i]
            painter.drawRect(i*(width)+30,400,50,30)
            painter.setPen(QColor(110,50,50))
            painter.setFont(text_font)
            str_text="{0} : {1:.2%}".format(cpus[i][0],cpus[i][1])
            painter.drawText(i*(width)+30,450,str_text)
        painter.setPen(QColor(50,50,50))
        painter.drawLine(30,30,30,330)
        painter.drawLine(30,330,630,330)
        data_length=len(self.cpu_data[:40])
        for i in range(data_length):
            if i==data_length-1:
                break
            for cpu in self.cpu_data[i]:
                if cpu=='cpu':
                    continue
                color=line_colors[cpu]
                painter.setPen(QPen(color,2))
                try:
                    y1=330-self.cpu_data[i][cpu]*300
                except:
                    y1=320
                try:
                    y2=330-self.cpu_data[i+1][cpu]*300
                except:
                    y2=320
                painter.drawLine(i*15+30,y1,i*15+45,y2)

class Manager(Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self):
        super(Manager,self).__init__()
        self.setupUi(self)
        self.cpu=CPU()
        self.memory=Memory()
        self.process=Process()
        self.network=Network()
        self.init_signal()
        self.cpu_data=[]
        self.mem_data=[]
        self.pro_data=[]
        self.net_data=[]

    def init_signal(self):
        self.cpu._cpu_infor_signal.connect(self.load_cpu_infor)
        self.cpu.start()
        self.memory._mem_infor_signal.connect(self.load_memory_infor)
        self.memory.start()
        self.process._proc_infor_signal.connect(self.load_process_infor)
        self.process.start()
        self.network._net_infor_signal.connect(self.load_network_infor)
        self.network.start()
        self.actionExit.triggered.connect(self.close)

    def load_cpu_infor(self,infor):
        try:
            del self.draw_cpu
        except:
            pass
        self.cpu_data.insert(0,infor)
        self.draw_cpu=DrawCPU(self.cpu_data)
        self.cpu_gridLayout.addWidget(self.draw_cpu,0,0)

    def load_memory_infor(self,infor):
        pass

    def load_network_infor(self,infor):
        try:
            del self.draw_net
        except:
            pass
        self.net_data.insert(0,infor)
        self.draw_net=DrawNetwork(self.net_data)
        self.net_gridLayout.addWidget(self.draw_net,0,0)

    def load_process_infor(self,infor):
        pass


if __name__ == '__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    management=Manager()
    management.show()
    sys.exit(app.exec_())
