from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from output_data import result_data



full_articles = []

def parse_page(html_article_page):
    html = HTMLParser(html_article_page)
    art_data = html.css("article.article-wrap.has-video")

    for item in art_data:
        title_element = item.css_first("header.article-header div.article-meta.article-meta-upper h1.headline")
        sub_title_element = item.css_first("header.article-header div.article-meta.article-meta-upper h2.sub-headline.speakable")
        h1_text = title_element.text() if title_element else ""
        h2_text = sub_title_element.text() if sub_title_element else ""

        article = {
            "title": h1_text,
            "sub-title": h2_text
        }

        full_articles.append(article)

    return full_articles


def get_full_articles(result_data):

    for result in result_data:
        url = result["article_url"]

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")

            print(parse_page(page.content()))

get_full_articles(result_data)