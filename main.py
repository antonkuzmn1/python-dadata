import sqlite3
from dadata import Dadata

def get_settings():
    conn = sqlite3.connect('settings.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        base_url TEXT,
        api_key TEXT,
        language TEXT
    )
''')
    cursor.execute(
        'SELECT base_url, api_key, language FROM settings WHERE id = 1')
    settings = cursor.fetchone()
    if settings is None:
        cursor.execute("INSERT INTO settings (id, base_url, api_key, language) VALUES (?, ?, ?, ?)",
                   (1, "default_base_url", "default_api_key", "ru"))
        conn.commit()
        conn.close()
        return ("default_base_url", "default_api_key", "ru")
    else:
        conn.close()
        return settings

def save_settings(base_url, api_key, language):
    conn = sqlite3.connect('settings.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE settings SET base_url=?, api_key=?, language=? WHERE id = 1',
                   (base_url, api_key, language))
    conn.commit()
    conn.close()

def searcher(cin, base_url, api_key, language):
    dadata = Dadata(api_key)
    results = dadata.suggest("address", cin, 10, language=language)
    i = 1
    for result in results:
        print('[', i, ']', result['value'])
        i += 1
    choice = int(input())
    selected_address = results[choice - 1]['value']
    return dadata.suggest("address", selected_address, language=language)

def resultat(cin, base_url, api_key, language):
    a = searcher(cin, base_url, api_key, language)
    print(a[0]['value'], a[0]['data']['geo_lat'], a[0]['data']['geo_lon'])

def main():
    base_url, api_key, language = get_settings()
    if language == 'en':
        cin = input('Enter addres: ')
    else:
        cin = input('Введите адрес: ')
    while cin:
        resultat(cin, base_url, api_key, language)
        if language == 'en':
            cin = input('Enter addres: ')
        else:
            cin = input('Введите адрес: ')
    menu()

def menu():
    base_url, api_key, language = get_settings()
    if language == 'en':
        print('\nBase URL addres:', base_url)
        print('API-key:', api_key)
        print('Language: english\n')
        print('[ 1 ] Search')
        print('[ 2 ] Settings')
        print('[ 3 ] Exit')
    else:
        print('\nБазовый URL адрес:', base_url)
        print('API-ключ:', api_key)
        print('Язык: русский\n')
        print('[ 1 ] Поиск')
        print('[ 2 ] Настройки')
        print('[ 3 ] Выход')
    a = input()
    if a.isnumeric():
        if int(a) == 1:
            main()
        elif int(a) == 2:
            if language == 'en':
                new_base_url = input('Enter URL: ')
            else:
                new_base_url = input('Введите URL: ')
            if new_base_url == '':
                new_base_url = base_url
            if language == 'en':
                new_api_key = input('Enter API-key: ')
            else:
                new_api_key = input('Введите API-ключ: ')
            if new_api_key == '':
                new_api_key = api_key
            if language == 'en':
                lang = input('Select language (en/ru): ').upper()
            else:
                lang = input('Выберите язык (en/ru): ').upper()
            while lang != 'EN' and lang != 'RU':
                if language == 'en':
                    lang = input('Select language (en/ru): ').upper()
                else:
                    lang = input('Выберите язык (en/ru): ').upper()
            save_settings(new_base_url, new_api_key, lang.lower())
            menu()
        else:
            return
    else:
        return

if __name__ == "__main__":
    menu()
