import requests
from bs4 import BeautifulSoup


def get_URL(BASE_URL):
    s = input("Введите название отеля: ").lower()
    c = input("Введите двухбуквенное сокращение страны(например, Russia = ru): ").lower()
    if "hotel" in s:
        for i in range(len(s) - 4):
            if s[i:i + 5] == "hotel":
                s = s[0:i] + s[i+5:len(s)]

    s = s.replace(' ', '-')
    if s[-1] == '-': s = s[0:-1]
    if s[0] == '-': s = s[1:]
    url = ""
    for i in range(len(BASE_URL) - 1):
        if BASE_URL[i] == '<' and BASE_URL[i + 1] == '>':
            url = BASE_URL[:i] + s + BASE_URL[i+2:]
            break
    if url == "": return "-1"
    for i in range(len(url) - 1):
        if url[i] == '[' and url[i + 1] == ']':
            URL = url[:i] + c + url[i+2:]
            return URL
    return "-1"


def get_Feedbacks(URL):
    headers = {
        'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8'
    }
    response = requests.get(URL, headers=headers)
    print(f"Статус ответа сервера: {response.status_code}")
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.prettify()
    return text