import threading
import requests
from bs4 import BeautifulSoup
from dao.cursor_getter import db


class IreadSpider(threading.Thread):

    def __init__(self, queue):
        """
        :param queue: url队列 Queue类型
        """
        threading.Thread.__init__(self)
        self.queue = queue
        self.cursor = db.cursor()

    def run(self):
        while not self.queue.empty():
            url = self.queue.get()
            html = requests.get(url).text
            try:
                self.parse(html)
            except:
                continue

    @staticmethod
    def parse(html):
        soup = BeautifulSoup(markup=html)
        download = soup.select('body > div > div > div.hanghang-za > div.hanghang-box > div.hanghang-shu-content-btn '
                               '> a')
        author = soup.select('body > div > div > div.hanghang-za > div.hanghang-shu-content > '
                             'div.hanghang-shu-content-font > p:nth-of-type(1)')
        book_name = soup.select('body > div > div > div.hanghang-za > div:nth-of-type(1)')
        book_type = soup.select('body > div > div > div.hanghang-za > div.hanghang-shu-content > '
                                'div.hanghang-shu-content-font > p:nth-of-type(2)')
        book_content = soup.select('body > div > div > div.hanghang-za > div.hanghang-shu-content > '
                                   'div.hanghang-shu-content-font > p:nth-of-type(5)')

        print('下载地址', download[0]['href'])
        print('作者', author[0].string)
        print('书籍名称', book_name[0].string)
        print('类型', book_type[0].string)
        print('简介', book_content[0].string)
        print("*********************************")
