import cv2
import numpy as np
import os
import math

import socket
import sys
from thread import *
import json

from bottle import run, route, request

json_data = {}
command = 0
command_recv = 1

@route('/getdata', method=['GET', 'POST'])
def getdata():
    global json_data
    global command
    global command_recv
    if request.method == 'GET':
        if command_recv == 1:
            json_data.update({"command": int(command)})
            data = json.dumps(json_data)
        elif command_recv == 0:
            data = json.dumps(json_data)
        return data+'\r'
    elif request.method == 'POST':
        print request.body.read()
        try:
            command = int(json.loads(str(request.body.read()))['command'])
            command_recv = 1
        except:
            print "Bad structure in POSTed data"
        return "OK"


###################################################################################################
def main():
    global json_data
    prev_x = [-1, -1, -1, -1]     #storing previous x_coordinates in a list prev_x
    prev_y = [-1, -1, -1, -1]     #storing previous y_coordinates in a list prev_y
    prev_ang = [-1, -1, -1, -1]     #storing previous angle_coordinates in a list prev_ang

    capWebcam = cv2.VideoCapture(1)  # declare a VideoCapture object and associate to webcam, 0 => use 1st webcam

    if capWebcam.isOpened() == False:  # check if VideoCapture object was associated to webcam successfully
        print "error: capWebcam not accessed successfully\n\n"  # if not, print error message to std out
        os.system("pause")  # pause until user presses a key so user can see error message
        return  # and exit function (which exits program)

    while cv2.waitKey(1) != 27 and capWebcam.isOpened():  # until the Esc key is pressed or webcam connection is lost
        blnFrameReadSuccessfully, imgOriginal = capWebcam.read()  # read next frame

        if not blnFrameReadSuccessfully or imgOriginal is None:  # if frame was not read successfully
            print "error: frame not read from webcam\n"  # print error message to std out
            os.system("pause")  # pause until user presses a key so user can see error message
            break  # exit while loop (which exits program)

        imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)
        #imgHSV = cv2.fastNlMeansDenoisingColored(imgHSV,None,3,3,5,15)
        list_x = [0.0, 0.0, 0.0, 0.0]    #storing current x_coordinates in a list list_x
        list_y = [0.0, 0.0, 0.0, 0.0]    #storing current y_coordinates in a list list_y
        list_ang = [0.0, 0.0, 0.0, 0.0]    #storing current angle_coordinates in a list list_ang

        for i in range(1, 5):

            if i==1:
                imgThresh1low = cv2.inRange(imgHSV, (0, 75, 150), (12, 220, 255))      # Since Red color is on the boundary line Hue=0
                imgThresh1high = cv2.inRange(imgHSV, (170, 75, 150), (180, 255, 255))   # We have to set 2 threshold masks and
                imgThresh = cv2.add(imgThresh1low, imgThresh1high)                       # Add them
            elif i==2:
                imgThresh = cv2.inRange(imgHSV, (60, 10, 180), (95, 110, 255))           # Setting threshold for cyan color
            elif i==3:
                imgThresh = cv2.inRange(imgHSV, (95, 70, 100), (130, 255, 255))          # Setting threshold for Blue color
            elif i == 4:
                imgThresh = cv2.inRange(imgHSV, (0, 0, 180), (180, 10, 255))            # Setting threshold for white color
            #elif i==5:
             #   imgThresh = cv2.inRange(imgHSV, (50, 0, 0), (70, 255, 255))              # Green
            #elif i==6:
             #   imgThresh = cv2.inRange(imgHSV, (140, 55, 55), (160, 255, 255))          # Magenta

                #imgThresh = cv2.GaussianBlur(imgThresh, (5, 5), 0)        # Gaussian blur for noise reduction
                imgThresh = cv2.medianBlur(imgThresh, 9)             #Median blur for redcuing the salt and pepper noise
                #imgThresh = cv2.bilateralFilter(imgThresh, 5, 75, 75)        #Bilateral filter for reducing noise
            ret3, imgThresh = cv2.threshold(imgThresh, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # blur
            image, contours, hierarchy = cv2.findContours(imgThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # finding contours and storing in contours list

            #print(len(contours))

            if len(contours) < 1:             # condition: if length of the contours is less than 1 then break the for loop
              break

            def smaller(a, b):       # function definition for sorting
              areaA = cv2.contourArea(a)    # based on the area of contour
              areaB = cv2.contourArea(b)
              if areaA > areaB:
                return -1
              if areaA == areaB:
                return 0
              else:
                return 1

            contours.sort(smaller)  # sorting contours based on its area

            cnt = contours[0]       # taking the largest contour
            rect0 = cv2.minAreaRect(cnt)    #setting minimum bounding area rectangle on the contour
            box = cv2.boxPoints(rect0)     #storing the cente,dimensions and R_angle in rect_0
            box = np.int0(box)          #R_angle: angle w.r.t bounding rectangle,rect_0[0] stores centre coordinates

            if i == 1:
                cv2.drawContours(imgOriginal, [box], 0, (0,0,255),2)                  #Drawing Red boundaries on the largest Red object
            elif i == 2:
                cv2.drawContours(imgOriginal, [box], 0, (255, 255, 0), 2)             #Drawing Green boundaries on the largest Green object
            elif i == 3:
                cv2.drawContours(imgOriginal, [box], 0, (255, 0, 0), 2)               #Drawing Blue boundaries on the largest Blue object
            elif i == 4:
                cv2.drawContours(imgOriginal, [box], 0, (255,255,255), 2)             #Drawing White boundaries on the largest White object

            elif i == 5:
               cv2.drawContours(imgOriginal, [box], 0, (0, 255, 0), 0)
            elif i == 6:
                cv2.drawContours(imgOriginal, [box], 0, (255,0,255),0)


            if len(contours)!=1:                                                 #if more than 1 contour is present

                cnt = contours[1]                 #taking the 2nd largest contour
            rect1 = cv2.minAreaRect(cnt)      #setting minimum bounding area rectangle on the contour
            box = cv2.boxPoints(rect1)       #storing the cente,dimensions and R_angle in rect_1
            box = np.int0(box)            #R_angle: angle w.r.t bounding rectangle,rect_1[0] stores centre coordinates

           #   cv2.drawContours(imgThresh, [box], 0, (255, 255, 255), 10)
              #[vx, vy, X, Y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)

            if i == 1:
                cv2.drawContours(imgOriginal, [box], 0, (0,0,255),2)                  #Drawing Red boundaries on the 2nd largest Red object
            elif i == 2:
                cv2.drawContours(imgOriginal, [box], 0, (255, 255, 0), 2)             #Drawing Green boundaries on the 2nd largest Green object
            elif i == 3:
                cv2.drawContours(imgOriginal, [box], 0, (255, 0, 0), 2)               #Drawing Blue boundaries on the 2nd largest Blue object
            elif i == 4:
                cv2.drawContours(imgOriginal, [box], 0, (255,255,255), 2)             #Drawing White boundaries on the 2nd largest White object
            elif i == 5:
                cv2.drawContours(imgOriginal, [box], 0, (0, 255, 0), 0)
            elif i == 6:
                  cv2.drawContours(imgOriginal, [box], 0, (255, 0, 255),0)

            """if i == 1:  # to get all colors in 1 window
                ImgThresh = imgThresh
            else:
                ImgThresh = ImgThresh + imgThresh"""

            if rect1[0][0] > rect0[0][0]:           #if x_coord of largest contour > x_coord of 2nd largest contour : 1st and 4th coordinate
                angle=math.atan((rect1[0][1] - rect0[0][1]) / (rect1[0][0] - rect0[0][0])) * 57.32          #then angle found is direct angle

            elif rect1[0][0] < rect0[0][0]:         #if x_coord of largest contour > x_coord of 2nd largest contour : 2nd and 3rd coordinate

                if (math.atan((rect1[0][1] - rect0[0][1]) / (rect1[0][0] - rect0[0][0])) * 57.32) > 0:         #if line lies in 2nd coordinate angle lies between 90 and 180
                    angle=(math.atan((rect1[0][1] - rect0[0][1]) / (rect1[0][0] - rect0[0][0])) * 57.32) - 180#so we subtract with 180, this makes angle to lie between -90 and 0

                else:                                                                                        #if line lies in 3rd coordinate angle lies between -90 and -180
                    angle=180 + (math.atan((rect1[0][1] - rect0[0][1]) / (rect1[0][0] - rect0[0][0])) * 57.32) #so we add 180 to make this angle lie between 0 and 90

            elif (rect1[0][0] == rect0[0][0]) and (rect1[0][1] > rect0[0][1]):                     #we have to write +90 and -90 angle cases seperately because 
                    angle=90                                                                       #the denominator in the above lines become zero 

            elif (rect1[0][0] == rect0[0][0]) and (rect1[0][1] < rect0[0][1]):
                angle= -90


            if len(contours)==1:                                                  #if only one contour is there
                [vx, vy, X, Y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)     #we are using inbuilt function to find the slope of the line
                angle = math.atan(vy/vx)*57.32

            dist=(rect0[0][0]-rect1[0][0])**2+(rect0[0][1]-rect1[0][1])**2        # we are finding distance between two points
            dist=math.sqrt(dist)

            if (cv2.contourArea(contours[0])>100 and dist<80.0):
              list_x[i-1]= rect0[0][0]                                         #storing x-coordinates into a list
              list_y[i-1]=480 - rect0[0][1]                                         #storing y-coordinates into a list
              list_ang[i-1]= angle                                             #storing orientation into a list

            else:
              list_x[i - 1] = -1                                               # if no color is present with minimum 100 units of area then coordinates are marked as -1
              list_y[i - 1] = -1                                               # and angle as zero
              list_ang[i - 1] = -1

            #CHANGE
            #filtering readings

            if (list_x[i-1]!=-1):                                             # updating the coordinates once iteration is complete
                prev_x[i-1]=list_x[i-1]
            if (list_y[i-1]!=-1):
                prev_y[i-1]=list_y[i-1]

            if (list_ang[i-1]!=-1):                                           #updating the angle once iteration is complete
                prev_ang[i-1]=list_ang[i - 1]

        """  if (prev_x[i - 1] != -1 and abs(list_x[i-1]-prev_x[i-1])>30):
                        list_x[i - 1] =  int(prev_x[i - 1] + list_x[i-1])/2
                    if (prev_y[i - 1] != -1 and  abs(list_y[i - 1] - prev_y[i - 1]) > 30):
                        list_y[i - 1] = int ( prev_y[i - 1] + list_y[i-1])/2
                    if (prev_ang[i - 1] != -1 and abs(list_ang[i - 1] - prev_ang[i - 1]) > 30):
                        list_ang[i - 1] =  prev_ang[i - 1]"""

        if len(contours) < 1:                                                  # this line takes us to the begining of the while loop if there are no contours
            continue

        # totallist = list_x+list_y+list_ang                                   #concatenating all 3 lists
        json_data.update({'xdata': list_x, 'ydata': list_y, 'angle': list_ang})

        json_data2 = json_data
        for key in json_data.keys():
            if not key == "command":
               json_data2.update({key: [int(a) for a in json_data[key]]})

        json_data.update(json_data2)

        print json_data
        # print data
        #print totallist
        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
#         totaltuple = tuple(totallist)                                        #converting list into tuple
#         print(totaltuple)

        #   cv2.imshow("Contour", imgThresh)                                     #this gives contours of magenta since i=6 for magenta

        #cv2.imshow("Contour", ImgThresh)
        cv2.imshow("imgOriginal", imgOriginal)  # show windows
        cv2.namedWindow("imgOriginal",cv2.WINDOW_AUTOSIZE)  # create windows, use WINDOW_AUTOSIZE for a fixed window size
       # cv2.namedWindow("Contour", cv2.WINDOW_AUTOSIZE)  # or use WINDOW_NORMAL to allow window resizing

    # end while

    cv2.destroyAllWindows()  # remove windows from memory

    return


###################################################################################################
# if __name__ == "__main__":
start_new_thread(main, ())
# clientthread()
run(host='0.0.0.0', port=8080)
