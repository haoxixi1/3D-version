import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import appcamare
import sys
import socket
import struct
import time

def read_data_from_file(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

class MainApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        # 设置主窗口的默认大小
        self.window.geometry('1200x760')
        self.video_source = None  # 初始时不启动摄像头
        # 使用place方法调整Canvas部件的位置
        self.canvas = Canvas(window, width=760, height=540)
        self.canvas.place(x=50, y=10)  # 使用x和y参数来指定Canvas部件的位置
        # 使用place方法调整按钮的位置
        self.btn_start = tk.Button(window, text="Start", width=10, command=self.start_camera)
        self.btn_start.place(x=1000, y=600)  # 使用x和y参数来指定按钮的位置
        # 添加一个Text部件来显示的输出
        self.output_box = tk.Text(window, height=30, width=40)  # 你可以根据需要调整height和width的值
        self.output_box.place(x=850, y=10)  # 你可以根据需要调整x和y的值
        self.status_box = tk.Text(window, height=5, width=40)  # 调整height和width的值以适应你的需求
        self.status_box.place(x=850, y=450)  # 调整x和y的值以适应你的布局
        self.delay = 10
        self.s = None
        self.window.mainloop()

    def send_packet_0(self, team_id):
        JUDGE_BOX_IP = '169.254.54.123'
        JUDGE_BOX_PORT = 6666
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((JUDGE_BOX_IP, JUDGE_BOX_PORT))

        data_type = 0
        data_length = len(team_id)
        header = struct.pack('>II', data_type, data_length)
        self.s.sendall(header + team_id.encode())
        print("数据包0成功发送到裁判盒!")

    def send_packet_1(self, data_content):
        if self.s:  # 检查socket是否存在
            data_type = 1
            data_length = len(data_content)
            header = struct.pack('>II', data_type, data_length)
            self.s.sendall(header + data_content.encode())
            self.s.close()  # 发送完数据包1后，关闭连接
            self.s = None  # 将socket对象设置为None
            print("数据包1成功发送到裁判盒!")
        else:
            print("Socket连接不存在!")

    def start_camera(self):
        self.update_status("正在加载模型")
        original_stdout = sys.stdout
        sys.stdout = self
        self.send_packet_0(team_id)
        sys.stdout = original_stdout
        self.window.after(1000, self.load_camera)  # 延迟1秒后加载摄像头

    def load_camera(self):
        if not self.video_source:  # 如果摄像头还没启动
            self.video_source = appcamare.detect()  # 创建摄像头帧的生成器
            self.update_status("模型加载成功")  # 新增的状态更新
            self.update()  # 开始更新
            self.window.after(500, self.redirect_stdout)  # x秒后开始重定向stdout
            self.update_status("正在识别")

    def redirect_stdout(self):
        sys.stdout = self

    def update(self):
        frame = next(self.video_source, None)  # 获取下一个摄像头帧，如果没有更多帧，则返回None

        if frame is not None:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.window.after(self.delay, self.update)  # 继续更新
        else:
            self.display_output()  # 当没有更多帧时，显示输出内容

    #显示识别结果
    def display_output(self):
        self.update_status("识别结束")
        original_stdout = sys.stdout
        sys.stdout = self
        self.send_packet_1(data_content)
        sys.stdout = original_stdout
        with open('SUDA-wlyl-Rx.txt', 'r') as file:
            content = file.read()
            self.output_box.insert(tk.END, content)
            self.output_box.see(tk.END)

    def update_status(self, message):
        self.status_box.insert(tk.END, message + "\n")
        self.status_box.see(tk.END)

    def flush(self):
        # 这个方法是为了满足sys.stdout的接口要求，实际上我们不需要实现任何功能
        pass

team_id = "Y2309T43880"  # 请替换为你的队伍ID
data_content_filename = "SUDA-wlyl-Rx.txt"  # 替换为你的txt文件的路径
data_content = read_data_from_file(data_content_filename)
root = tk.Tk()
app = MainApp(root, "3D视觉")