import os
import re
import shutil

import requests


def clean_folder(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
        os.makedirs(folder_name)
    else:
        os.makedirs(folder_name)

    print('Folder "result" empty')


def get_link(data: list):
    call = requests.get(data[1])
    blocks = call.text.split('\n')

    for block in blocks:
        link_pattern = r'data-streams="(http[s]?://[^"]+)"'
        link_match = re.search(link_pattern, block)
        if link_match:
            url = link_match.group(1)
            if '?n=' in url:
                url = url.split('?n=')[0]
            return url


def txt_to_m3u8(source_file):
    base = os.path.splitext(source_file)[0]
    new_file = f"{base}.m3u8"
    os.rename(source_file, new_file)
    return new_file


def normalify(url):
    return url.replace('\n', '').replace('\'', '').replace('(', '').replace(')',
                                                                            '').split(
        ', ')


def pagination_check(raw_response) -> int:
    if 'data-paged' in raw_response.text:
        return raw_response.text.count('data-paged') - 1
    else:
        return 1


def pairify(new_response) -> list:
    temp_list = []
    items = [x for x in new_response.text.split('\n') if 'title="Radio station ' in x]
    for item in items:
        pattern = r'title="Radio station (.*?)" href="(.*?)"'
        match = re.search(pattern, item)
        if match:
            name = match.group(1).replace(',', '')
            link = base_url + match.group(2)
            patch: tuple[str, str] = (name, link)
            temp_list.append(patch)
    return temp_list


if __name__ == '__main__':
    clean_folder('result')

    base_url = 'https://radio.menu'
    country = input('\nEnter short country code: ').lower()

    response = requests.get(base_url + f'/stations/facet/country/{country}/')
    print(f'Станции найдены на {pagination_check(response)} странице(ах)')
    STATIONS = list()

    if pagination_check(response) == 1:
        list_of_pairs = pairify(response)
        STATIONS.extend(list_of_pairs)
    else:
        for num in range(pagination_check(response)):
            response = requests.get(base_url + f'/stations/facet/country/'
                                               f'{country}/paged/{num + 1}/')
            list_of_pairs = pairify(response)
            STATIONS.extend(list_of_pairs)

    # print('Список "STATIONS" готов')

    with open(file='result/stations.txt', mode='w', encoding='utf-8') as file:
        for element in STATIONS:
            file.write(str(element) + '\n')

    print('Файл "result/stations.txt" готов')

    with open(file=f'result/{country} radios.txt', mode='a', encoding='utf-8') as file:
        file.write('#EXTM3U\n')

        with open(file='result/stations.txt', mode='r', encoding='utf-8') as st_file:
            lines = st_file.readlines()
            print(f'Всего станций: {len(lines)}\n')

            for index, line in enumerate(lines):
                print(f'Добавлена станция №{index + 1} из {len(lines)}')
                station = normalify(line)
                pure_link = get_link(station)
                file.write(f'#EXTINF:-1, {station[0]}\n{pure_link}\n')

    txt_to_m3u8(f'result/{country} radios.txt')

    print('\nВсё готово!')
