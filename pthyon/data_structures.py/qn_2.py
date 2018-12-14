lines = []
while True:
    x = input('enter sentence! ')
    if x:
        lines.append(x.upper())
    else:
        break;

for sentence in lines:
    print(sentence)