array = [4, 7, 1, 3, 12, 5, 0, 8]

for i in range(len(array) - 1, -1, -1):
    for c in range(0, i):
        if array [i] < array[c]:
            array[i], array[c] = array[c], array[i]

print(array)
