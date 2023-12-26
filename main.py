from PIL import Image
import cv2
import numpy
import sys


import os
color_red = (0,0,255)
color_green = (0,255,0)
video = cv2.VideoCapture('metall.mp4')

# We need to check if camera
# is opened previously or not
if (video.isOpened() == False):
    print("Error reading video file")

# We need to set resolutions.
# so, convert them from float to integer.
frame_width = 1000
frame_height = 250

size = (frame_width, frame_height)

# Below VideoWriter object will create
# a frame of above defined The output
# is stored in 'filename.avi' file.
result = cv2.VideoWriter('filename.mp4',
                         cv2.VideoWriter_fourcc(*'MP4V'),
                         25, size)
flag=0
name=0

while (True):
    ret, frame = video.read()
    flag-=1
    

    if ret == True:
        frame=frame[0:250, 0:1000]
        top = frame[40:50, 803:806]
        mid = frame[95:105, 810:815]
        down= frame[140:145, 816:819]
        top = cv2.cvtColor(top, cv2.COLOR_BGR2RGB)
        mid = cv2.cvtColor(mid, cv2.COLOR_BGR2RGB)
        down = cv2.cvtColor(down, cv2.COLOR_BGR2RGB)
        top = Image.fromarray(top)
        mid = Image.fromarray(mid)
        down = Image.fromarray(down)
        check_top = Image.open('check_top.jpg')
        check_mid = Image.open('check_mid.jpg')
        check_down = Image.open('check_down.jpg')

        t = 0
        m=0
        d=0
        for band_index, band in enumerate(top.getbands()):
            m1 = numpy.array([p[band_index] for p in top.getdata()]).reshape(*top.size)
            m2 = numpy.array([p[band_index] for p in check_top.getdata()]).reshape(*check_top.size)
            t += numpy.sum(numpy.abs(m1-m2))
        for band_index, band in enumerate(mid.getbands()):
            m1 = numpy.array([p[band_index] for p in mid.getdata()]).reshape(*mid.size)
            m2 = numpy.array([p[band_index] for p in check_mid.getdata()]).reshape(*check_mid.size)
            m += numpy.sum(numpy.abs(m1-m2))
        for band_index, band in enumerate(down.getbands()):
            m1 = numpy.array([p[band_index] for p in down.getdata()]).reshape(*down.size)
            m2 = numpy.array([p[band_index] for p in check_down.getdata()]).reshape(*check_down.size)
            d += numpy.sum(numpy.abs(m1-m2))


        if t<2000 or m<3000 or d <1000:
            flag = 30
            print('detected')
            print(t,m,d)

        if flag > 0:
                cv2.circle(frame, (190, 70), 10, color_red, -1)
               
        else:
                cv2.circle(frame, (190, 70), 10, color_green, -1)

        # Write the frame into the
        # file 'filename.avi'
        result.write(frame)

        # Display the frame
        # saved in the file


        # Press S on keyboard
        # to stop the process
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    # Break the loop
    else:
        break

# When everything done, release
# the video capture and video
# write objects
video.release()
result.release()

# Closes all the frames


print("The video was successfully saved")
