#查找某元素在列表内的下标索引
my_list = ["dog", "cat", "fish", "bird", "lion"]
index = my_list.index("fish")
print(f"The index of 'fish' in the list is {index}")

#修改特定下标索引的值
my_list[2] = "lizard"
print(f"修改元素后的列表是: {my_list}")

#在指定下标索引位置插入新元素
my_list.insert(1, "elephant")
print(f"在指定下标索引位置插入新元素后的列表是: {my_list}")

#在列表末尾添加新元素
my_list.append("tiger")
print(f"在列表末尾添加新元素后的列表是: {my_list}")


#在尾部增添一批新元素
my_list2 = [1, 2, 3]
my_list.extend(my_list2)
print(f"列表在尾部追加了一批元素后是: {my_list}")
