import cv2
import numpy as np

def detect():
    cap = cv2.VideoCapture(0)  # 使用默认摄像头
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 添加这一行

        # 在这里，你可以添加你的目标检测代码
        # 例如: frame = your_object_detection_function(frame)

        yield frame  # 使用yield返回摄像头的每一帧

        # 如果你有任何要显示的消息或信息，你可以返回它们，例如:
        # yield frame, "Detected an object!"

    cap.release()