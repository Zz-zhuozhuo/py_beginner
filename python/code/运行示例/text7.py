from time import sleep
from random import randint
def callback_func(num):
    i=randint(1, 10)
    print(f"{i*num}")   
def pb_f(sleep_time,func):
    for i in range(0,101):
        print(f"{i*'▶'}{(100-i)*'▷'} {i}%", end="\r")
        sleep(sleep_time)
        if i==100:
           func("终于结束力！")
my_list = [ "写完这段代码高考分数必如意", 750, ["计算机", "机器人", "自动化"],
           "", 12.9682, 6+9j, ["清华大学", "浙江大学"], "Apple", 
           pb_f, print("我是个print函数, 被执行了！"),
           pb_f(0.05, print("进度条函数执行完毕！"))]
while len(my_list)!=0:
        my_list.remove(my_list[0])
        print(f"{'列表已清空！'}{my_list}")
"""my_list_1=list()
for i in range(0,len(my_list)+1):
    my_list_1[i]=my_list[]

new_list=list()
for my_list in new_list:
     """