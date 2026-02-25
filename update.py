import base64
import requests
import os

# === НАСТРОЙКИ ===

# Твои постоянные конфиги (вставь сюда все 118 штук)
MY_CONFIGS = """
vless://552265ad-e6d4-44f6-86b3-5036ba7f7feb@95.85.245.104:8443?security=reality&encryption=none&pbk=T6xIzGPsy--IRyF0ts9LgfDka7bDMjOaOKT6zJ1hL1U&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=eh.vk.com#🇪🇪 LatteVpn
vless://552265ad-e6d4-44f6-86b3-5036ba7f7feb@93.123.39.204:443?security=reality&encryption=none&pbk=ReHxtyEtHLEiCAraVUd3jlS8XIKTRVxuTCHDr0zQSTY&headerType=none&type=tcp&flow=xtls-rprx-vision&sni=est.alibarda-ru.ru#🇪🇪 LatteVpn
vless://048cc1d8-971e-4566-9c97-6bac03779d92@ee.tropico.su:443?security=reality&encryption=none&pbk=oNi0HaIqxbf26tEGKplHFpoULf1K3ulyT4wnYczcGTg&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=teamdocs.su&sid=1e9d8c7b6a5f4321#🇪🇪 LatteVpn
""".strip()
# ↑↑↑ СЮДА ВСТАВЬ ВСЕ 118 КОНФИГОВ ↑↑↑

# Подписки которые надо скачивать и добавлять (если есть)
EXTERNAL_SUBS = [
    # "https://example.com/sub1",
    # "https://example.com/sub2",
]

# === КОД ===

def fetch_sub(url):
    """Скачивает подписку и декодирует"""
    try:
        r = requests.get(url, timeout=15)
        try:
            decoded = base64.b64decode(r.text.strip()).decode('utf-8')
            return [line.strip() for line in decoded.splitlines() if line.strip()]
        except:
            return [line.strip() for line in r.text.splitlines() if line.strip()]
    except Exception as e:
        print(f"Ошибка: {url} - {e}")
        return []

def main():
    all_configs = []
    
    # Добавляем свои конфиги
    for line in MY_CONFIGS.splitlines():
        if line.strip():
            all_configs.append(line.strip())
    
    # Добавляем из внешних подписок
    for sub_url in EXTERNAL_SUBS:
        configs = fetch_sub(sub_url)
        all_configs.extend(configs)
        print(f"Загружено {len(configs)} из {sub_url}")
    
    # Убираем дубликаты
    all_configs = list(dict.fromkeys(all_configs))
    
    # Сохраняем обычный файл
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_configs))
    
    # Сохраняем Base64 версию
    b64 = base64.b64encode("\n".join(all_configs).encode()).decode()
    with open("sub_base64.txt", "w", encoding="utf-8") as f:
        f.write(b64)
    
    print(f"Готово! Всего конфигов: {len(all_configs)}")

if __name__ == "__main__":
    main()
