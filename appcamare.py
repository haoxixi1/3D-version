import matplotlib
matplotlib.use('Agg')
import argparse
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized


def detect():
    class_counts = {}
    source, weights, view_img, save_txt, imgsz = opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://', 'https://'))

    # Initialize
    set_logging()
    device = select_device(opt.device)
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

    # Set Dataloader
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
    frame_idx = 0

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    for path, img, im0s, vid_cap in dataset:
        if frame_idx > 0:  # 如果不是第一帧，跳过
            break
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        pred = model(img, augment=opt.augment)[0]

        # Apply NMS
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)

        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            p, s, im0, frame = path[i], '', im0s[i].copy(), dataset.count
            s += '%gx%g ' % img.shape[2:]  # print string
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                for cls in det[:, -1].unique():
                    class_name = names[int(cls)]
                    if class_name not in class_counts:
                        class_counts[class_name] = 0
                    class_counts[class_name] += (det[:, -1] == cls).sum().item()

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if  view_img:  # Add bbox to image
                        label = f'{names[int(cls)]} {conf:.2f}'
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)

            # Print time (inference + NMS)
            print(s)

            # Stream results
            cv2.waitKey(1)  # 1 millisecond
            im0 = cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)
            yield im0

            frame_idx += 1

        with open('SUDA-wlyl-Rx.txt', 'w') as f:
            f.write("START\n")
            for class_name, count in class_counts.items():
                f.write(f"Goal_ID={class_name};Num={count}\n")
            f.write("END\n")

    yield None

class Options:
    pass

opt = Options

opt.weights = 'yolov5s.pt'
opt.source = '0'
opt.img_size = 640
opt.conf_thres = 0.25
opt.iou_thres = 0.45
opt.device = ''
opt.view_img = False
opt.save_txt = False
opt.save_conf = False
opt.nosave = False
opt.classes = None
opt.agnostic_nms = False
opt.augment = False
opt.update = False
opt.project = 'runs/detect'
opt.name = 'exp'
opt.exist_ok = False
opt.no_trace = False
print(opt)

