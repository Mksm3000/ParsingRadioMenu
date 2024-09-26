import os
import re
import time


# with open('all.txt', 'r', encoding='utf-8') as file:
#     content = file.read()
#
# lines = content.split('/n')
#
# with open('output.txt', 'w', encoding='utf-8') as file:
#     for line in lines:
#         file.write(line + '\n')


def txt_to_md(source_file):
    base = os.path.splitext(source_file)[0]
    new_file = f"{base}.md"
    time.sleep(5)
    os.rename(source_file, new_file)
    return new_file


with open('output.txt', 'r', encoding='utf-8') as file:
    content = file.read()

lines = content.split('</a>\n')

with open('readme.txt', 'w', encoding='utf-8') as file:
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
        stamp = f'# | <img src="{flag_url}" alt="{country}" width="32" height="21"> | {country} | {short_name} |'
        file.write(stamp + '\n')

txt_to_md('readme.txt')
