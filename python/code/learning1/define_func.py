def add(a, b):
    rusult = a + b
    return rusult

#return后面不再执行任何代码，因此不能将代码写在return后面。

num1 = input("请输入第一个数字：")
num2 = input("请输入第二个数字：")

result = add(int(num1), int(num2))

print("结果是：", result)