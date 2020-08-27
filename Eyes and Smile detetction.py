import numpy as np
import cv2
import time
#import opencv-contrib



face_cascade = cv2.CascadeClassifier("C:/Users/Prakash/Desktop/Python_/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("C:/Users/Prakash/Desktop/Python_/haarcascade_eye.xml")
#mouth_cascade = cv2.CascadeClassifier("C:/Users/Prakash/Desktop/Python_/haarcascade_mouth.xml")
smile_cascade = cv2.CascadeClassifier("C:/Users/Prakash/Desktop/Python_/haarcascade_smile.xml")



Vidcap = cv2.VideoCapture(0)  #to capture from video ('sources filelink instead of 0')


fourcc = cv2.VideoWriter_fourcc(*'XVID') #defining the code to save the videowriter #newly added
output = cv2.VideoWriter('here_filename.avi',fourcc, 20.0, (640,480)) # captured video source, video width and height


check,frame = Vidcap.read()

while (Vidcap.isOpened()):              #:  #instead of 1, here i have added Vidcap.isOpened--> returns False
    ret, frame = Vidcap.read()
    if ret ==True:  
        frame = cv2.flip(frame, 1) # if frame is 0, videoframe rotates to upside down
        output.write(frame) 
        
        
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #to capture in monochrome
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
    
     
    for (x,y, w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
        
        roi_gray = gray[y:y-int((y+h)*0.7), x:x+w]  #for avoiding mouth considering as eyes so region of interest more than 80%
        roi_color = frame[y:y-int((y+h)*0.7), x:x+w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray)
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.4, 20) #by testing all the value from 1.1-1.9, 1.6 was the best one
        
        for (ex,ey,ew,eh) in eyes:    #bounding box for eye detection
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            
            for (sx, sy, sw, sh) in smiles: #bounding box for smile detection 
                cv2.rectangle(roi_color,(sx, sy),((sx + sw), (sy + sh)), (0,0,255), 2)
                          

    k = cv2.waitKey(25) #how a frame for specified no. of milliseconds. returns either code of pressed key or -1.
    print("the value of k is " + str(k)) ## check if the return value of waitkey() is a number if yes. if k>0 means some key was pressed. 
    if int(k) == 97: # if you press "a" then close.
        break
    #else:  #newly added
        #break #newly added
        
    cv2.imshow('frame',frame)  #Displaying the output

print(check)
print(frame)

time.sleep(3) # captures images for 3 seconds after pressing the stop button
#cv2.imshow('frame', frame) # newly added

output.release 
Vidcap.release()  #with no release function camera may not be free for another purposes
cv2.destroyAllWindows()
Vidcap.stop() ## TODO: stop the cam