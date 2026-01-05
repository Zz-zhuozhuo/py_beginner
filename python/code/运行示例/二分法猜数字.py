def guess_number(low_number, high_number):
    from random import randint
    answer = randint(low_number, high_number)
    guess_1= int((low_number + high_number) // 2)
    guess_count = 1
    while guess_1 != answer:
        if guess_1< answer:
            guess_1 = int((guess_1 + high_number) // 2)
        elif guess_1 > answer:
            guess_1 = int((low_number + guess_1) // 2)
        guess_count += 1
    return guess_count, answer

A = int(input("请输入一个整数："))
B = int(input("请输入另一个整数："))


if A == B:
    raise ValueError("两个数字不能相同")

if A > B:
    raise ValueError("第一个数字不能大于第二个数字")
guess_count,answer = guess_number(A, B)

print(f"猜测次数为{guess_count}",end=",")
print(f"答案为{answer}")