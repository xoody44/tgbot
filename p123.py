import json
from bs4 import BeautifulSoup
import requests
import lxml


def first_news():
    url = "https://gimn19-r45.gosuslugi.ru/roditelyam-i-uchenikam/novosti/"
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    article_pages = soup.find_all(class_="object-item")
    news_dict = {}

    for article in article_pages:
        try:
            article_image = f'https://gimn19-r45.gosuslugi.ru{article.find("div", class_="item-image").find("div", class_="image").find("a").find("img").get("src")}'
            article_title = article.find("h2", class_="object-item-title tpl-text-header2").find("a").text.strip()
            article_date = article.find("span", class_="item-date tpl-text-alt").text.strip()
            article_url = f'https://gimn19-r45.gosuslugi.ru{article.find("h2", class_="object-item-title tpl-text-header2").find("a").get("href")}'
        except AttributeError:
            # print(f"В этом объекте случилась проблема. См. его ниже:")
            # print(article)
            continue

        article_id = article_url.split("/")[-1]
        article_id = article_id[:-5]

        news_dict[article_id] = {
            "article_image": article_image,
            "article_title": article_title,
            "article_date": article_date,
            "article_url": article_url
        }
        # print(f"{article_title} | {article_date} | {article_url}")

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    url = "https://gimn19-r45.gosuslugi.ru/roditelyam-i-uchenikam/novosti/"
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    article_pages = soup.find_all(class_="object-item")

    fresh_news = {}
    for article in article_pages:
        try:
            article_url = f'https://gimn19-r45.gosuslugi.ru{article.find("h2", class_="object-item-title tpl-text-header2").find("a").get("href")}'
        except AttributeError:
            #print(f"В этом объекте случилась проблема. См. его ниже:")
            #print(article)
            continue
        article_id = article_url.split("/")[-1]
        article_id = article_id[:-5]
        if article_id in news_dict:
            continue
        else:
            try:
                article_title = article.find("h2", class_="object-item-title tpl-text-header2").find("a").text.strip()
                article_image = f'https://gimn19-r45.gosuslugi.ru{article.find("div", class_="item-image").find("div", class_="image").find("a").find("img").get("src")}'
                article_date = article.find("span", class_="item-date tpl-text-alt").text.strip()
                article_url = f'https://gimn19-r45.gosuslugi.ru{article.find("h2", class_="object-item-title tpl-text-header2").find("a").get("href")}'
            except AttributeError:
                #print(f"В этом объекте случилась проблема. См. его ниже:")
                #print(article)
                continue

            news_dict[article_id] = {
                "article_image": article_image,
                "article_title": article_title,
                "article_date": article_date,
                "article_url": article_url
            }
            fresh_news[article_id] = {
                "article_image": article_image,
                "article_title": article_title,
                "article_date": article_date,
                "article_url": article_url
            }
    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)
    return fresh_news


def main():
    first_news()
    #print(check_news_update())


if __name__ == '__main__':
    main()
