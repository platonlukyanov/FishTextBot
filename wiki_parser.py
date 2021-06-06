import requests
from bs4 import BeautifulSoup
from functools import reduce


def get_html(url):
    r = requests.get(url)
    return r.text


def parse_wiki_page(html):
    soup = BeautifulSoup(html, "html.parser")
    map(lambda e: e.decompose(), soup.select("[role='navigation']"))
    title = soup.select("h1#firstHeading")[0].text
    body = reduce(lambda x, y: str(x) + str(y), [item.text for item in soup.select("p")])
    return {
        "title": title,
        "body": body
    }


def get_random_wiki():
    html = get_html(
        "http://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
    return parse_wiki_page(html)


if __name__ == "__main__":
    get_random_wiki()
