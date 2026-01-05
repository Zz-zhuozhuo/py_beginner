# %%
x=float(input("请输入充值金额："))
if 0<=x<1000:
    x=x
elif 1000<=x<5000:
    x=x*1.15
elif 5000<=x<10000:
    x=x*1.2+500
else:
    x=x+10000
print(x)


