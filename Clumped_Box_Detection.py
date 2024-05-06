import cv2
import numpy as np
# import paho.mqtt.client as mqtt
import time


def on_log(client, userdata, level, buf):
    print("log: " + buf)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code" + str(rc))


def on_message(client, userdata, msg):
    global shapeWanted
    shapeWanted = str(msg.payload.decode("utf-8"))
    print("Shape wanted changed to :" + shapeWanted + " | " + str(msg.payload.decode("utf-8")))


def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv2.setTrackbarPos(low_H_name, window_detection_name, low_H)


def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv2.setTrackbarPos(high_H_name, window_detection_name, high_H)


def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv2.setTrackbarPos(low_S_name, window_detection_name, low_S)


def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv2.setTrackbarPos(high_S_name, window_detection_name, high_S)


def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv2.setTrackbarPos(low_V_name, window_detection_name, low_V)


def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv2.setTrackbarPos(high_V_name, window_detection_name, high_V)

def on_area_thresh_trackbar(val):
    global low_a
    global high_a
    low_a = val
    low_a = min(high_a-1, low_a)
    cv2.setTrackbarPos('area', window_detection_name, low_a)


# Setting up MQTT server connection
# broker = "129.97.228.106"  # MQTT Broker IP address
# client = mqtt.Client("JetsonNano1")  # Create new instance
# client.connect(broker)
# client.subscribe("Conveyor04/shape_detected")
# client.subscribe("Conveyor04/boxes_clumped")
#
# # Linking the callback functions
# client.on_connect = on_connect
# client.on_disconnect = on_disconnect
# client.on_log = on_log
# client.on_message = on_message

time.sleep(4)

# Variable Declaration
max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
low_a = 0
high_a = 1200
font = cv2.FONT_HERSHEY_COMPLEX
counter = 0
num_rectangles_adjust = 0
limit = 50
prev_val = False
crop_x_offset = 272
crop_y_offset = 0

# Used to determine the correct values for the mask
# cv2.namedWindow(window_detection_name)
# cv2.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
# cv2.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
# cv2.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
# cv2.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
# cv2.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
# cv2.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)
# cv2.createTrackbar("area", window_detection_name , low_a, high_a, on_area_thresh_trackbar)

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('Test_Video.mp4')
frameTime = 20
colour = (0, 255, 0)  # green

while True:
    _, frame = cap.read()
    # frame = cv2.imread("Test_Image-2.jfif")

    # Loops the video
    if frame is None:
        cap = cv2.VideoCapture('Test_Video.mp4')
        _, frame = cap.read()
    
    frameWidth, frameHeight = frame.shape[:2]
    cv2.rectangle(frame, (0,0), (frameHeight, frameWidth), colour, 10)

    cropped = frame[crop_y_offset:640, crop_x_offset:445]
    frame_hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 0, 144])
    upper_red = np.array([180, 255, 255])

    mask = cv2.inRange(frame_hsv, lower_red, upper_red)
    # mask = cv2.inRange(frame_hsv, (low_H, low_S, low_V), (high_H, high_S, high_V))
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.erode(mask, kernel)

    # Contours detection
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    num_rectangle = 0
    counter += 1

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        approx = approx + [crop_x_offset, crop_y_offset]
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        # Check whether the detected contours make reasonable sense.
        # Contours that are too small or too large cannot be caused by the boxes.
        if 12000 < area < 19000:
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
            num_rectangle += 1

    if num_rectangle > num_rectangles_adjust:
        num_rectangles_adjust = num_rectangle
        print(num_rectangles_adjust)
        if num_rectangles_adjust > 1 and not prev_val:
            print("boxes_clumped = True")
            colour = (0, 0, 255) # red
            # client.publish("Conveyor04/boxes_clumped", True, 0, False)
            prev_val = True
        if num_rectangles_adjust < 2 and prev_val:
            print("boxes_clumped = False")
            colour = (0, 255, 0)  # green
            # client.publish("Conveyor04/boxes_clumped", False, 0, False)
            prev_val = False

    if counter == limit:
        num_rectangles_adjust = -1
        counter = 0

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    # Press Esc key to exit out of camera window
    key = cv2.waitKey(frameTime)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
