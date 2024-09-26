
with open('all.txt', 'r', encoding='utf-8') as file:
    content = file.read()

lines = content.split('/n')

with open('output.txt', 'w', encoding='utf-8') as file:
    for line in lines:
        file.write(line + '\n')


