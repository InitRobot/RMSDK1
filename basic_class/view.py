import cv2
import socket
import struct
import time

# HOST = '10.42.0.1'  # 电脑端地址
# PORT = 9999
# server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server.connect((HOST, PORT))
capture = cv2.VideoCapture(1)

w = 3
h = 4
capture.set(w, 640)
capture.set(h, 360)
# l = capture.get(w)
# k = capture.get(h)
# print(l,k)
try:
    while True:
        a = time.time()
        print(a)
        success, frame = capture.read_latest_frame()
        print(frame)
        #result, imgencode = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])  # 编码
        # server.sendall(imgencode)  # 发送视频帧数据
        #imgencode = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        #cv2.imshow("Live view", img)
        cv2.imshow("Live view", frame)
        cv2.waitKey(1)
        b = time.time()
        print(b - a)
        print(frame.shape)
except Exception as e:
    print(e)
    capture.release()
    # server.close()