import selenium.webdriver as webdriver
from bs4 import BeautifulSoup
from parse import parse_with_openai

import time

def scape_website(website):
    print("Launch chroma browser...")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(website)
        print("Page loaded...")
        html = driver.page_source
        time.sleep(3)

        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content,  "html.parser")
    body_content = soup.body

    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content,  "html.parser")

    for script_or_stle in soup(["script", "style"]):
        script_or_stle.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join([
        line.strip() for line in cleaned_content.split("\n") if line.strip()])
    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)
        ]

if __name__ == "__main__":
    url = "https://www.google.com"
    html = scape_website(website=url)
    body_content = extract_body_content(html)
    # print(body_content)
    # print("=" * 100)
    cleaned_content = clean_body_content(body_content)
    # print(cleaned_content)
    # print("=" * 100)
    dom_content = split_dom_content(cleaned_content)
    print(dom_content)

    # parse_with_openai(dom_content, "Gmail")