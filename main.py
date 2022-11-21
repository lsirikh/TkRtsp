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
        
    def set_properties(self, window):
        try:
            self.window = window
        
            self.interval = 20 # Interval in ms to get the latest frame
            # Create canvas for image
            self.canvas = tk.Canvas(self.window, width=600, height=400)
            self.canvas.grid(row=0, column=0)
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

    def set_rtsp_frame(self):
        try:
            fpsLimit = 1 # throttle limit
            startTime = time.time()
            self.cap = cv2.VideoCapture(self.url)
            #self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            #self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            #self.cap.set(cv2.CAP_PROP_FPS, 5)
            # Update image on canvas
            self.isRun = True
            #self.update_image()
            #root.after(self.interval, self.update_image)
        except Exception as e:
            print("Raised Exception in set_properties : ", e)
    
    
    
    def update_image(self):    
        prev_time = 0
        FPS = 5
        while self.isRun:
            ret, frame = self.cap.read()
            frame = cv2.resize(frame, (640, 480))
            current_time = time.time() - prev_time

            # ret, img = self.cap.read()
            # img = cv2.resize(img, (720, 480))

            # if ret:
            #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
            #     h,w,c = img.shape
            #     qImg = QImage(img.data, w, h, w*c, QImage.Format_RGB888)
            #     pixmap = QPixmap.fromImage(qImg)
            #     self.label.setPixmap(pixmap)
            # else:
            #     raise Exception("Cannot read frame.")

            if (ret is True) and (current_time > 1./ FPS) :
                
                prev_time = time.time()
                # Get the latest frame and convert image format
                #self.OGimage = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
                self.OGimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # to RGB
                self.OGimage = Image.fromarray(self.OGimage) # to PIL format
                #self.image = self.OGimage.resize((600, 400))
                self.image = ImageTk.PhotoImage(self.OGimage) # to ImageTk format
                # Update image
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
                # Repeat every 'interval' ms
                #self.window.after(self.interval, self.update_image)
    
#def run_decoding(): 
    #os.system("ffmpeg -i rtsp://192.168.1.10?tcp -codec copy -f mpegts udp://127.0.0.1:5000 &")


if __name__ == "__main__":
    #my_cam = ONVIFCamera('192.168.1.10', 80, 'gemer.daniel@gmail.com', 'dg24111998')
    #media = my_cam.create_media_service()
    #ptz = my_cam.create_ptz_service()
    #media_profile = media.GetProfiles()[0]

    # Get PTZ configuration options for getting continuous move range
    #request = ptz.create_type('GetConfigurationOptions')
    #request.ConfigurationToken = media_profile.token
    #ptz_configuration_options = ptz.GetConfigurationOptions(request)

    #request = ptz.create_type('ContinuousMove')
    #request.ProfileToken = media_profile._token

    #ptz.Stop({'ProfileToken': media_profile._token})
    #p1 = threading.Thread(target=run_decoding)
    #p1.start()
    root = tk.Tk()
    window = MainWindow(root)
    url = "rtsp://admin:Abc.12345@192.168.1.64:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
    #url = "rtsp://admin:Abc.12345@192.168.1.65:554/Streaming/channels/101"
    window.set_rtsp_url(url) 
    root.mainloop()