import tkinter as tk 

import cv2  
from PIL import Image
from PIL import ImageTk
import threading
import os

class MainWindow():
    def __init__(self, window):
        self.set_properties(window)
        
    def set_properties(self, window):
        try:
            self.window = window
        
            self.interval = 3 # Interval in ms to get the latest frame
            # Create canvas for image
            self.canvas = tk.Canvas(self.window, width=600, height=400)
            self.canvas.grid(row=0, column=0)
            self.button = tk.Button(self.window, 
                                overrelief="solid", 
                                text="Execute",
                                width=15, 
                                command=self.run_rtsp, 
                                repeatdelay=1000, 
                                repeatinterval=100)
            self.button.grid(row=1, column=0)
        except Exception as e:
            print("Raised Exception in set_properties : ", e)
    
    def set_rtsp_url(self, url):
        self.url = url
        
    def run_rtsp(self):
        print("Streaming Starts...")
        self.set_rtsp_frame()

    def set_rtsp_frame(self):
        try:
            self.cap = cv2.VideoCapture(self.url)
            self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            
            # Update image on canvas
            root.after(self.interval, self.update_image)
        except Exception as e:
            print("Raised Exception in set_properties : ", e)
    
    
    
    def update_image(self):    
            
        # Get the latest frame and convert image format
        self.OGimage = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
        self.OGimage = Image.fromarray(self.OGimage) # to PIL format
        self.image = self.OGimage.resize((600, 400), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image) # to ImageTk format
        # Update image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        # Repeat every 'interval' ms
        self.window.after(self.interval, self.update_image)
    
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
    window.set_rtsp_url(url) 
    url = "rtsp://admin:Abc.12345@192.168.1.65:554/Streaming/channels/101"
    root.mainloop()