
"""
注意：本代码直接是.py 文件的内容, 你可以分段复制到jupyter(.ipynb)中运行，你也可以直接执行本.py 文件
本代码示例具有超级详细的注释, 如果依然有疑问, 优先问AI, 要养成习惯，这是新时代人类的习惯

实现一个 多层感知机(MLP) 模型, 使用 PyTorch 框架
数据来源: MNIS 数据集
源作者: 依力 EL@zju.edu.cn
"""

import torch
from torch import nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import matplotlib

# 设置支持中文字体（macOS）
matplotlib.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']  # 优先使用可用字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题


# 设置超参数
# batch_size指的是每次训练使用的样本数量
batch_size = 64
# learning_rate指的是优化器的学习率
learning_rate = 0.01
# 训练的轮数
epochs = 5


# 定义图像预处理方式：转换为Tensor
transform = transforms.Compose([transforms.ToTensor()])

# 下载并加载训练集和测试集
# 训练集
train_data = datasets.MNIST(root='data', train=True, transform=transform, download=True)
# 测试集
test_data = datasets.MNIST(root='data', train=False, transform=transform, download=True)
# 创建数据加载器
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
# 创建测试数据加载器
test_loader = DataLoader(test_data, batch_size=batch_size)



# 展示部分训练图像
examples = enumerate(train_loader)
batch_idx, (example_data, example_targets) = next(examples)
# 显示前6张图像
fig, axes = plt.subplots(1, 6, figsize=(15, 3))
for i in range(6):
    axes[i].imshow(example_data[i][0], cmap="gray")
    axes[i].set_title(f"Label: {example_targets[i].item()}")
    axes[i].axis('off')
plt.suptitle("Example Training Images")
plt.show()



# 构建简单的多层感知机模型（包含隐藏层，便于可视化输出）
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        
        # 定义网络结构，包括输入层、隐藏层和输出层，flatten指的是将输入图像展平，目的是将28x28的图像转换为一维向量
        self.flatten = nn.Flatten()

        
        # 输入层到隐藏层的线性变换，输入维度为28*28=784，输出维度为128
        self.hidden = nn.Linear(784, 128)

        # 激活函数ReLU，数学表达式为f(x) = max(0, x)
        self.relu = nn.ReLU()

        # 隐藏层到输出层的线性变换，输出维度为10（对应数字0-9）
        self.output = nn.Linear(128, 10)





    
    # 前向传播函数，定义数据如何通过网络流动
    def forward(self, x):
        # x是输入图像，形状为(batch_size, 1, 28, 28)
        x = self.flatten(x)

        hidden_out_raw = self.hidden(x)  # 通过输入层到隐藏层的线性变换
        # 通过隐藏层和激活函数
        hidden_out = self.relu(hidden_out_raw)  # 获取隐藏层输出


        # 最终输出层
        out = self.output(hidden_out)


        # 返回输出和隐藏层输出
        return out, hidden_out
    



# 初始化模型、损失函数和优化器
model = MLP()
# 定义损失函数为交叉熵损失，适用于多分类问题
loss_fn = nn.CrossEntropyLoss()











# 定义优化器为随机梯度下降（SGD），学习率为0.01
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

train_losses = []
test_accuracies = []

# 训练模型，循环进行多个epoch
for epoch in range(epochs):
    # 每个epoch的训练损失初始化为0
    epoch_loss = 0
    # 设置模型为训练模式
    model.train()
    # 遍历训练数据加载器
    for images, labels in train_loader:
        # 前向传播，获取模型输出和隐藏层输出
        outputs, _ = model(images)
        # 计算损失
        loss = loss_fn(outputs, labels)
        # 清零梯度
        optimizer.zero_grad()
        # 反向传播计算梯度
        loss.backward()
        # 更新模型参数
        optimizer.step()
        # 累加损失
        epoch_loss += loss.item()
    # 记录每个epoch的平均损失
    train_losses.append(epoch_loss / len(train_loader))

    # 测试模型
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

# 可视化训练过程
plt.figure(figsize=(12, 5))

# 训练损失图
plt.subplot(1, 2, 1)
plt.plot(range(1, epochs+1), train_losses, marker='o')
plt.title("Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")

# 测试准确率图
plt.subplot(1, 2, 2)
plt.plot(range(1, epochs+1), test_accuracies, marker='o', color='green')
plt.title("Test Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy (%)")

plt.tight_layout()
plt.show()

# 选取一个测试样本，查看隐藏层输出
sample_img, _ = test_data[0]
sample_img_batch = sample_img.unsqueeze(0)  # 添加 batch 维度
model.eval()
with torch.no_grad():
    _, hidden_out = model(sample_img_batch)

# 展示隐藏层前20个神经元激活值
plt.figure(figsize=(10, 3))
plt.bar(range(20), hidden_out[0][:20].numpy())
plt.title("First 20 Hidden Layer Activations")
plt.xlabel("Neuron Index")
plt.ylabel("Activation")
plt.show()

# 展示部分测试图像及模型预测结果
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
plt.suptitle("Test Images: Prediction (P) vs True (T)")
plt.show()

# 假设 model 是你训练完的 MLP 实例
torch.save(model.state_dict(), "mlp_mnist_model.pt")