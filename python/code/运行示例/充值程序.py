input_money=int(input("请输入你的充值金额: "))
name=input("你是否为新顾客: ")
if 2000>=input_money>=1000:
    final_money=input_money+input_money+input_money*0.15
elif 10000>=input_money>=2000:
    final_money=input_money+input_money+input_money*0.2+500
elif input_money>10000:
    final_money=input_money+10000
if name=="是":
    final_money=final_money+final_money*0.1
else:
    final_money=final_money
print(f"你好！你最终的充值金额为: {final_money}元")