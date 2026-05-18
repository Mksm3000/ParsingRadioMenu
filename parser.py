import re
import requests
from config import BASE_URL


def extract_pages_count(html_text: str) -> int:
    """Определяет, сколько страниц пагинации есть у выбранной страны."""
    if 'data-paged' in html_text:
        return html_text.count('data-paged') - 1
    return 1


def parse_stations_from_page(html_text: str) -> list[tuple[str, str]]:
    """Находит на странице радиостанции и возвращает список кортежей (имя, ссылка)."""
    stations = []
    # Фильтруем строки, где точно есть радиостанции, чтобы не гонять регулярку по всему HTML
    items = [x for x in html_text.split('\n') if 'title="Radio station ' in x]

    pattern = r'title="Radio station (.*?)" href="(.*?)"'
    for item in items:
        match = re.search(pattern, item)
        if match:
            name = match.group(1).replace(',', '')
            link = BASE_URL + match.group(2)
            stations.append((name, link))
    return stations


def get_stream_link(station_url: str) -> str | None:
    """Заходит на страницу конкретной радиостанции и вытаскивает прямую ссылку на поток."""
    try:
        response = requests.get(station_url, timeout=10)
        if response.status_code != 200:
            return None

        blocks = response.text.split('\n')
        link_pattern = r'data-streams="(http[s]?://[^"]+)"'

        for block in blocks:
            match = re.search(link_pattern, block)
            if match:
                url = match.group(1)
                if '?n=' in url:
                    url = url.split('?n=')[0]
                return url
    except requests.RequestException:
        pass  # Если сайт заглючил или пропал интернет, просто пропускаем станцию
    return None
