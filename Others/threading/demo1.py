# -*- coding: utf-8 -*-
__author__ = 'yunshu'

import threading
from threading import Thread
import time
import random


def worker_func():
    print('start %s' % (threading.current_thread()))
    random.seed()
    time.sleep(random.random())
    print('finish %s' % (threading.current_thread()))


# 创建十个线程
def mk_thread(count=5):
    for i in range(count):
        t = Thread(target=worker_func)
        t.start()


'''
运行结果：
start <Thread(Thread-1, started 123145306509312)>
 start <Thread(Thread-2, started 123145310715904)>
start <Thread(Thread-3, started 123145314922496)>
start <Thread(Thread-4, started 123145319129088)>
start <Thread(Thread-5, started 123145323335680)>
finish <Thread(Thread-1, started 123145306509312)>
finish <Thread(Thread-5, started 123145323335680)>
finish <Thread(Thread-4, started 123145319129088)>
finish <Thread(Thread-3, started 123145314922496)>
finish <Thread(Thread-2, started 123145310715904)>
'''
if __name__ == '__main__':
    mk_thread(5)