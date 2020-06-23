import re

from selenium import webdriver
from bs4 import BeautifulSoup as bs
from time import sleep
import os
from datetime import datetime
from month import month_in_words
from url_list import news_link


class ScrapeNews:
    def __init__(self, url):
        self.browser = webdriver.Chrome()
        self.url = url
        self.date = None

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
        self.get_current_date()
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
            text_only = [title.text]

            for paragraph in page_content:
                text_only.append(paragraph.text.strip())

            return text_only

    def get_current_date(self):
        date = datetime.now()
        year = int(date.year)
        month = int(date.month)
        day = int(date.day)

        self.date = '%02d.%02d.%04d' % (day, month, year)
        # self.date = '20.05.2020'

    def create_file(self, directory):
        exist = os.path.exists(directory)
        if not exist:
            os.mkdir(directory)

    def validate_title(self, title):
        invalid_symbols = re.compile(r'[\\/:*?"<>|]')

        return invalid_symbols.sub('', title)

    def generate_dir(self, text_only):
        title = self.validate_title(text_only[0])
        news_content = text_only[1:]
        dir = 'C:\\Users\\Autumn\\Documents\\News\\'
        self.create_file(dir)
        dir = dir + str(self.date)
        self.create_file(dir)
        category = str(self.url.split('/')[-1])
        dir = dir + '\\' + category
        self.create_file(dir)
        dir = dir + '\\' + str(title) + '.txt'

        return dir

    def write_file(self, text_only, directory):
        title = text_only[0]
        news_content = text_only[1:]
        file = open(directory, 'w+')
        file.write(title)
        file.write('\n' * 2)
        for text in news_content:
            file.write(text)
            print(text)
            file.write('\n')

        if not file.closed:
            file.close()

    def main(self):
        href = self.get_page_link()
        for link in href:
            try:
                text_only = self.get_text(link)
                print(text_only)
                directory = self.generate_dir(text_only)

                self.write_file(text_only, directory)
            except (UnicodeEncodeError, TypeError) as ue:
                print(ue)
            except:
                continue

        self.browser.quit()


if __name__ == '__main__':
    for link in news_link:
        obj = ScrapeNews(link)
        obj.main()
