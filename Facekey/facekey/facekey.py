from PIL import Image
import cv2
import time
import os

from baidu.face import face_match
from baidu.face import get_access_token

# Baidu人脸识别 API Key
CLIENT_ID = ''
# Baidu人脸识别 Secret Key
SEC_KEY = ''
# 匹配的图像地址
FACE_IMAGE_PATH = '/Users/nyloner/Image/image.jpg'
# TEMP Image 地址
TEMP_IMAGE_PATH = '/Users/nyloner/Image/temp.jpeg'


class FaceKey():
    def __init__(self):
        super(FaceKey, self).__init__()
        self.images = []
        self.capture = cv2.VideoCapture(0)

        self.client_id = CLIENT_ID
        self.sec_key = SEC_KEY
        self.token = get_access_token(self.client_id, self.sec_key)

        self.not_match_num = 0

    def face_match(self):
        result = face_match(TEMP_IMAGE_PATH, FACE_IMAGE_PATH, self.token)
        print(time.strftime('%Y-%m-%s %H:%M:%S'), 'FaceKey:', result)
        if result['result_num'] == 0:
            self.not_match_num += 1
        else:
            score = result['result'][0]['score']
            if score < 80:
                self.not_match_num += 1
            else:
                self.not_match_num = 0

        if self.not_match_num >= 5:
            self.lock_screen()

    def lock_screen(self):
        os.system('pmset displaysleepnow')
        self.capture.release()
        cv2.destroyAllWindows()
        input_key = input("Press Q(q) to quit,other to continue.\n")
        if input_key == 'q' or input_key == 'Q':
            exit(0)
        else:
            self.capture = cv2.VideoCapture(0)
            self.not_match_num = 0

    def start(self):
        time.sleep(1)
        while True:
            ret, frame = self.capture.read()
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            image.thumbnail((400, 300))
            image.save(TEMP_IMAGE_PATH, format='jpeg')
            self.face_match()
            #cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.capture.release()
        cv2.destroyAllWindows()

def execute():
    facekey = FaceKey()
    facekey.start()


if __name__ == '__main__':
    execute()
