def say_hi():
    print("Hi, there!")
    return

result = say_hi()
print("函数的返回值是：", {result})
print("返回类型是：", type(result))

#none of if
def check_age(age):
    if age < 18:
        return
    else:
        return "success"
    
result = check_age(22)
if not result:
    print("未满18岁，无法通过验证")
