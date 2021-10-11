import cv2 as cv
import time
import requests
import os
import glob
import shutil


URL = 'http://192.168.43.144:80/capture'




def start_recording():

    start_time = time.time()
    specified_time = 15

    img_array = []
    img_file_name_array = []

    while True:

        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > specified_time:
            print("Finished iterating in: " + str(int(elapsed_time)) + " seconds")
            break

        response_img = requests.get(URL, stream=True)

        print(response_img.status_code)

        if response_img.status_code == 200: 

            response_img.raw.decode_content = True

            img_name = f'frame_{current_time}.jpg'


            with open(f'src/imgs/{img_name}', 'wb') as frame_buffer:
                
                shutil.copyfileobj(response_img.raw, frame_buffer)

                img_file_name_array.append(img_name)
            
    

        else:
            print('algo deu errado')


    for filename in glob.glob('/home/gustavofernandes/Documents/sv-recorder/src/imgs/*.jpg'):
        img = cv.imread(filename)
        print(img)
        
        height, width, layers = img.shape

        size = (width, height)

        img_array.append(img)     

    out = cv.VideoWriter('test.avi', cv.VideoWriter_fourcc(*'DIVX'), 3, size) 

    for i in range(len(img_array)):
        out.write(img_array[i])

    out.release()


def start_recording_from_stream():
    
    cap = cv.VideoCapture(URL)

    while(cap.isOpened()):

        ret, frame = cap.read()

        if not ret:
            break

        cv.imshow('frame', frame)

        k = cv.waitKey(1)
        if k == 27:
            break

# start_recording_from_stream()
start_recording()