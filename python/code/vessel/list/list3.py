mylist = [1, 2, 3, 4, 5]

#删除方式1：使用del语句删除元素
del mylist[2]
print(f"用del语句删除元素后的列表是: {mylist}")

#删除方式2：使用pop()方法删除元素
mylist = [1, 2, 3, 4, 5]
mylist.pop(2)
print(f"用pop()方法删除元素后的列表是: {mylist}")

#删除方式3：使用remove()方法删除元素
mylist = [1, 2, 3, 3, 4, 5]
mylist.remove(3)
print(f"用remove()方法删除元素后的列表是: {mylist}")

#清空列表中的所有元素
mylist.clear()
print(f"清空列表中的所有元素后的列表是: {mylist}")

#统计列表中某个元素的个数
mylist = [1, 2, 3, 3, 4, 5]
count = mylist.count(3)
print(f"统计列表中某个元素的个数: {count}")

#统计列表中全部元素个数
mylist = [1, 2, 3, 3, 4, 5]
count = len(mylist)
print(f"统计列表中全部元素个数: {count}")