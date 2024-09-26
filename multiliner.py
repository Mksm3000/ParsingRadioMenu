import re

# with open('all.txt', 'r', encoding='utf-8') as file:
#     content = file.read()
#
# lines = content.split('/n')
#
# with open('output.txt', 'w', encoding='utf-8') as file:
#     for line in lines:
#         file.write(line + '\n')


with open('output.txt', 'r', encoding='utf-8') as file:
    content = file.read()

lines = content.split('</a>\n')
print(lines)

with open('readme.md', 'a', encoding='utf-8') as file:
    file.write(
        '| Флаг         | Название страны | Обозначение '
        '|\n|--------------|----------------|-------------|\n')
    for line in lines:
        country_pattern = r'alt=[\'"]?(.*?)[\'"]?"'
        country_match = re.search(country_pattern, line)
        country = country_match.group(1)
        flag_pattern = r'src=[\'"]?(.*?)[\'"]?"'
        flag_match = re.search(flag_pattern, line)
        flag_url = flag_match.group(1)
        short_pattern = r'href=[\'"]?(.*?)[\'"]?"'
        short_match = re.search(short_pattern, line)
        short_name = short_match.group(1).split('/')[-2]
        stamp = (f'# | ![{country}](<img width="32" height="21" src="{flag_url}") | {country} | {short_name} |')
        file.write(stamp + '\n')
