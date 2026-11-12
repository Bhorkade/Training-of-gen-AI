
import json
import requests

from pathlib import Path
from html.parser import HTMLParser


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "startup_india_pages.json"

PAGES = [
    {
        "title": "Startup India Homepage",
        "url": "https://www.startupindia.gov.in/"
    },
    {
        "title": "DPIIT Recognition",
        "url": "https://www.startupindia.gov.in/content/sih/en/startupgov/startup_recognition_page.html"
    },
    {
        "title": "Startup India FAQ",
        "url": "https://www.startupindia.gov.in/content/sih/en/faqs.html"
    },
    {
        "title": "Startup India Schemes",
        "url": "https://www.startupindia.gov.in/content/sih/en/startup-scheme.html"
    }
]


class TextParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self.skip = False

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.text.append(data.strip())


def fetch_page(page):

    try:
        print("Downloading:", page["title"])

        response = requests.get(
            page["url"],
            timeout=(5, 30),
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        parser = TextParser()
        parser.feed(response.text)

        content = " ".join(parser.text)

        if not content:
            print("No readable content:", page["url"])
            return None

        print("Downloaded successfully:", page["title"])

        return {
            "title": page["title"],
            "url": page["url"],
            "description": content
        }

    except requests.exceptions.Timeout:
        print("Request timed out:", page["url"])

    except requests.exceptions.RequestException as error:
        print("Request error:", error)

    except (ValueError, TypeError) as error:
        print("Processing error:", error)

    return None


def fetch_data():

    records = []

    for page in PAGES:
        result = fetch_page(page)

        if result:
            records.append(result)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

    print("\nFetch completed!")
    print("Total pages configured:", len(PAGES))
    print("Successfully downloaded:", len(records))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    fetch_data()
