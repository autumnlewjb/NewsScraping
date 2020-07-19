import re
from pathlib import Path

from selenium import webdriver
from bs4 import BeautifulSoup as bs
from time import sleep
import os
from datetime import datetime
from news_scraping.month import month_in_words
from news_scraping.url_list import news_link
from news_scraping.notification import Notification


def create_file(directory):
    directory = str(directory)
    exist = os.path.exists(directory)
    if not exist:
        os.mkdir(directory)


def validate_title(title):
    invalid_symbols = re.compile(r'[\\/:*?"<>|]')

    return invalid_symbols.sub('', title)


def write_file(text_only, directory):
    title = text_only['title']
    news_content = text_only['content']
    file = open(directory, 'w+')
    file.write(title)
    file.write('\n' * 2)
    for text in news_content:
        file.write(text)
        print(text)
        file.write('\n')

    if not file.closed:
        file.close()


class ScrapeNews:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.url = None
        self.date = datetime.now()
        self.main_directory = Path().home() / 'Documents' / 'News'
        self.notify = Notification()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        year = int(date.year)
        month = int(date.month)
        day = int(date.day)

        self._date = '%02d.%02d.%04d' % (day, month, year)
        # self.date = '20.05.2020'

    def get_page_link(self):
        main_page = "{}?page={}"
        page = 0
        true_href = []
        while True:
            self.browser.get(main_page.format(self.url, page))
            sleep(2)
            source = self.browser.page_source
            soup = bs(source, 'lxml')
            div = soup.find('div', class_='article-listing')
            a_list = div.find_all('a')
            post_time = div.find_all('span', class_='created-ago')
            href = []
            i = 0

            while i < len(a_list):
                posting_time = post_time[i].text.split(' ')
                if posting_time[-1] == 'ago' and posting_time[-2] == 'hour' or posting_time[-2] == 'hours':
                    href.append('https://www.nst.com.my/' + str(a_list[i].get('href')))

                i += 1

            if len(href) == 0:
                break
            else:
                true_href.extend(href)
            print(href)
            page += 1

        return true_href

    def get_text(self, href):
        self.browser.get(str(href))
        source = self.browser.page_source
        soup = bs(source, 'lxml')
        article_date = soup.find('div', class_='article-meta mb-2 mb-lg-0')

        # process article_date below
        article_date = article_date.text.strip().split(" ")
        # ['April', '30,', '2020', '@', 5:05pm]

        day = int(article_date[-4].replace(',', ''))
        year = int(article_date[-3])
        month = month_in_words[article_date[-5]]

        news_date = "%02d.%02d.%04d" % (day, month, year)

        if news_date == self.date:
            title = soup.find('h1', class_='page-title mb-2')
            content_div = soup.find('div', class_='field field-body')
            page_content = content_div.find_all('p')
            page_content = [paragraph.text.strip() for paragraph in page_content]
            text_only = dict(title=title.text, content=page_content)

            return text_only

    def generate_dir(self, title):
        if title:
            title = validate_title(title)
            create_file(self.main_directory)
            directory = self.main_directory / str(self.date)
            create_file(directory)
            self.notify.set_directory(directory)
            category = str(self.url.split('/')[-1])
            directory = directory / category
            create_file(directory)
            directory = directory / (str(title) + '.txt')

            return str(directory)

    def each_category(self):
        number_of_news = 0
        href = self.get_page_link()
        for link in href:
            try:
                text_only = self.get_text(link)
                print(text_only['title'])
                print(text_only['content'])
                directory = self.generate_dir(text_only['title'])

                write_file(text_only, directory)
                number_of_news += 1
            except (UnicodeEncodeError, TypeError) as ue:
                print(ue)
            except:
                continue

        self.notify.get_total_news(number_of_news)

    def main(self):
        for link in news_link:
            self.url = link
            self.each_category()
        self.browser.quit()
        self.notify.send_note()


if __name__ == '__main__':
    obj = ScrapeNews()
    obj.main()
