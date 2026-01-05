from random import randint
low_number = 0
high_number = 10000
answer=randint(low_number,high_number)
guess_number = None
guess_count=0

while guess_number !=answer:
    guess_number=randint(low_number,high_number)
    guess_count += 1
    print(f"第{guess_count}次猜测，猜测的数字是:{guess_number}")
    print(f"猜测的数字是:{guess_number}")