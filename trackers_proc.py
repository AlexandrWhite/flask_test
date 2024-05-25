import cv2
from ultralytics import YOLO
import torch
import time 

if __name__ != '__main__':
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = YOLO('yolov8n').to(device)
    print(f'Using device for Tracking tests: {device}')
    model.fuse()


        


def process_frame(frame):
    start = time.time()

    frame = cv2.resize(frame, (720, 640))

    result = model.track(
        tracker='bytetrack.yaml',
        verbose = False,
        classes = [2,3,5,7])
    
    frame = result[0].plot()

    if (time.time()-start) != 0:
        fps = 1/(time.time()-start) 
        fps = 'FPS:' + str(int(fps))
        font = cv2.FONT_HERSHEY_SIMPLEX 
        cv2.putText(frame, fps, (7, 70), font, 2, (100, 255, 0), 3, cv2.LINE_AA) 
    
    


    return frame

