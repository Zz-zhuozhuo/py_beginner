def guess_progress():
    low_number=int(input())
    high_number=int(input())
    from random import randint
    guess_number=randint(low_number ,high_number)
    try_number=randint(low_number,high_number)
    time=0
    while try_number!=guess_number:
        time+=1
        if try_number>guess_number:
            try_number=int(try_number+low_number)//2
        elif try_number<guess_number:
            try_number=int(try_number+high_number)//2
    else:
        return time,guess_number
print(guess_progress())
