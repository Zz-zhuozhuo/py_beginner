from random import randint
right_numer = randint(1, 100)
input("欢迎来到猜数字游戏！\n请按回车键开始游戏")
while user_guess != right_numer:  
    user_guess = int(input("请输入你猜的数字（1-100）："))
    if user_guess < right_numer:
        print("你猜的数字小了")
    elif user_guess > right_numer:
        print("你猜的数字大了")
    else:
        print("恭喜你，猜对了！")
    count = 0
    print(f"你已经猜了{count+1}次")
    if count >= 5:
        print("你已经猜了5次，太菜了！")
    elif count >= 10:
        print("你已经猜了10次，菜的没边了！")