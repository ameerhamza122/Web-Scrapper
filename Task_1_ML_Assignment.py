import os
import requests
import re
import sys
from bs4 import BeautifulSoup


def get_page():
    global url

    url = input("Enter url of a medium article: ").strip()

    if not re.match(r'https?://medium.com/', url):
        print("Please enter a valid Medium article URL")
        sys.exit(1)

    # 🔑 IMPORTANT FIX:
    # Use Jina AI reader instead of Medium directly
    reader_url = "https://r.jina.ai/" + url

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    res = requests.get(reader_url, headers=headers, timeout=15)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def collect_text(soup):
    text = f"url: {url}\n\n"

    paragraphs = soup.find_all("p")
    for p in paragraphs:
        text += p.get_text(strip=True) + "\n\n"

    return text


def save_file(text):
    if not os.path.exists("scraped_articles"):
        os.mkdir("scraped_articles")

    name = url.split("/")[-1]
    fname = f"scraped_articles/{name}.txt"

    with open(fname, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"File saved in directory {fname}")


if __name__ == "__main__":
    text = collect_text(get_page())
    save_file(text)
