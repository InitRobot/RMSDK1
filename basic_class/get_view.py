import cv2


class vidio:
    def __init__(self):
        self.cap = cv2.VideoCapture(1)
        #fps = cap.get(cv2.CAP_PROP_FPS)

    def get_vidio(self):
        success, frame = self.cap.read_latest_frame()
        if not success:
            print("fail")
            return False
        return frame


if __name__ == '__main__':
    my_vidio = vidio
    while True:
        frame = my_vidio.get_vidio()
        print(frame)
