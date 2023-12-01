from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser

results = []

#parsing function for fox news 
def parse_item(html_page, base_url):
    html = HTMLParser(html_page)
    data = html.css("section.collection.collection-article-list.has-load-more article.article")


    for item in data:
        title_element = item.css_first("div.info header.info-header h4.title a")
        article_url = title_element.attributes['href'] if title_element else None
        title_text = title_element.text() if title_element else None

        # Check if the article_url is not None and is a relative path
        if article_url and not article_url.startswith('http'):
            # Construct the full URL by joining the base_url and the relative article_url
            article_url = base_url.rstrip('/') + '/' + article_url.lstrip('/')

        meta_element = item.css_first("div.info header.info-header div.meta div")
        category = meta_element.css_first("span.eyebrow a").text() if meta_element else None
        time = meta_element.css_first("span.time").text() if meta_element else None

        content_element = item.css_first("div.info header.info-header + div.content p.dek")
        content_text = content_element.text() if content_element else None

        article = {
            "title": title_text,
            "article_url": article_url,
            "category": category,
            "time": time,
            "content": content_text
        }
        results.append(article)

    return results

#this is the code that runs through everything 
# def main():
#     base_url = "https://www.foxnews.com"
#     url = "https://www.foxnews.com/category/world/global-economy"  # Replace with the actual URL
#     output_file_path = "article_url_title_data.py"
    
#     with sync_playwright() as pw:
#         browser = pw.chromium.launch(headless=False)
#         page = browser.new_page()
#         page.goto(url, wait_until="networkidle")

#         while True:
#             print(parse_item(page.content(), base_url))

#             # Locate the "Show More" button
#             show_more_button = page.locator(".button.load-more")

#             # Check if the button is disabled
#             if show_more_button.is_disabled():
#                 break

#             # Scroll to the "Show More" button
#             show_more_button.scroll_into_view_if_needed()

#             # Click the "Show More" button
#             show_more_button.click()

#             # Wait for the page to finish loading
#             page.wait_for_load_state("networkidle", timeout=30000)

#     with open(output_file_path, "w", encoding="utf-8") as output_file:
#         output_file.write("result_data = ")
#         output_file.write(repr(results))

# if __name__ == "__main__":

#     main()


#this code is limited to 5 pages

def main():
    base_url = "https://www.foxnews.com"
    url = "https://www.foxnews.com/category/world/global-economy"  # Replace with the actual URL
    output_file_path = "output_data.py"  # Specify the desired output file path
    max_pages = 5  # Set the maximum number of pages to process

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        results = []
        page_counter = 0  # Initialize the page counter

        while page_counter < max_pages:
            results.extend(parse_item(page.content(), base_url))
            page_counter += 1  # Increment the page counter

            # Locate the "Show More" button
            show_more_button = page.locator(".button.load-more")

            # Check if the button is disabled
            if show_more_button.is_disabled():
                break

            # Scroll to the "Show More" button
            show_more_button.scroll_into_view_if_needed()

            # Click the "Show More" button
            show_more_button.click()

            # Wait for the page to finish loading
            page.wait_for_load_state("networkidle", timeout=30000)

    # Save the results to a Python file
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write("result_data = ")
        output_file.write(repr(results))

    

if __name__ == "__main__":
    main()

