from fric.pyposit import Posit

# x = posit(1, "0001001")
# y = posit(1, "0001111")
# ## 0000101→+000101 3/128

# # print(x)
# # print(x.to_float())
# print(y)
# print(3/128)
# y.from_float(3/128, 7, 1)
# print(y)
# print(y.to_float_2c())

print(3/16) # 0001110 7 1
x = Posit(1, "0001110")
print(x, x.to_float_2c())
x.from_float(x.to_float_2c(), 7, 1)
print(x, x.to_float_2c())

print(3/128) # 0000101 7 1
x = Posit(1, "0000101")
print(x, x.to_float_2c())
x.from_float(x.to_float_2c(), 7, 1)
print(x, x.to_float_2c())
