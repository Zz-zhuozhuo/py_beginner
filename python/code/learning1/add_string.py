print("Hello" + "World")

name = "Alice"
age = 25
print("My name is " + name + " and I am " + str(age) + " years old.")

#通过占位来拼接
name1 = "Alice"
age1 = 25
weight1 = 60.02
message = "%s is %d years old and weighs %.2f kg." % (name1, age1, weight1)
print(message)