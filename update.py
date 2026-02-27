import requests
from urllib.parse import unquote

# Твои постоянные конфиги
MY_CONFIGS = """
vless://552265ad-e6d4-44f6-86b3-5036ba7f7feb@95.85.245.104:8443?security=reality&encryption=none&pbk=T6xIzGPsy--IRyF0ts9LgfDka7bDMjOaOKT6zJ1hL1U&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=eh.vk.com#🇪🇪 LatteVpn
""".strip()

# Подписки для скачивания
EXTERNAL_SUBS = [
    "https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/26.txt",
    "https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/1.txt",
    "https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/6.txt",
    "https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt",
    "https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/23.txt",
]

COUNTRY_FLAGS = {
    'ru': '🇷🇺', 'ee': '🇪🇪', 'fi': '🇫🇮', 'se': '🇸🇪', 'de': '🇩🇪', 
    'nl': '🇳🇱', 'pl': '🇵🇱', 'fr': '🇫🇷', 'gb': '🇬🇧', 'us': '🇺🇸', 
    'at': '🇦🇹', 'ch': '🇨🇭', 'lv': '🇱🇻', 'lt': '🇱🇹', 'kz': '🇰🇿', 
    'hk': '🇭🇰', 'in': '🇮🇳', 'jp': '🇯🇵', 'sg': '🇸🇬', 'tr': '🇹🇷', 
    'ua': '🇺🇦', 'ca': '🇨🇦', 'au': '🇦🇺'
}

COUNTRY_ORDER = [
    '🇪🇪', '🇫🇮', '🇸🇪', '🇱🇻', '🇱🇹', '🇵🇱', '🇩🇪', '🇳🇱', '🇦🇹', '🇨🇭',
    '🇫🇷', '🇬🇧', '🇹🇷', '🇰🇿', '🇺🇸', '🇨🇦', '🇭🇰', '🇯🇵', '🇸🇬', '🇮🇳', '🇦🇺',
    '🇷🇺', '🌍'
]

def fetch_sub(url):
    """Скачивает подписку (обрабатывает и текст, и base64 на входе)"""
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        text = r.text.strip()
        # Проверяем, не в base64 ли входящая подписка, чтобы прочитать её
        if not text.startswith(('vless://', 'vmess://', 'ss://', 'trojan://')):
            import base64
            try:
                text = base64.b64decode(text).decode('utf-8')
            except:
                pass
        return [l.strip() for l in text.splitlines() if l.strip()]
    except Exception as e:
        print(f"Ошибка загрузки {url}: {e}")
        return []

def detect_country(config):
    config_lower = config.lower()
    for keyword, flag in COUNTRY_FLAGS.items():
        if keyword in config_lower:
            return flag
    return '🌍'

def rename_config(config):
    if '#' not in config: return config
    base = config.rsplit('#', 1)[0]
    
    # Логика переименования
    if 'security=reality' in config.lower():
        return f"{base}#🇷🇺 Обход Глушилок"
    
    name = unquote(config.split('#')[-1]).lower()
    if any(kw in name for kw in ['youtube', 'ютуб', 'yt']):
        return f"{base}#🇷🇺 YouTube Без Рекламы"
    
    flag = detect_country(config)
    return f"{base}#{flag} LatteVpn"

def get_sort_key(config):
    if '🇷🇺 YouTube' in config: return (0, config)
    if '🇷🇺 Обход' in config: return (1, config)
    for i, flag in enumerate(COUNTRY_ORDER):
        if flag in config: return (i + 2, config)
    return (100, config)

def main():
    all_configs = []
    
    # 1. Добавляем свои
    for line in MY_CONFIGS.splitlines():
        if line.strip(): all_configs.append(line.strip())
    
    # 2. Добавляем внешние
    for sub_url in EXTERNAL_SUBS:
        configs = fetch_sub(sub_url)
        for cfg in configs:
            if cfg.startswith(('vless://', 'vmess://', 'trojan://', 'ss://')):
                all_configs.append(rename_config(cfg))
    
    # Удаляем дубли и сортируем
    all_configs = list(dict.fromkeys(all_configs))
    all_configs.sort(key=get_sort_key)
    
    # 3. СОХРАНЕНИЕ В ЧИСТОМ ВИДЕ (БЕЗ BASE64)
    with open("Sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_configs))
    
    print(f"✅ Готово! Файл Sub.txt обновлен. Всего конфигов: {len(all_configs)}")

if __name__ == "__main__":
    main()
