# -*- coding:utf-8 -*-
import requests
import MySQLdb
from scrapy.selector import Selector

from scrapyspiders.settings import MYSQL_HOST
from scrapyspiders.settings import MYSQL_DBNAME
from scrapyspiders.settings import MYSQL_USER
from scrapyspiders.settings import MYSQL_PASSWD
from scrapyspiders.settings import MYSQL_CHARSET

conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DBNAME, charset=MYSQL_CHARSET)
cursor = conn.cursor()

# 爬取西刺的免费ip代理（http://www.xicidaili.com/）
def get_xici_ip():
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    response = requests.get('http://www.xicidaili.com/nn/1', headers=headers)
    if response.status_code != 200:
        return
    selector = Selector(text=response.text)
    pagetext = selector.css('.pagination a::text').extract()
    pages = int(pagetext[-2:-1][0])

    for page in range(pages):
        response = requests.get('http://www.xicidaili.com/nn/{0}'.format(page+1), headers=headers)
        if response.status_code == 200:
            selector = Selector(text=response.text)
            ip_trs = selector.css('#ip_list tr')
            ip_list = []
            for tr in ip_trs[1:]:
                td_text = tr.css('td::text').extract()
                ip = td_text[0]
                port = int(td_text[1])
                http_type = td_text[5]
                speed_str = tr.css(".bar::attr(title)").extract()[0]
                if speed_str:
                    speed = float(speed_str.split('秒')[0])
                ip_list.append((ip, port, http_type, speed))

            for ip_info in ip_list:
                #todo:插入http_type的值得为空处理~~
                cursor.execute("insert into proxy_ip(ip,port,http_type,speed) values('{0}',{1},'{2}',{3}) ON DUPLICATE KEY UPDATE http_type='{4}',speed={5}".format(ip_info[0],ip_info[1],ip_info[2], ip_info[3], ip_info[2], ip_info[3]))
                conn.commit()

class GetIp(object):
    # 判断ip是否有效
    def judge_ip(self, ip, port, http_type):
        http_url = 'http://www.baidu.com'
        proxy_url = 'http://{0}:{1}'.format(ip, port)
        proxies = {http_type:proxy_url}
        try:
            response = requests.get(http_url, proxies=proxies)
        except Exception as e:
            self.delete_ip(ip, port)
            return False
        else:
            if response.status_code != 200:
                self.delete_ip(ip, port)
                return False
            else:
                return True

    def delete_ip(self, ip, port):
        sql = '''
            delete from proxy_ip where ip='{0}' and port={1}
        '''.format(ip, port)
        cursor.execute(sql)
        conn.commit()
        return True

    def get_random_ip(self):
        sql = '''
            select ip,port,http_type from proxy_ip where speed<2 and (http_type='HTTP' or http_type='HTTPS') order by rand() limit 1
        '''
        cursor.execute(sql)
        ip_info = cursor.fetchall()
        if len(ip_info) <= 0:
            return False
        ip = ip_info[0][0]
        port = ip_info[0][1]
        http_type = ip_info[0][2]
        result = self.judge_ip(ip, port, http_type)
        if result == True:
            return '{0}://{1}:{2}'.format(http_type, ip, port)
        else:
            return self.get_random_ip()


if __name__ == "__main__":
    # get_xici_ip()
    getip = GetIp()
    random_ip = getip.get_random_ip()
    print(random_ip)