
"""
注意：本代码直接是.py 文件的内容, 你可以分段复制到jupyter(.ipynb)中运行，你也可以直接执行本.py 文件
本代码示例具有超级详细的注释, 如果依然有疑问, 优先问AI, 要养成习惯，这是新时代人类的习惯

实现一个 Softmax 回归标签分类模型，使用 PyTorch 框架
数据来源: MNIST-Fashion 数据集
源作者: 依力 EL@zju.edu.cn

基于LR线性回归的示例代码之外, 需要额外安装:
- torchvision: `pip install torchvision`
pytorch框架中专门用于处理图像数据的库, 提供了常用的数据集和预处理方法
"""


import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import matplotlib


# 英伟达 GPU 配置
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(f"Using device: {device}")

# Apple M系列 GPU 配置
# if torch.backends.mps.is_available():
#     device = torch.device("mps")  # 使用 Apple GPU
# else:
#     print("❌ MPS 不可用，回退到 CPU")
# device = torch.device("mps"  else "cpu")


# 设置支持中文字体（macOS是这样设置，Windows问一下AI，我没测试过）
matplotlib.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']  # 优先使用可用字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题


# ========== 1. 设置随机种子确保结果可复现 ==========
# 设置 PyTorch 中的随机数生成器的种子为 42，以确保每次运行时生成的随机数是相同的，从而让你的实验结果具有“可复现性”
# 在深度学习中，很多操作都涉及随机性，例如：
# 初始化模型参数（权重）
# 数据加载时的随机打乱（shuffle）
# 数据增强（如随机裁剪、旋转等）
# 设置随机种子可以确保每次运行时这些随机操作的结果都是一样的
torch.manual_seed(42)


# ========== 2. 数据预处理 ==========
transform = transforms.Compose([
    # 将图像转换为张量，范围变为 [0, 1]，图像原始像素值一般是 0~255，经 ToTensor() 转成 Tensor 后，会变成 [0, 1] 之间的浮点数
    transforms.ToTensor(), 


    # 标准化到 [-1, 1]，标准化的作用是将这些值进一步变成一个分布更适合训练的范围，通常是 均值为0，方差为1 的分布，也就是标准正态分布，将像素值从中心值 0.5 减去，变成以 0 为中心（对称），再除以 0.5，扩大分布范围（从 [0, 1] → [-1, 1]）
    # 若像素值为 1，则变为 (1 - 0.5) / 0.5 = 1；若像素值为 0，则变为 (0 - 0.5) / 0.5 = -1；若像素值为 0.5：则变为 (0.5 - 0.5) / 0.5 = 0，所以整个像素值的范围由 [0, 1] 转换成了 [-1, 1]
    transforms.Normalize((0.5,), (0.5,))
])


# ========== 3. 下载并加载数据集 ==========
train_dataset = datasets.FashionMNIST(root='data', train=True, download=True, transform=transform)
test_dataset = datasets.FashionMNIST(root='data', train=False, download=True, transform=transform)


# batch_size每次迭代用多少个样本来计算梯度，小（如 1 或 16）学习更细致、泛化好，但训练慢、不稳定、噪声大；大（如 128 或 512）稳定、速度快但泛化能力差、内存占用大；64（经验值）稳定性 + 泛化折中好，是深度学习中常用默认值
# shuffle=True每个 epoch 随机打乱数据顺序，避免模型学到“样本顺序的偏见”，尤其对于梯度下降，如果每次 batch 的顺序一样，很容易陷入局部最优或过拟合，shuffle=True 每一轮都会重新洗牌，使得模型泛化能力更强
# 假设你是个老师，要教 60 个学生考试技巧：
# 如果你每次上课都让前 10 个是学霸，最后 10 个是学渣，学生就可能学会了“顺序”而不是“技巧”
# 你把学生洗牌，随机 10 人一组，每节课的学生都不一样，教学效果就更平均，模型泛化能力也更好
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True) 
# test_loader 测试集通常不需要打乱顺序，因为我们只关心最终的准确率，保持评估一致性，不需要“泛化训练”
test_loader = DataLoader(test_dataset, batch_size=64)


# ========== 4. 类别标签 ==========
class_names = [
    'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
    'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot'
]

# ========== 5. 可视化部分图像样本 ==========
def show_sample_images():
    images, labels = next(iter(train_loader))
    plt.figure(figsize=(10, 4))
    for i in range(6):
        plt.subplot(1, 6, i + 1)
        plt.imshow(images[i].squeeze(), cmap='gray')
        plt.title(class_names[labels[i]])
        plt.axis('off')
    plt.suptitle("🎨 示例训练图像")
    plt.tight_layout()
    plt.show()


show_sample_images()


# ========== 6. 构建 Softmax 回归模型 ==========
class SoftmaxRegression(nn.Module):
    def __init__(self):
        super().__init__()
        # 输入图像大小为 28x28，展平为 784 维向量
        self.flatten = nn.Flatten()
        self.linear = nn.Linear(28 * 28, 10)  # 784 -> 10 个类别

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear(x)  # 输出 raw score（logits）
        return logits



model = SoftmaxRegression()


# ========== 7. 损失函数 & 优化器 ==========
# 交叉熵损失函数，内部有两步：Softmax：将模型输出的 logits 转为概率分布; Log + NLLLoss：计算真实类别对应位置的对数概率并取负;所以你 不需要再手动加 softmax，直接传 raw logits 就行了
loss_fn = nn.CrossEntropyLoss()
# 定义优化器（Optimizer）,随机梯度下降,学习率为 0.1，表示每次更新参数时走的“步长”，实际上用的是 小批量随机梯度下降，因为你传入的是小批量数据
# 0.1 是一个经验值，其实并没有一个放之四海而皆准的值
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
# 想用Adam？可以试试
# optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


# ========== 8. 训练过程 ==========
# 定义训练模型的函数，参数 num_epochs 表示训练多少个周期（整个训练集被模型看几遍）
def train_model(num_epochs=5):
    # 遍历每一个 epoch（训练周期）
    for epoch in range(num_epochs):
        running_loss = 0.0  # 累计每轮的总损失
        correct = 0         # 累计预测正确的样本数
        total = 0           # 累计总样本数，用于计算准确率

        # 遍历训练集的每一个 batch（小批量），每个 batch 包含一组图像和对应标签
        for images, labels in train_loader:
            # 将一批图像输入模型，得到预测的原始分数（logits）
            outputs = model(images)

            # 计算当前 batch 的损失（预测值 outputs 与真实标签 labels 的差距）
            loss = loss_fn(outputs, labels)

            # 清除之前 batch 的梯度，避免梯度累加
            optimizer.zero_grad()

            # 反向传播：自动计算所有模型参数对损失函数的梯度
            loss.backward()

            # 更新模型参数（根据刚刚计算出的梯度调整参数）
            optimizer.step()

            # 累加损失值，.item() 是将张量转为 Python 数值
            running_loss += loss.item()

            # torch.max(outputs, 1) 返回最大值和对应下标，这里我们取下标（即预测的类别）
            _, predicted = torch.max(outputs.data, 1)

            # 统计这一批的总样本数
            total += labels.size(0)

            # 统计这一批中预测正确的数量（与真实标签比对）
            correct += (predicted == labels).sum().item()

        # 每个 epoch 结束后，计算训练准确率
        acc = 100 * correct / total

        # 打印当前 epoch 的平均损失和准确率
        print(f"Epoch {epoch + 1}, Loss: {running_loss:.4f}, Accuracy: {acc:.2f}%")

train_model()


# ========== 9. 测试集上评估模型 ==========
def test_model():
    # 关闭 Dropout（随机丢弃部分神经元，防止过拟合）、BatchNorm（使用当前 batch 的均值和方差进行归一化） 等训练时特有的行为，确保推理时模型表现一致、稳定，模型进入评估模式
    model.eval()
    correct = 0
    total = 0
    # 在推理或测试时禁用梯度计算，节省内存和计算资源，并加快速度（因为不需要反向传播）
    with torch.no_grad():
        correct = 0      # 用于累计预测正确的样本数
        total = 0        # 用于累计测试集的总样本数

        # 遍历整个测试集的数据加载器（按 batch 加载）
        for images, labels in test_loader:
            # 将图像送入模型进行前向传播，输出为每类的打分（logits）
            outputs = model(images)

            # 从 logits 中取每个样本得分最大的索引，作为预测的类别
            _, predicted = torch.max(outputs.data, 1)

            # 累加当前 batch 的样本数量
            total += labels.size(0)

            # 将预测与真实标签逐个对比，统计预测正确的个数
            correct += (predicted == labels).sum().item()

        # 计算整体测试准确率
        accuracy = 100 * correct / total
        print(f"✅ 测试准确率：{accuracy:.2f}%")

test_model()

# ========== 10. 可视化预测结果 ==========
def visualize_predictions():
    model.eval()
    # next() 会从 test_loader 中取出第一个 batch，也就是测试集的前 64 张图像和对应标签，images: 一个包含多个图像的张量，形状是 [batch_size, 1, 28, 28]，labels: 一个包含多个图像对应标签的张量，形状是 [batch_size]
    images, labels = next(iter(test_loader))
    outputs = model(images)
    _, predicted = torch.max(outputs.data, 1)

    plt.figure(figsize=(12, 4))
    for i in range(6):
        plt.subplot(1, 6, i + 1)
        plt.imshow(images[i].squeeze(), cmap='gray')
        plt.title(f"Pred: {class_names[predicted[i]]}")
        plt.axis('off')
    plt.suptitle("🔍 模型在测试集上的预测")
    plt.tight_layout()
    plt.show()

visualize_predictions()

torch.save(model.state_dict(), "softmax_mnist_fashion.pt")