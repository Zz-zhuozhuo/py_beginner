
"""
注意：本代码直接是.py 文件的内容, 你可以分段复制到jupyter(.ipynb)中运行，你也可以直接执行本.py 文件
本代码示例具有超级详细的注释, 如果依然有疑问, 优先问AI, 要养成习惯，这是新时代人类的习惯

实现一个 CNN 卷积神经网络模型，使用 PyTorch 框架
数据来源: MNIST 数据集
源作者: 依力 EL@zju.edu.cn
"""

import torch
from torch import nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# 设置超参数
batch_size = 64
learning_rate = 0.01
epochs = 5

# 数据预处理
transform = transforms.Compose([transforms.ToTensor()])
train_data = datasets.MNIST(root='data', train=True, transform=transform, download=True)
test_data = datasets.MNIST(root='data', train=False, transform=transform, download=True)
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_data, batch_size=batch_size)

# 展示部分训练图像
examples = enumerate(train_loader)
_, (example_data, example_targets) = next(examples)
fig, axes = plt.subplots(1, 6, figsize=(15, 3))
for i in range(6):
    axes[i].imshow(example_data[i][0], cmap="gray")
    axes[i].set_title(f"Label: {example_targets[i].item()}")
    axes[i].axis('off')
plt.suptitle("Example Training Images")
plt.show()

# 定义 CNN 模型
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        # 卷积层1：输入1个通道（灰度图），输出16个通道，卷积核大小5x5，填充2（保持尺寸不变）
        self.conv1 = nn.Conv2d(1, 16, kernel_size=5, padding=2)  # 输出: (16, 28, 28)
        # 激活函数
        self.relu1 = nn.ReLU()
        # 池化层1：2x2 最大池化，输出尺寸减半
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

model = CNN()
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

train_losses = []
test_accuracies = []

# 模型训练
for epoch in range(epochs):
    epoch_loss = 0
    model.train()
    for images, labels in train_loader:
        outputs, _ = model(images)
        loss = loss_fn(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    train_losses.append(epoch_loss / len(train_loader))

    # 测试阶段
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            outputs, _ = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    test_accuracies.append(100 * correct / total)
    print(f"Epoch {epoch+1}, Loss: {epoch_loss:.4f}, Accuracy: {test_accuracies[-1]:.2f}%")

# 可视化训练曲线
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(range(1, epochs+1), train_losses, marker='o')
plt.title("Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.subplot(1, 2, 2)
plt.plot(range(1, epochs+1), test_accuracies, marker='o', color='green')
plt.title("Test Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy (%)")
plt.tight_layout()
plt.show()

# 查看特征图（隐藏层输出）
sample_img, _ = test_data[0]
sample_img_batch = sample_img.unsqueeze(0)
model.eval()
with torch.no_grad():
    _, feature_map = model(sample_img_batch)

# 显示前6个通道的特征图
fig, axes = plt.subplots(1, 6, figsize=(15, 3))
for i in range(6):
    axes[i].imshow(feature_map[0][i].numpy(), cmap='viridis')
    axes[i].set_title(f"Feature {i+1}")
    axes[i].axis('off')
plt.suptitle("Conv1 Feature Maps")
plt.show()

# 展示测试图像和预测结果
examples = enumerate(test_loader)
_, (example_data, example_targets) = next(examples)

model.eval()
with torch.no_grad():
    outputs, _ = model(example_data)
    _, predictions = torch.max(outputs, 1)

fig, axes = plt.subplots(2, 6, figsize=(15, 5))
for i in range(12):
    ax = axes[i // 6][i % 6]
    ax.imshow(example_data[i][0], cmap='gray')
    ax.set_title(f"P: {predictions[i].item()}, T: {example_targets[i].item()}")
    ax.axis('off')
plt.suptitle("Test Predictions vs True Labels")
plt.show()
torch.save(model.state_dict(), "mlp_mnist_model_cnn.pt")