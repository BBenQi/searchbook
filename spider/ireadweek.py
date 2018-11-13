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

    def parse(self, html):
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

        print(book_name[0].string + '&&&' + author[0].string + '&&&' + book_type[0].string + '&&&' + download[0][
            'href'] + '&&&' + book_content[0].string)
        # print('下载地址', download[0]['href'])
        # print('作者', author[0].string)
        # print('书籍名称', book_name[0].string)
        # print('类型', book_type[0].string)
        # print('简介', book_content[0].string)
        # print("*********************************")

        sql = '''INSERT INTO book(book_name, book_author, book_type, download_link, book_content) VALUES('%s','%s',
        '%s','%s','%s') '''(book_name[0].string, author[0].string, book_type[0].string, download[0]['href'],
                            book_content[0].string)
        print(sql)
        self.cursor.execute(sql)
        db.commit()
