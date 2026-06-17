# x=10
# y=x

# print (int(x), int(y)
#        )\

# a='hi'
# print (id(a))
# a=a+" there"
# print (id(a))

# a=[1,2,3]
# print (id(a))
# a.append(4)
# print (id(a))
# print (a)
a= [1,2,3]
print(id(a))
b=a
print(id(b))
b.append(4)
b=a.copy()
print (a)
print (b)