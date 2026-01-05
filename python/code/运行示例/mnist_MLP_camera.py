"""
注意：本代码直接是.py 文件的内容, 你可以分段复制到jupyter(.ipynb)中运行，你也可以直接执行本.py 文件
本代码示例具有超级详细的注释, 如果依然有疑问, 优先问AI, 要养成习惯，这是新时代人类的习惯

实现一个 多层感知机(MLP) 模型, 并且使用摄像头实时识别手写数字， 使用 PyTorch 框架
数据来源: MNIS 数据集
源作者: 依力 EL@zju.edu.cn

需要额外安装
- CV2：`pip install opencv-python`
- PIL：`pip install pillow`
- torchvision：`pip install torchvision`

注意，本模型效果非常差！
"""
import cv2
import torch
from torch import nn
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']  # 优先使用可用字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题


# ===== 定义 MLP 模型结构 =====
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.hidden = nn.Linear(28 * 28, 128)
        self.relu = nn.ReLU()
        self.output = nn.Linear(128, 10)

    def forward(self, x):
        x = self.flatten(x)
        hidden_out = self.relu(self.hidden(x))
        out = self.output(hidden_out)
        return out, hidden_out

# ===== 加载模型 =====
model = MLP()
model.load_state_dict(torch.load("mlp_mnist_model.pt", map_location=torch.device("cpu")))
model.eval()

# ===== 图像预处理函数 =====
def preprocess(img_cv2):
    # ========== Step 1. 灰度化 ==========
    gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)

    # ========== Step 2. 高斯滤波去噪 ==========
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # ========== Step 3. 自适应阈值二值化 ==========
    # 255 - cv2.ADAPTIVE_THRESH_GAUSSIAN_C 是为了将黑字白底 → 白字黑底
    binary = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
        blockSize=11, C=2
    )

    # ========== Step 4. PIL 转换 & Resize ==========
    img_pil = Image.fromarray(binary).convert('L')

    # 可视化二值图像
    plt.imshow(img_pil, cmap='gray')
    plt.title("二值化图像")
    plt.axis('off')
    plt.show()

    # ========== Step 5. 转换为Tensor ==========
    transform = transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.ToTensor()
    ])
    img_tensor = transform(img_pil).unsqueeze(0)  # [1, 1, 28, 28]

    # ========== Step 6. 显示模型看到的图像 ==========
    plt.imshow(img_tensor.squeeze().numpy(), cmap='gray')
    plt.title("模型看到的图像")
    plt.axis('off')
    plt.show()

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
