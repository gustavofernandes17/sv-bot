import os
import glob
import shutil 
from time import time
import cv2 
import requests

class Recorder: 


    def __init__(self) -> None:

        self.elapsed_time = 0
        self.should_break = False

        self.video_path = os.getcwd() + '/src/videos'
        self.jpg_buffers_path = os.getcwd() + '/src/jpg_buffer/'

        self.jpg_capture_url = 'http://192.168.15.67:80/jpg'

        self.errors = []

        self.fps = 1
    
    def set_jpg_capture_url(self, url):
        self.jpg_capture_url = url

    def set_video_path(self, video_path):
        self.video_path = video_path

    def set_jpg_buffers_path(self, jpg_path):
        self.jpg_buffers_path = jpg_path

    def capture_buffers(self):

        start_time = time()

        self.should_break = False

        while True:

            self.elapsed_time = time() - start_time

            if self.should_break == True: 
                break 

            filename = f'frame_{time()}.jpg'
            
            response_jpg = requests.get(self.jpg_capture_url, stream=True)

            if response_jpg.status_code == 200:
                
                response_jpg.raw.decode_content = True

                with open(self.jpg_buffers_path + filename, 'wb') as buffer_file: 

                    shutil.copyfileobj(response_jpg.raw, buffer_file)
                    print(f'[CAPTURE BUFFERS - S] {filename} salvo com sucesso')


            else: 
                self.errors.append
                (
                    f'[CAPTURE BUFFERS - ERR] não foi possível acessar a url de captura código de resposta da requisição {response_jpg.status_code}'
                )
        
            

    def stop_recording(self): 
        self.should_break = True


        jpg_array = []

        for filename in glob.glob(self.jpg_buffers_path + '*.jpg'): 

            img = cv2.imread(filename)

            height, width, _ = img.shape

            size = (width, height)

            jpg_array.append(img)

        out = cv2.VideoWriter(
            f'{self.video_path}/simov_captura_{int(time())}-{self.elapsed_time}.mp4',
            cv2.VideoWriter_fourcc(*'MP4V'), 
            self.fps, 
            size
        )

        for i in range(len(jpg_array)): 
            out.write(jpg_array[i])

        out.release()


        for filename in os.listdir(self.jpg_buffers_path):

            os.remove(os.getcwd() + f'/src/jpg_buffer/{filename}')

            

