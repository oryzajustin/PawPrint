from threading import Thread
import cv2
import urllib
import numpy as np
import datetime
from msft_api import detect_doggo

urls = ['http://temp.dirt.io/doggo.mjpg']
# urls = ['http://temp.dirt.io/stream.mjpg']


def process_cam(url):
    stream = urllib.urlopen(url)
    bytes = ''
    first_frame = None

    detect_thresh = 5
    detected_count = 0
    x_total = 0
    y_total = 0
    w_total = 0
    h_total = 0

    count = 0


    while True:
        bytes += stream.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]

            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if first_frame is None:
                first_frame = gray
                continue

            frameDelta = cv2.absdiff(first_frame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            text = ''
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < 100:
                    continue

                (x, y, w, h) = cv2.boundingRect(c)
                if detected_count < 10:
                    x_total += x
                    y_total += y
                    w_total += w
                    h_total += h

                    detected_count += 1
                else:

                    x_avg = abs(x - x_total/10)
                    y_avg = abs(y - y_total/10)
                    w_avg = abs(w - w_total/10)
                    h_avg = abs(h - h_total/10)

                    if x_avg  > detect_thresh or y_avg > detect_thresh or w_avg > detect_thresh or h_avg > detect_thresh:
                        cv2.rectangle(i, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        text = "Motion Detected"

                    count += 1

                    detected_count = 0
                    x_total = 0
                    y_total = 0
                    w_total = 0
                    h_total = 0

                    if count >= 50:
                        thread = Thread(target=detect_doggo, args=(url,jpg,))
                        thread.start()
                        # detect_doggo(url, jpg)
                        count = 0

                    print count

            cv2.putText(i, text, (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(i, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, i.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            cv2.imshow('i', i)

            if cv2.waitKey(1) == 27:
                exit(0)


def execute():
    for url in urls:
        thread = Thread(target=process_cam(url), args=(url,))
        thread.start()

execute()
