import glob
import os
import requests
from bs4 import BeautifulSoup
from selene import browser, query, be
from selenium import webdriver


def clean_folder(folder_name):
    files = glob.glob(os.path.join(folder_name, '*'))
    for file in files:
        os.remove(file)
        print(f'File {file} removed')
    print('Folder "result" empty')


def get_radio(data: list):
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('--headless')
    browser.config.driver_options = driver_options


    try:
        temp_url = data[1]
        browser.open(temp_url)
        radio_link = browser.element('.stream.display-flex').get(query.attribute(
            'data-streams'))

        castro = radio_link.split('?n=')[0]

    except:
        return ''
    finally:
        browser.quit()
    return castro


def txt_to_m3u8(source_file):
    base = os.path.splitext(source_file)[0]
    new_file = f"{base}.m3u8"
    os.rename(source_file, new_file)
    return new_file


if __name__ == '__main__':

    clean_folder('result')

    base_url = 'https://radio.menu'
    country = input('\nCountry: ').lower()

    response = requests.get(base_url + f'/stations/facet/country/{country}/')
    soup = BeautifulSoup(response.text, 'html.parser')

    collection = soup.find_all('a',
                               class_='grid items-center relative w-full bg-white '
                                      'transition duration-500 shadow ease-in-out '
                                      'transform hover:-translate-y-1 hover:shadow-lg '
                                      'select-none cursor-pointer bg-white rounded-md '
                                      'p-2')

    STATIONS = list()

    for item in collection:
        name = item.attrs['title'].replace('Radio station ', '').replace(',', ' ')
        link = base_url + item.attrs['href']
        patch = (name, link)
        STATIONS.append(patch)

    print('Список "STATIONS" готов')

    with open(file='result/stations.txt', mode='w', encoding='utf-8') as file:
        for element in STATIONS:
            file.write(str(element) + '\n')

    print('Файл "stations.txt" готов')

    with open(file=f'result/{country} radios.txt', mode='a', encoding='utf-8') as file:
        file.write('#EXTM3U8\n')

        with open(file='result/stations.txt', mode='r', encoding='utf-8') as st_file:
            lines = st_file.readlines()
            print(f'Всего строк: {len(lines)}')

            for index, line in enumerate(lines):
                print(f'Добавлена станция №{index + 1} из {len(lines)}')

                station = line.replace('\n', '').replace('\'',
                                                         '').replace('(',
                                                                     '').replace(
                    ')', '').split(', ')
                pure_link = get_radio(station)
                file.write(f'# EXTINF:-1, {station[0]}\n{pure_link}\n')

    txt_to_m3u8(f'result/{country} radios.txt')

    print('\nВсё готово!')
