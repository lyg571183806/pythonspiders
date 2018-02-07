__author__ = 'yunshu'

import hashlib

def get_md5(url):
    #如果是unicode字符串，则进行utf-8编码
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == '__main__':
    print(get_md5('http://www.jobbole.com'))