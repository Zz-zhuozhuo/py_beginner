
"""
注意：本代码直接是.py 文件的内容, 你可以分段复制到jupyter(.ipynb)中运行，你也可以直接执行本.py 文件
本代码示例具有超级详细的注释, 如果依然有疑问, 优先问AI, 要养成习惯，这是新时代人类的习惯

实现一个 CNN 卷积神经网络模型，并且使用摄像头实时识别手写数字，使用 PyTorch 框架
数据来源: MNIST 数据集
源作者: 依力 EL@zju.edu.cn
"""


import cv2
import torch
from torch import nn
from torchvision import transforms
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']  # 优先使用可用字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题

# ===== 定义 MLP 模型结构 =====
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=5, padding=2)  # 输出: (16, 28, 28)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(2, 2)                          # 输出: (16, 14, 14)
        
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5, padding=2) # 输出: (32, 14, 14)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(2, 2)                          # 输出: (32, 7, 7)

        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.relu3 = nn.ReLU()
        self.output = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool1(self.relu1(self.conv1(x)))  # conv1 block
        feature_map = x                            # 保存特征图
        x = self.pool2(self.relu2(self.conv2(x)))  # conv2 block
        x = self.flatten(x)
        x = self.relu3(self.fc1(x))
        x = self.output(x)
        return x, feature_map

# ===== 加载模型 =====
model = CNN()
# 注意：这里假设你已经训练好了模型并保存为 'mlp_mnist_model_cnn.pt'
model.load_state_dict(torch.load("mlp_mnist_model_cnn.pt", map_location=torch.device("cpu")))
model.eval()

# ===== 图像预处理函数 =====
def preprocess(img_cv2):
    # Step 1: 灰度化
    gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)

    # Step 2: 高斯滤波降噪
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Step 3: 自适应阈值 + 反色（黑底白字）
    binary = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
        blockSize=11, C=2
    )

    # Step 4: 找最大轮廓（数字区域）
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("❌ 未检测到数字")
        return None, None

    # Step 5: 裁剪数字区域（最大轮廓）
    x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
    digit_roi = binary[y:y+h, x:x+w]

    # Step 6: 居中 + 缩放成 20x20
    resized_digit = cv2.resize(digit_roi, (20, 20), interpolation=cv2.INTER_AREA)

    # Step 7: 创建空白画布 28x28，居中粘贴
    canvas = np.zeros((28, 28), dtype=np.uint8)
    x_offset = (28 - 20) // 2
    y_offset = (28 - 20) // 2
    canvas[y_offset:y_offset+20, x_offset:x_offset+20] = resized_digit

    # Step 8: PIL 转换 + 可视化
    img_pil = Image.fromarray(canvas)
    plt.imshow(img_pil, cmap='gray')
    plt.title("标准化输入图像")
    plt.axis('off')
    plt.show()

    # Step 9: 转换为Tensor并归一化到[0,1]
    transform = transforms.Compose([
        transforms.ToTensor()
    ])
    img_tensor = transform(img_pil).unsqueeze(0)  # [1, 1, 28, 28]

    return img_tensor, img_pil


# ===== 打开摄像头 =====
cap = cv2.VideoCapture(0)
print("📷 摄像头已打开，按 's' 拍照识别，按 'q' 退出程序")

while True:
    ret, frame = cap.read()
    if not ret:
        continue
    # 显示实时画面
    cv2.imshow("Camera - Press 's' to snap, 'q' to quit", frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'):
        # 拍照 + 处理
        img_tensor, img_pil = preprocess(frame)
        with torch.no_grad():
            output, _ = model(img_tensor)
            pred = torch.argmax(output, dim=1).item()
        print(f"🎯 识别结果：{pred}")

        # 显示识别图像
        plt.imshow(img_pil, cmap='gray')
        plt.title(f"预测结果：{pred}")
        plt.axis('off')
        plt.show()

cap.release()
cv2.destroyAllWindows()
