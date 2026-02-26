import base64
import requests
import re
from urllib.parse import unquote, urlparse, parse_qs

# Твои постоянные конфиги (вставь все 118 штук)
MY_CONFIGS = """
vless://552265ad-e6d4-44f6-86b3-5036ba7f7feb@95.85.245.104:8443?security=reality&encryption=none&pbk=T6xIzGPsy--IRyF0ts9LgfDka7bDMjOaOKT6zJ1hL1U&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=eh.vk.com#🇪🇪 LatteVpn
""".strip()
# ^^^ ВСТАВЬ ВСЕ 118 КОНФИГОВ ^^^

# Подписки для скачивания
EXTERNAL_SUBS = [
    "https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt",
    "https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/1.txt",
    "https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt",
    "https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt",
    "https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt",
]

# Флаги стран
COUNTRY_FLAGS = {
    'ru': '🇷🇺', 'russia': '🇷🇺', 'россия': '🇷🇺', 'msk': '🇷🇺', 'spb': '🇷🇺', 'moscow': '🇷🇺',
    'ee': '🇪🇪', 'estonia': '🇪🇪', 'эстония': '🇪🇪',
    'fi': '🇫🇮', 'finland': '🇫🇮', 'финляндия': '🇫🇮',
    'se': '🇸🇪', 'sweden': '🇸🇪', 'швеция': '🇸🇪',
    'de': '🇩🇪', 'germany': '🇩🇪', 'германия': '🇩🇪',
    'nl': '🇳🇱', 'netherlands': '🇳🇱', 'нидерланды': '🇳🇱', 'ams': '🇳🇱', 'amsterdam': '🇳🇱',
    'pl': '🇵🇱', 'poland': '🇵🇱', 'польша': '🇵🇱',
    'fr': '🇫🇷', 'france': '🇫🇷', 'франция': '🇫🇷',
    'gb': '🇬🇧', 'uk': '🇬🇧', 'united kingdom': '🇬🇧', 'великобритания': '🇬🇧', 'англия': '🇬🇧',
    'us': '🇺🇸', 'usa': '🇺🇸', 'сша': '🇺🇸', 'america': '🇺🇸',
    'at': '🇦🇹', 'austria': '🇦🇹', 'австрия': '🇦🇹',
    'ch': '🇨🇭', 'switzerland': '🇨🇭', 'швейцария': '🇨🇭',
    'lv': '🇱🇻', 'latvia': '🇱🇻', 'латвия': '🇱🇻', 'riga': '🇱🇻', 'рига': '🇱🇻',
    'lt': '🇱🇹', 'lithuania': '🇱🇹', 'литва': '🇱🇹',
    'kz': '🇰🇿', 'kazakhstan': '🇰🇿', 'казахстан': '🇰🇿',
    'hk': '🇭🇰', 'hong kong': '🇭🇰', 'гонконг': '🇭🇰',
    'in': '🇮🇳', 'india': '🇮🇳', 'индия': '🇮🇳',
    'jp': '🇯🇵', 'japan': '🇯🇵', 'япония': '🇯🇵',
    'sg': '🇸🇬', 'singapore': '🇸🇬', 'сингапур': '🇸🇬',
    'tr': '🇹🇷', 'turkey': '🇹🇷', 'турция': '🇹🇷',
    'ua': '🇺🇦', 'ukraine': '🇺🇦', 'украина': '🇺🇦',
    'ca': '🇨🇦', 'canada': '🇨🇦', 'канада': '🇨🇦',
    'au': '🇦🇺', 'australia': '🇦🇺', 'австралия': '🇦🇺',
}

# Порядок сортировки (ближе = выше)
COUNTRY_ORDER = [
    '🇪🇪', '🇫🇮', '🇸🇪', '🇱🇻', '🇱🇹', '🇵🇱', '🇩🇪', '🇳🇱', '🇦🇹', '🇨🇭',
    '🇫🇷', '🇬🇧', '🇹🇷', '🇰🇿', '🇺🇸', '🇨🇦', '🇭🇰', '🇯🇵', '🇸🇬', '🇮🇳', '🇦🇺',
    '🇷🇺', '🌍'
]

def fetch_sub(url):
    """Скачивает подписку"""
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        text = r.text.strip()
        try:
            decoded = base64.b64decode(text).decode('utf-8')
            return [l.strip() for l in decoded.splitlines() if l.strip()]
        except:
            return [l.strip() for l in text.splitlines() if l.strip()]
    except Exception as e:
        print(f"Ошибка: {url} - {e}")
        return []

def detect_country(config):
    """Определяет страну по конфигу"""
    config_lower = config.lower()
    
    # Ищем в хосте и названии
    for keyword, flag in COUNTRY_FLAGS.items():
        if keyword in config_lower:
            return flag
    
    return '🌍'

def is_reality(config):
    """Проверяет есть ли Reality"""
    return 'security=reality' in config.lower()

def is_youtube(config):
    """Проверяет YouTube в названии"""
    name = unquote(config.split('#')[-1] if '#' in config else '')
    keywords = ['youtube', 'ютуб', 'yt']
    return any(kw in name.lower() for kw in keywords)

def rename_config(config):
    """Переименовывает конфиг по правилам"""
    if '#' not in config:
        return config
    
    base = config.rsplit('#', 1)[0]
    
    # YouTube
    if is_youtube(config):
        return f"{base}#🇷🇺 YouTube Без Рекламы"
    
    # Reality = Обход Глушилок
    if is_reality(config):
        return f"{base}#🇷🇺 Обход Глушилок"
    
    # Обычный = LatteVpn с флагом страны
    flag = detect_country(config)
    return f"{base}#{flag} LatteVpn"

def get_sort_key(config):
    """Ключ сортировки"""
    if '🇷🇺 YouTube' in config:
        return (100, config)
    if '🇷🇺 Обход' in config:
        return (99, config)
    
    for i, flag in enumerate(COUNTRY_ORDER):
        if flag in config:
            return (i, config)
    
    return (98, config)

def main():
    all_configs = []
    
    # Свои конфиги (уже переименованные)
    for line in MY_CONFIGS.splitlines():
        if line.strip() and (line.startswith('vless://') or line.startswith('vmess://') or 
                            line.startswith('trojan://') or line.startswith('ss://')):
            all_configs.append(line.strip())
    
    print(f"Своих конфигов: {len(all_configs)}")
    
    # Внешние подписки
    for sub_url in EXTERNAL_SUBS:
        configs = fetch_sub(sub_url)
        for cfg in configs:
            if cfg.startswith(('vless://', 'vmess://', 'trojan://', 'ss://')):
                renamed = rename_config(cfg)
                all_configs.append(renamed)
        print(f"Загружено {len(configs)} из {sub_url}")
    
    # Убираем дубликаты
    all_configs = list(dict.fromkeys(all_configs))
    
    # Сортируем
    all_configs.sort(key=get_sort_key)
    
    # Сохраняем
    with open("Sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_configs))
    
    print(f"\n✅ Готово! Всего: {len(all_configs)} конфигов")

if __name__ == "__main__":
    main()
