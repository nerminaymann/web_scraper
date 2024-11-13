import requests
import pandas as pd
from lxml import html, etree
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        self.LANGUAGE = "en-US,en;q=0.5"
        self.response = None
        self.tree = None

    def setup_session(self):
        self.session.headers['User-Agent'] = self.USER_AGENT
        self.session.headers['Accept-Language'] = self.LANGUAGE
        self.session.headers['Content-Language'] = self.LANGUAGE

    def fetch_html_content(self):
        """Fetch the HTML content of the page and parse with lxml for XPath support."""
        self.setup_session()
        self.response = self.session.get(self.url)
        self.response.raise_for_status()
        self.tree = html.fromstring(self.response.content)  # Use lxml's html parser
        return self.tree


class ContentParser(WebScraper):
    def __init__(self, url):
        super().__init__(url)
        self.html_content = self.fetch_html_content()

    def scrape_items(self,title_xpath=None,description_xpath=None,image_xpath=None):
        """Scrape items with title, description, and image file based on given xPaths."""
        items = []

        titles = self.extract_data(title_xpath) if title_xpath else []
        descriptions = self.extract_data(description_xpath) if description_xpath else []
        images = self.extract_data(image_xpath,is_image=True) if image_xpath else []

        max_len = max(len(titles), len(descriptions), len(images))

        # Combine extracted data into a single dictionary
        for i in range(max_len):
            item = {
                'url': self.url,
                'title': titles[i] if i < len(titles) else None,
                'description': descriptions[i] if i < len(descriptions) else None,
                'image_url': images[i] if i < len(images) else None,
            }
            items.append(item)

        return items

    def extract_data(self, xpath, is_image=False):
        """Extract data from the HTML tree based on an XPath expression."""
        elements = self.html_content.xpath(xpath)
        if is_image:
            print(f'Images are found: {elements}')
            return [
                element.get('src') or element.get('data-src') or element.get('data-lazy')
                for element in elements
                # if isinstance(element,etree._Element) and element.tag == 'img'
            ]
        else:
            return [element.text_content().strip() for element in elements]

    def save_to_csv(self, data, filename='scraped_data.csv'):
        """Save scraped data to a CSV file."""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        return filename

    def save_to_excel(self, data, filename='scraped_data.xlsx'):
        """Save scraped data to an Excel file."""
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        return filename
