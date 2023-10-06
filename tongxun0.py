import socket
import struct
import time

# 初始化SEND_DATA为True
SEND_DATA = True

def send_data_to_judge_box0(team_id,data_content):
    global SEND_DATA  # 声明SEND_DATA为全局变量
    # 定义裁判盒的IP和端口
    JUDGE_BOX_IP = '192.168.137.1'  # 请替换为实际的裁判盒IP地址
    JUDGE_BOX_PORT = 6666

    # 创建一个TCP套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((JUDGE_BOX_IP, JUDGE_BOX_PORT))

    if SEND_DATA:
        # 设置DataType和DataLength
        data_type = 0  # 0表示发送队伍ID
        data_length = len(team_id)

        # 将DataType和DataLength打包为大端字节序的格式
        header = struct.pack('>II', data_type, data_length)  # '>II'表示两个大端字节序的int
        print(header)
        # 发送数据
        s.sendall(header + team_id.encode())
        print("数据成功发送到裁判盒!")

        time.sleep(10)
        data_type = 1  # 1表示你的特定数据类型
        data_length = len(data_content)

        # 将DataType和DataLength打包为大端字节序的格式
        header = struct.pack('>II', data_type, data_length)  # '>II'表示两个大端字节序的int

        # 发送数据
        s.sendall(header + data_content.encode())
        s.close()
        print("数据成功发送到裁判盒!")




def send_data_to_judge_box1(data_content):
    global SEND_DATA  # 声明SEND_DATA为全局变量
    # 定义裁判盒的IP和端口
    JUDGE_BOX_IP = '192.168.137.1'  # 请替换为实际的裁判盒IP地址
    JUDGE_BOX_PORT = 6666

    # 创建一个TCP套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((JUDGE_BOX_IP, JUDGE_BOX_PORT))

    if SEND_DATA:
        # 设置DataType和DataLength
        data_type = 1  # 1表示你的特定数据类型
        data_length = len(data_content)

        # 将DataType和DataLength打包为大端字节序的格式
        header = struct.pack('>II', data_type, data_length)  # '>II'表示两个大端字节序的int

        # 发送数据
        s.sendall(header + data_content.encode())
        s.close()
        print("数据成功发送到裁判盒!")


# 使用函数发送队伍ID

team_id = "aaa111"  # 请替换为你的队伍ID
data_content = """
START
Goal_ID=CA002;Num=2
Goal_ID=CAO05;Num=2
Goal_ID=CD001;Num=2
END
"""

send_data_to_judge_box0(team_id=team_id,data_content=data_content)



