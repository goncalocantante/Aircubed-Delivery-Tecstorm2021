from pyzbar.pyzbar import decode
from djitellopy import tello
from time import sleep
import numpy as np
import pygame
import cv2


def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))


def get_key(keyname):
    ans = False
    for eve in pygame.event.get():
        pass
    keyinput = pygame.key.get_pressed()
    mykey = getattr(pygame, 'K_{}'.format(keyname))
    if keyinput[mykey]:
        ans = True
    pygame.display.update()
    return ans


pError = [0, 0]
pid = [0.4, 0.4, 0]
w = 360
h = 240
fbRange = [9000, 11000]

#me = None


def PolygonArea(corners):
    n = len(corners)  # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area


def track_qr(me, fbRange, info, w, h, pid, pError):
    area = info[1]
    x, y = info[0]

    error_alt = y - h // 2
    error_lat = x - w // 2

    speed_alt = pid[0] * error_alt + pid[1] * (error_alt - pError[0])
    speed_alt = int(np.clip(speed_alt, -25, 25))
    speed_alt = -speed_alt
    speed_y = pid[0] * error_lat + pid[1] * (error_lat - pError[1])
    speed_y = int(np.clip(speed_y, -25, 25))

    if fbRange[0] < area < fbRange[1]:
        fb = 0
    elif area >= fbRange[1]:
        fb = -25
    elif area <= fbRange[0] and area != 0:
        fb = 25

    print(speed_y, fb, speed_alt)

    me.send_rc_control(speed_y, fb, speed_alt, 0)

    return [speed_y, fb, speed_alt, 0], [error_alt, error_lat]


def auto_pilot(me, pError):

    rc_command = [0, 0, 0, 0]

    while True:
        detected = False
        img = me.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        # cv2.normalize(img, img, -65, 190, cv2.NORM_MINMAX)
        # success, img = cap.read()
        for barcode in decode(img):
            data = barcode.data.decode('utf-8')
            pts = np.array([barcode.polygon], np.int32)
            listpts = pts
            listpts.tolist()
            corners = [tuple(point) for point in listpts[0]]
            area = PolygonArea(corners)
            print(area)
            pts = pts.reshape((-1, 1, 2))
            centroid = np.mean(pts, axis=0)
            detected = True
        if detected:
            cv2.polylines(img, [pts], True, (255, 0, 0), 3)
            cv2.circle(img, (int(centroid[0][0]), int(
                centroid[0][1])), 3, (255, 0, 0), 3)
            info = [(int(centroid[0][0]), int(centroid[0][1])), area]
            rc_command, pError = track_qr(me, fbRange, info, w, h, pid, pError)
        else:
            me.send_rc_control(0, 0, 0, 0)
            pError = [0, 0]
        if get_key('v'):
            manual_pilot(me)
        elif get_key('c'):
            me.takeoff()
        elif get_key('b'):
            me.land()
            break
        cv2.imshow('Image', img)
        cv2.waitKey(1)


def manual_pilot(me):

    while True:
        lr, fb, ud, yv = 0, 0, 0, 0

        if get_key('LEFT'):
            lr = -50
        elif get_key('RIGHT'):
            lr = 50

        if get_key('UP'):
            ud = 50
        elif get_key('DOWN'):
            ud = -50

        if get_key('w'):
            fb = 50
        elif get_key('s'):
            fb = -50

        if get_key('a'):
            yv = -50
        elif get_key('d'):
            yv = 50

        print(lr, fb, ud, yv)

        if get_key('n'):
            break

        me.send_rc_control(lr, fb, ud, yv)


me = tello.Tello()
me.connect()
me.streamon()
print(me.get_battery())

'''cap = cv2.VideoCapture(0)
cap.set(3, 60)
cap.set(4, 40)'''

init()

auto_pilot(me, pError)
