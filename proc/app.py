from ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor,QPen,QFont
from proc import *
import time

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

class DrawCPU(QtWidgets.QWidget):
    def __init__(self,cpu_data):
        super(DrawCPU,self).__init__()
        self.cpu_data=cpu_data
        self.colors=[QColor(255,160,90),QColor(255,100,90),QColor(200,200,200),QColor(100,100,100)]

    def paintEvent(self,event):
        painter=QtGui.QPainter()
        painter.begin(self)
        self.draw_cpus(painter)
        painter.end()

    def draw_cpus(self,painter):
        cpus=self.cpu_data[0]
        cpus=sorted(cpus.items(),key=lambda x:x[0])
        text_font=QFont()
        text_font.setPointSize(20)
        text_font.setItalic(True)
        for i in range(len(cpus)-1):
            painter.setPen(QPen(QColor(100,120,30),2))
            painter.setBrush(self.colors[i]);
            painter.drawRect(20,i*80+20,100,60)
            painter.setPen(QColor(110,50,50))
            painter.setFont(text_font)
            str_text="{0} : {1:.2%}".format(cpus[i+1][0],cpus[i+1][1])
            painter.drawText(130,i*80+60,str_text)


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
        pass

    def load_process_infor(self,infor):
        pass


if __name__ == '__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    management=Manager()
    management.show()
    sys.exit(app.exec_())
