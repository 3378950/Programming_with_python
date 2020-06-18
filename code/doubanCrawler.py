import requests
import re
from lxml import html
import time
import random
import urllib.parse

class MyCrawler:
    def __init__(self, filename):
        self.filename = filename
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4128.3 Safari/537.36'
        }

    def download(self, url: str):
        r = requests.get(url, headers=self.headers)
        return r.text

    def extract(self, content, pattern):
        res = re.findall(pattern, content)
        return res

    def save(self, info):
        with open(self.filename, 'a', encoding='utf-8') as f:
            for item in info:
                f.write(''.join(item) + '\n') 

    def crawl(self, url: str, pattern: str, headers=None):
        if headers:
            self.headers.update(headers)
        content = self.download(url)
        info = self.extract(content, pattern)
        self.save(info)

class doubanCrawler(MyCrawler):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4128.3 Safari/537.36'
        }

    def getTag(self, url: str) -> dict:
        content = self.download(url)
        tree = html.fromstring(content)
        self.tag_dict = dict()
        self.tag_list = tree.xpath('//td/a')
        for tag in self.tag_list:
            # print(tag.text)
            self.tag_dict[tag.text] = urllib.parse.quote(tag.text)
        return self.tag_dict

    def getBooklist(self, encode: str) -> list:
        res = []
        page_id = 1
        last_start = 0
        number = 0
        while 1:
            start_id = 20 * (page_id - 1)
            url = 'https://book.douban.com/tag/{}?start={}&type=T'.format(encode, start_id)
            # print(url)
            content = self.download(url)
            tree = html.fromstring(content)
            if page_id == 1:
                page_links = tree.xpath("//div[@class='paginator']/a[last()]/@href")
                if page_links:
                    # print(page_links)
                    last_start = int(re.findall("start=(\d+)", page_links[0])[0])
                    print('Last start id = ', last_start)
            book_list = tree.xpath('//li[@class=\'subject-item\']')
            for book in book_list:
                bookname = book.xpath('.//h2/a')[0].text.strip()
                # bookurl = book.xpath('.//h2/a')[0].attrib['href']
                # bookinfo = book.xpath('.//div[@class=\'pub\']')[0].text.strip()
                # bookintro = 'N/A'
                # if book.xpath(".//div[@class='info']/p"):
                #     bookintro = book.xpath(".//div[@class='info']/p")[0].text.strip()
                number += 1
                tmp = str(number) + ': ' + bookname
                # print(tmp)
                res.append(tmp)
            page_id += 1
            if start_id == last_start:
                break
            time.sleep(1)
        return res

    def save(self, tag: str) -> None:
        filename = tag + ".txt"
        print(filename)
        with open(filename, 'a', encoding='utf-8') as f:
            res = self.getBooklist(self.tag_dict[tag])
            for lin in res:
                f.write(lin + '\n')
        
mytest = doubanCrawler()
res = mytest.getTag('https://book.douban.com/tag/?view=type&icn=index-sorttags-all')
# print(res)
# print(mytest.getBooklist(res['小说']))
mytest.save('神经网络')

