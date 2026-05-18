import os
import requests
from config import BASE_URL, RESULT_DIR
from utils import prepare_workspace, save_to_m3u8
from parser import extract_pages_count, parse_stations_from_page, get_stream_link


def main():
    country = input('Введи короткий код страны (например: rs, ru, us): ').strip().lower()
    if not country:
        print("Код страны не может быть пустым!")
        return

    # 1. Подготовка папки
    prepare_workspace(RESULT_DIR)

    # 2. Получаем первую страницу, чтобы узнать количество страниц
    first_url = f'{BASE_URL}/stations/facet/country/{country}/'
    try:
        response = requests.get(first_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при подключении к сайту: {e}")
        return

    pages_count = extract_pages_count(response.text)
    print(f'Станции найдены на {pages_count} странице(ах)')

    # 3. Собираем пары (Название, Ссылка на страницу) со всех страниц пагинации
    all_stations = []
    print('Сбор общего списка станций...')

    # Обрабатываем первую страницу, которую уже скачали
    all_stations.extend(parse_stations_from_page(response.text))

    # Если страниц больше одной, проходим по остальным в цикле
    if pages_count > 1:
        for num in range(2, pages_count + 1):
            page_url = f'{BASE_URL}/stations/facet/country/{country}/paged/{num}/'
            try:
                res = requests.get(page_url, timeout=10)
                all_stations.extend(parse_stations_from_page(res.text))
            except requests.RequestException:
                print(f"Не удалось загрузить страницу пагинации №{num}, пропускаем.")

    total_stations = len(all_stations)
    print(f'Всего найдено станций: {total_stations}\n')

    if total_stations == 0:
        print("Станций не найдено. Завершение работы.")
        return

    # 4. Проходим по каждой станции и вытаскиваем прямую ссылку на аудио-поток
    valid_playlist = []

    for index, (name, page_url) in enumerate(all_stations):
        print(f'Обработка станции №{index + 1} из {total_stations}: {name}')

        stream_link = get_stream_link(page_url)
        if stream_link:
            valid_playlist.append((name, stream_link))
        else:
            print(f'  --> Ссылка для "{name}" не найдена.')

    # 5. Сохраняем финальный результат
    output_file = os.path.join(RESULT_DIR, f'{country}_radios.m3u8')
    save_to_m3u8(output_file, valid_playlist)

    print(f'Всё готово! Успешно собрано потоков: {len(valid_playlist)} из {total_stations}')


if __name__ == '__main__':
    main()