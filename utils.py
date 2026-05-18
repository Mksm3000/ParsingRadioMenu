import os
import shutil
from config import RESULT_DIR

def prepare_workspace(folder_name: str = RESULT_DIR) -> None:
    """ Очищает старые результаты и создает чистую папку для работы."""
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
    os.makedirs(folder_name)
    print(f'Папка {folder_name} успешно подготовлена.')

def save_to_m3u8(filepath: str, stations: list[tuple[str, str]]) -> None:
    """ Принимает готовый список станций и записывает их в формат M3U8."""
    with open(filepath, mode='w', encoding='utf-8') as file:
        file.write('#EXTM3U\n')
        for name, link in stations:
            if link: # Записываем только если ссылка успешно нашлась
                file.write(f'#EXTINF:-1, {name}\n{link}\n')

    print(f'\nПлейлист успешно сохранен в файл: {filepath}')
