#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
import urllib
import urllib.request
import matplotlib.animation as animation
import pandas
from matplotlib import style


#REF_HEIGHT = 120;

#it will work better from python idle or pycharm

plt.style.use('fivethirtyeight')
fig1=plt.figure()#figure 1

ax1=fig1.add_subplot(1,1,1)#axis 1 from figure 1

def animate(p):#shouldn't match with the animation library present
    plot_data=open('datau.txt','r').read()
    line_data=plot_data.split('\n')#it will take data to new line
    x1=[]
    y1=[]

    #empty dictonaries to record data

    for line in line_data:
        if len(line)>1: #Means there must be some data
            x,y=line.split(',')#we dont need the , present in the file
            x1.append(float(x))
            y1.append(float(y))


        ax1.clear()
        ax1.plot(x1,y1)


def main():    
    a = 0
    b = 0
    t = 0
    const = 13.5  
    with open('datau.txt', 'w') as outfile:
        outfile.write("0,0")
        
    url='http://192.168.0.110:8080/shot.jpg'
    #imgResp=urllib.urlopen("http://192.168.0.3:8080/shot.jpg")
    while True:
        imgResp=urllib.request.urlopen(url)
        imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
        frame = cv2.imdecode(imgNp, -1)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        l_r = np.array([0, 120, 70])
        u_r = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, l_r, u_r)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        print("Number of contours = " + str(len(contours)))
        
        for c in contours:
            # calculate moments for each contour
            M = cv2.moments(c)
         
            # calculate x,y coordinate of center
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0
            #print(a, b)
            distance = math.sqrt((cX-a)*(cX-a) + (cY-b)*(cY-b))
            
            height = distance/const
             
            a = cX
            b = cY
                           
            cv2.circle(hsv, (cX, cY), 5, (255, 255, 255), -1)
            
            cv2.putText(hsv, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                            (255, 255, 255), 2)
            
        if(len(contours)==2):
            t=t+1
            with open('datau.txt', 'a') as outfile:
                outfile.write("\n"+str(t)+","+str(height))
            #anime_data=animation.FuncAnimation(fig1, animate, interval=500)     
            #interval is in milisecond
            #plt.show()
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
        cv2.drawContours(hsv, contours, -1, (0, 255, 0), 3)
        
        
        cv2.imshow('Live Feed', frame)
        cv2.imshow('RED feed', hsv)
        if cv2.waitKey(1)==27 or t == 25:
            break
        
    cv2.destroyAllWindows() 
    anime_data=animation.FuncAnimation(fig1, animate, interval=500)
    plt.show()
if __name__ == "__main__":
    main()
