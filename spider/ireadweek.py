import threading
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
            print(self.queue.get())
