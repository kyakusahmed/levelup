
value = []
num = [x for x in input("enter numbers! ").split(',')]
for i in num:
    x = int(i, 2)
    if not x%5:
        value.append(i)
print(','.join(value))
