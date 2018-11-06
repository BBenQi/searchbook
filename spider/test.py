import queue

from spider.ireadweek import IreadSpider

urls = queue.Queue()

for i in range(100, 200):
    urls.put('http://ireadweek.com/index.php/bookInfo/' + str(i) + '.html')

for i in range(100):
    thread = IreadSpider(urls)
    thread.start()
