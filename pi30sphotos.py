
import os
import sqlite3
from picamera import PiCamera
import time
import keyboard
import datetime as DT

connection=sqlite3.connect("Snailphotos.db")
connection.execute("CREATE TABLE IF NOT EXISTS piphoto(filename TEXT,path TEXT,status INTEGER);")
status =0 
camera=PiCamera()



try:
    while True:
            
            
            img_name="{}.jpg".format(str(DT.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            camera.resolution=(3072,2048)
            camera.capture(img_name)
            print("{} written".format(img_name))
            path=os.path.abspath(img_name)
            connection.execute(
                "INSERT INTO piphoto VALUES(?,?,?);",(img_name,path,status)
                )
            connection.commit()       
            time.sleep(30)
   
except KeyboardInterrupt:
    print("Exit")
    exit()

