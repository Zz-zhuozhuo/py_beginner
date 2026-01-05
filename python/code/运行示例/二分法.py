from random import randint
low_number = 0
high_number = 10000
answer=randint(low_number , high_number)

middle_number = int((low_number + high_number)/2)
new_low_number = low_number
new_high_number = high_number
guess_count = 1

while middle_number != answer:
    if answer > middle_number:
        new_low_number = middle_number
        middle_number = int((middle_number + high_number)/2)
    elif answer < middle_number:
        new_high_number = middle_number
        middle_number = int((new_low_number + middle_number)/2)
    
    guess_count += 1
    print(f"第{guess_count}次猜测，猜测到的数字是:{middle_number}")