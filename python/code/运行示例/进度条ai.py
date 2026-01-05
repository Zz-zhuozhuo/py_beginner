def progress_bar(current, total, bar_length=40):
    percent = float(current) / total
    arrow = '█' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(arrow))
    print(f'\r进度: [{arrow}{spaces}] {int(percent * 100)}%', end='')
    if current == total:
        print()  # 换行

# 示例用法
import time

for i in range(101):
    progress_bar(i, 100)
    time.sleep(0.05)