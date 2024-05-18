# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 10:43:14 2023

@author: SKAN
"""


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import os
import signal
from picamera import PiCamera


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
      
        self.initUI()
       

    def initUI(self):
        self.setWindowTitle("Snail Live Camera")
        self.showMaximized()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        
       
        self.start_button = QPushButton("Start Preview")
        self.start_button.setIcon(QIcon('/home/dataeffects/snail/files/icons/start.png'))
        self.start_button.clicked.connect(self.start_video)
        self.start_button.setIconSize(1*(QSize(37,37)))
        self.start_button.setStyleSheet("background-color:white;color:black; font: bold 20px Courier;")
        
        self.pixmap = QPixmap('/home/dataeffects/snail/files/icons/no-video.png')
        
        self.stop_button = QPushButton("Stop Preview")
        self.stop_button.setIcon(QIcon('/home/dataeffects/snail/files/icons/stop1.png'))
        self.stop_button.setIconSize(1*(QSize(30,30)))
        self.stop_button.clicked.connect(self.stop_video)
        self.stop_button.setEnabled(True)
        self.stop_button.setStyleSheet("background-color: white;color:black;font:bold 20px Courier;")
        
      
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setPixmap(self.pixmap)
        self.video_label.setMinimumSize(640, 480)

      
        self.vbox2 = QVBoxLayout()
        self.vbox2.addWidget(self.video_label)
        
        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.start_button)
        self.vbox1.addWidget(self.stop_button)
        
        self.group_box1 = QGroupBox("", self)
        self.group_box1.setStyleSheet("background-color: black;")
        self.group_box1.setFixedSize(250, 100)
        self.group_box1.setLayout(self.vbox1)
  
        self.group_box2 = QGroupBox("Camera Preview", self)
        self.group_box2.setStyleSheet("background-color: white; color:black")
     
        self.group_box2.setLayout(self.vbox2)
        
       
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.group_box1)
        self.hbox.addWidget(self.group_box2)
       
        self.setLayout(self.hbox)
        

        self.camera = PiCamera()
        
        self.camera.resolution=(3072,2048)
     
        self.video_playing = False
        self.video_paused = True
        
       
        
        
    def start_video(self):
        os.system("sudo systemctl stop snail_capture.service")
       
        self.video_paused = not self.video_paused
        if (self.start_button.text() == "Start Preview"):
            self.start_button.setText("Pause")
            self.start_button.setIcon(QIcon("/home/dataeffects/snail/files/icons/pause.png"))
            x=self.video_label.geometry().x()
   
            
            self.camera.resolution=(3840,2160)
            self.camera.start_preview(fullscreen=False)
           
            self.camera.start_preview(fullscreen=False,window=(self.video_label.mapToGlobal(QPoint(0,0)).x(),self.video_label.mapToGlobal(QPoint(0,0)).y(),self.video_label.width(),self.video_label.height()))
            
            self.video_playing = True
            
        else:
            self.start_button.setText("Start Preview")
            self.start_button.setIcon(QIcon("/home/dataeffects/snail/files/icons/start.png"))
            self.camera.stop_preview()
            

 
    def stop_video(self):
        self.camera.stop_preview()
        os.system("sudo systemctl start snail_capture.service")
        self.close()
        sys.exit(1)
        
    def closeEvent(self,event):
        self.camera.stop_preview()
        print("inside signal_exit")
        os.system("sudo systemctl start snail_capture.service")
        self.close()
        sys.exit(1)
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    myapp.showMaximized()   
    myapp.setStyleSheet("background-color : black;"
                        "QPushButton"
                          "{"
                          "background-color : white;"
                          
                          "border-style: outset;"
                         "border-width: 1px;"
                         "border-radius: 10px;"
                          "border-color: black;"
                          "font: Courier ;"
                          "padding:1px;"
                          "min-width: 10em;"
                          "padding: 6px;"
                          

                         
                          "}"
                           "QPushButton::pressed"
                           "{"
                           "background-color : beige;"
                           "}"
                           "QGroupBox { border: 2px solid gray; border-style:outset ;}"
                           
                           "QVBoxLayout { background-color :black;}")
    sys.exit(app.exec_())
