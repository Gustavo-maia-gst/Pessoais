maxNum = 20

a, b = 0, 1

for n in range(0, maxNum - 1):
    a, b = b, a + b

print(b)
print(b < 2 ** 64)
