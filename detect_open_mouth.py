#!/usr/bin/env python3

# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import math
import argparse
import imutils
import time
import dlib
import cv2
import serial
import os

# stepper definitions
A1_PIN = '89'
A2_PIN = '75'
B1_PIN = '61'
B2_PIN = '62'

seq = [[1,0,0,1], [1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,1,0],[0,0,1,1], [0,0,0,1]]

delay = 0.01
steps = 100
step_count = 0
i = 0

#servo definitions
duty_min = 500000
duty_max = 2500000 
duty_range = duty_max - duty_min

servo_pwm_chip='0'
servo_pwm_pin='0'
path = '/sys/class/pwm/pwmchip' + servo_pwm_chip + '/pwm' + servo_pwm_pin + '/'

def init_pwm():
    enable_cmd = "echo 1 > " +  path + 'enable'
    print(enable_cmd)
    os.system(enable_cmd)

    period_cmd = "echo 20000000 > " + path + 'period'
    print(period_cmd)
    os.system(period_cmd)

def set_duty(duty):
    print(duty)
    os.system("echo " + duty + ' > ' +  path + 'duty_cycle')

def set_angle(angle):
    print(angle)
    duty_cycle = duty_min + (duty_range * angle / 180)
    duty_cycle = int(duty_cycle)
    set_duty(str(duty_cycle))

def fire_relay():
    relay_pin = '59'
    
    relay_fire_cmd = 'gpioset 1 ' + relay_pin + '=1'
    relay_stop_fire_cmd = 'gpioset 1 ' + relay_pin + '=0'
    
    print("starting firing...")
    os.system(relay_fire_cmd)
    
    time.sleep(5)
    
    print("stopping firing...")
    os.system(relay_stop_fire_cmd)
    
def stepper_motor_move():
    global step_count
    global i
    global steps
    global delay
    # Forwards
    if step_count < steps:
        if i == 8:
            i = 0 # reset counter
        os.system("gpioset 1 " + A1_PIN + "=" + str(seq[i][0]))
        os.system("gpioset 1 " + A2_PIN + "=" + str(seq[i][1]))
        os.system("gpioset 1 " + B1_PIN + "=" + str(seq[i][2]))
        os.system("gpioset 1 " + B2_PIN + "=" + str(seq[i][3]))
        time.sleep(delay)
        i += 1
        step_count += 1
    # Backwards
    elif step_count < 2*steps:
        if i == -1:
            i = 7 # reset counter
        os.system("gpioset 1 " + A1_PIN + "=" + str(seq[i][0]))
        os.system("gpioset 1 " + A2_PIN + "=" + str(seq[i][1]))
        os.system("gpioset 1 " + B1_PIN + "=" + str(seq[i][2]))
        os.system("gpioset 1 " + B2_PIN + "=" + str(seq[i][3]))
        time.sleep(delay)
        i -= 1
        step_count += 1
    else:
        step_count = 0

def turn_off_stepper():
    # Turn off
    os.system("gpioset 1 " + A1_PIN + "=0" )
    os.system("gpioset 1 " + A2_PIN + "=0" )
    os.system("gpioset 1 " + B1_PIN + "=0" )
    os.system("gpioset 1 " + B2_PIN + "=0" )

def decide_to_shoot(x, y):
    print(x, y)
    # if the x is over a face then shoot, near the center
    if 320 - 30 < x and x < 320 + 30:
        # Adjust servo for y
        # Assume a distance away from the camera
        d = 5
        angle = math.degrees(math.atan2(y, x-d))
        print(angle)
        set_angle(int(angle))

        # shoot
        fire_relay()


def mouth_aspect_ratio(mouth):
    # compute the euclidean distances between the two sets of
    # vertical mouth landmarks (x, y)-coordinates
    A = dist.euclidean(mouth[2], mouth[10]) # 51, 59
    B = dist.euclidean(mouth[4], mouth[8]) # 53, 57

    # compute the euclidean distance between the horizontal
    # mouth landmark (x, y)-coordinates
    C = dist.euclidean(mouth[0], mouth[6]) # 49, 55

    # compute the mouth aspect ratio
    mar = (A + B) / (2.0 * C)

    # return the mouth aspect ratio
    return mar

def calc_centroid(arr):
    x_sum = 0
    y_sum = 0
    for subarr in arr:
        x_sum += subarr[0]
        y_sum += subarr[1]
    x_sum = x_sum / len(arr)
    y_sum = y_sum / len(arr)
    return [int(x_sum), int(y_sum)]

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=False, default='shape_predictor_68_face_landmarks.dat',
        help="path to facial landmark predictor")
ap.add_argument("-w", "--webcam", type=int, default=2,
        help="index of webcam on system")
args = vars(ap.parse_args())

# define one constants, for mouth aspect ratio to indicate open mouth
MOUTH_AR_THRESH = 0.79

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# Let's init the PWM pins
init_pwm()

# grab the indexes of the facial landmarks for the mouth
(mStart, mEnd) = (49, 68)

# start the video stream thread
print("[INFO] starting video stream thread...")
vs = VideoStream(src=args["webcam"]).start()
time.sleep(1.0)

frame_width = 640
frame_height = 360

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))
time.sleep(1.0)

# loop over frames from the video stream
while True:
    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale
    # channels)
    frame = vs.read()
    frame = imutils.resize(frame, width=640)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # TODO: Maybe rotate the base?
    stepper_motor_move()

    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # extract the mouth coordinates, then use the
        # coordinates to compute the mouth aspect ratio
        mouth = shape[mStart:mEnd]

        mouthMAR = mouth_aspect_ratio(mouth)
        mar = mouthMAR
        # compute the convex hull for the mouth, then
        # visualize the mouth
        mouthHull = cv2.convexHull(mouth)

        cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
        cv2.putText(frame, "MAR: {:.2f}".format(mar), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Draw text if mouth is open
        if mar > MOUTH_AR_THRESH:
            centroid = calc_centroid(mouth)

            # Send the mouth center to the peripherals so that it can calculate angle
            decide_to_shoot(centroid[0], centroid[1]) 
            cv2.putText(frame, "Mouth is Open!", (30,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)

    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
vs.release()
cv2.destroyAllWindows()
vs.stop()
