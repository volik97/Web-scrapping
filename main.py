import requests
import bs4
from fake_useragent import UserAgent
from tqdm import tqdm


KEYWORDS = ['дизайн', 'фото', 'web', 'python']
url = 'https://habr.com/ru'
ua = UserAgent()
HEADERS = {'User-Agent': ua.random}


def _get_html_text(url_address):
    '''Получаем HTML-text'''
    response = requests.get(url_address, headers=HEADERS)
    text = response.text
    return text

def get_url_articles(text):
    '''Получаем URL статей с главной страницы'''
    url_articles_list = []
    textBS = bs4.BeautifulSoup(text, features="html.parser")
    articles = textBS.find_all('article')
    for article in articles:
        preview_info = article.find(class_='tm-article-snippet')
        href = preview_info.find('a', class_="tm-article-snippet__title-link").get('href')
        url_article = url + href[3:]
        url_articles_list.append(url_article)
    return url_articles_list

def check_article(url_articles_list):
    '''Проверка на содержание статьями ключевых слов'''
    article_list = set()
    for url in tqdm(url_articles_list):
        text = _get_html_text(url)
        textBS = bs4.BeautifulSoup(text, features="html.parser")
        article = textBS.find('article', class_="tm-article-presenter__content tm-article-presenter__content_narrow")
        words_article = list(words.text.split() for words in article)
        for words in words_article:
            for word in words:
                if word.lower() in KEYWORDS:
                    datetime = article.find('time').get('title')
                    title = article.find('h1').find('span').text
                    article_title_url_datetime = f'{datetime} "{title}" \n{url}\n\n'
                    article_list.add(article_title_url_datetime)
    return print(f'Найдено {len(article_list)} совпадений!\n', *article_list)

def main():
    check_article(get_url_articles(_get_html_text(url)))

if __name__ == '__main__':
    main()
