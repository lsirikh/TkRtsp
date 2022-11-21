import tkinter as tk 

import cv2  
from PIL import Image
from PIL import ImageTk
import threading
import os
import time


class MainWindow():
    def __init__(self, window):
        self.set_properties(window)
        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)
        
    def set_properties(self, window):
        try:
            self.window = window
            self.label = tk.Label(self.window)
            self.label.grid(row=0, column=0, columnspan=2)
            self.runButton = tk.Button(self.window, 
                                overrelief="solid", 
                                text="Execute",
                                width=15, 
                                command=self.run_rtsp, 
                                #repeatdelay=1000, 
                                #repeatinterval=100
                                )
            self.stopButton = tk.Button(self.window, 
                                overrelief="solid", 
                                text="Stop",
                                width=15, 
                                command=self.stop_rtsp, 
                                #repeatdelay=1000, 
                                #repeatinterval=100
                                )

            self.runButton.grid(row=1, column=0)
            self.stopButton.grid(row=1, column=1)
            self.isRun = False
        except Exception as e:
            print("Raised Exception in set_properties : ", e)
    
    def set_rtsp_url(self, url):
        self.url = url
    
    def run_rtsp(self):
        print("Streaming Starts...")
        self.set_rtsp_frame()
        self.rtspThread = threading.Thread(target=self.update_image)
        self.rtspThread.start()
        
    def stop_rtsp(self):
        self.isRun = False
        if self.rtspThread.is_alive():
            self.rtspThread.join(3)

    def set_rtsp_frame(self):
        try:
            self.cap = cv2.VideoCapture(self.url)
            #self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            #self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            #self.cap.set(cv2.CAP_PROP_FPS, 5)
            self.isRun = True
        except Exception as e:
            print("Raised Exception in set_properties : ", e)
    
    def on_exit(self):
        print("Exit program")
        if self.isRun:
            self.stop_rtsp()
        self.window.destroy()
    
    def update_image(self):    
        prev_time = 0
        FPS = 5
        while self.isRun:
            try:
                ret, frame = self.cap.read()
                frame = cv2.resize(frame, (640, 480))
                current_time = time.time() - prev_time

                if (ret is True) and (current_time > 1./ FPS) :
                    prev_time = time.time()
                    # Get the latest frame and convert image format
                    self.OGimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # to RGB
                    self.OGimage = Image.fromarray(self.OGimage) # to PIL format
                    self.image = ImageTk.PhotoImage(self.OGimage) # to ImageTk format
                    # Update image
                    self.label.config(image=self.image)
                    self.label.image = self.image
            except Exception as e:
                print("Raised Exception in update_image : ", e)

if __name__ == "__main__":
    root = tk.Tk()
    window = MainWindow(root)
    #url = "rtsp://admin:Abc.12345@192.168.1.64:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
    #url = "rtsp://admin:Abc.12345@192.168.1.65:554/Streaming/channels/101"
    url = "rtsp://admin:sensorway1@192.168.202.119:554/Streaming/channels/101"
    window.set_rtsp_url(url) 
    root.mainloop()