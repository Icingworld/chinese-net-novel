import requests
from bs4 import BeautifulSoup
import os
import time
import sys

# ——————————————————————————————————————————————————————————————————
# BeautifulSoup需要安装html5lib、lxml解析                              |
# 使用时修改Path为小说保存路径                                           |
# By 蒋梓文 2021-3-15                                                 |
# 关于为什么显示开始下载后需要等待很长时间，因为需要把所有章节的信息放入多个列表  |
# 功能太多导致有时候运行速率比较慢                                        |
# ——————————————————————————————————————————————————————————————————

Path = "/Users/apple/Desktop/小说/"
soup = BeautifulSoup
url = "http://www.xbiquge.la/modules/article/waps.php"
host = "http://www.xbiquge.la"

keys = {
    "key1": "章",
    "key2": "结局",
    "key3": "番",
    "key4": "1",
    "key5": "2",
    "key6": "3",
    "key7": "4",
    "key8": "5",
    "key9": "6",
    "key10": "7",
    "key11": "8",
    "key12": "9",
    "key13": "序"
}

global data
global book_name
global name__
global now__
global start_time

book_names = []
book_urls = []
book_authors = []
book_counts = []
chapter_hrefs = []
chapter_names = []

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://www.xbiquge.la",
    "Host": "www.xbiquge.la",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "11",
    "Accept-Encoding": "gzip, deflate",
    "Cookie": "_abcde_qweasd=0; _abcde_qweasd=0; bdshare_firstime=1615377374914",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/11.1.2 Safari/605.1.15",
    "Referer": "http://www.xbiquge.la/",
    "Accept-Language": "zh-cn"
}


def name_():
    global data
    global book_name
    print("请输入书名：")
    book_name = input()
    data = {"searchkey": book_name}


def choose_book(search_result_):
    bs_search_result = soup(search_result_.content, "lxml")
    book_infos = bs_search_result.find_all(name="tr")
    for book_info in book_infos[1:]:
        book_name1 = book_info.find("a")
        book_names.append(book_name1.string)
        book_url = book_info.find("a").get("href")
        book_urls.append(book_url)
        book_author = book_info.find_all("td")[2]
        book_authors.append(book_author.string)
    if book_names is None:
        pass
    else:
        for check in (book_names + book_authors):
            if book_name not in check:
                pass
            else:
                print("——————搜索结果：——————\n")
                for name in book_names:
                    count = book_names.index(name)
                    book_counts.append(count)
                    print(str(count) + "  书籍名：" + name + "  作者：" + book_authors[count])
                print("\n——————输入序号以选择书籍：——————")
                choose_count = input()
                print("——————加载中···——————")
                if 0 <= int(choose_count) <= book_names.index(book_names[-1]):
                    book_choose_url = book_urls[int(choose_count)]
                    with open("log.txt", "a", encoding="utf-8") as f6:
                        f6.write(book_names[int(choose_count)] + "\n")
                    make_dir(choose_count)
                    book_web_page(book_choose_url)
                else:
                    print("——————错误，请检查输入——————")
                    book_names.clear()
                    book_urls.clear()
                    book_authors.clear()
                    book_counts.clear()
                    choose_book(search_result_)


def book_web_page(book_choose_url_):
    web_page = requests.get(book_choose_url_)
    web_page_soup = soup(web_page.content, "lxml")
    read_(web_page_soup)


def read_(page_soup):
    global start_time
    chapter_lists = page_soup.find_all(name="dd")
    for chapter_list in chapter_lists:
        href_ = chapter_list.find("a").get("href")
        chapter_hrefs.append(host + href_)
        chapter_name = chapter_list.find("a")
        chapter_names.append(chapter_name.string)
    start_time = time.time()
    print("——————正在检索起始章节···——————")
    if not os.path.exists(Path + name__ + "/" + "log.txt"):
        with open(Path + name__ + "/" + "log.txt", "w") as f3:
            f3.close()
            start_num = 0
    else:
        with open(Path + name__ + "/" + "log.txt", "r") as f4:
            last_line = f4.readlines()[-1]
            start_num = chapter_names.index(last_line) + 1
    print("——————开始下载——————")
    print("——————本书共 " + str(len(chapter_names)) + "个加载项——————")
    down_novel(start_num)


# 下载正文
def down_novel(chapter_now_):
    global now__
    book_names.clear()
    book_urls.clear()
    book_authors.clear()
    book_counts.clear()
    try:
        for links in chapter_hrefs[chapter_now_:]:
            now__ = chapter_hrefs.index(links)
            novel_content = requests.get(links)
            content_soup = soup(novel_content.content, "html5lib")
            title = content_soup.find("h1").string
            wrong = "503 Service Temporarily Unavailable"
            if wrong in title:
                chapter_now_ = now__
                time.sleep(10)
                down_novel(chapter_now_)
            else:
                for value in keys.values():
                    if value not in title:
                        pass
                    else:
                        content = content_soup.find_all(name="div", id="content")
                        content1 = str(content)[19:-189]
                        content2 = content1.replace("<br/>", "")
                        with open(Path + name__ + "/" + name__ + ".txt", "a", encoding="utf-8") as f:
                            f.write(chapter_names[now__] + "\n")
                            f.write(content2 + "\n\n\n\n")
                        with open(Path + name__ + "/" + "log.txt", "a", encoding="utf-8") as f1:
                            f1.write("\n" + chapter_names[now__])
                            print("已下载：" + chapter_names[now__])
                        break
        end_time = time.time()
        time_ = end_time - start_time
        print("——————《" + name__ + "》已下载完成——————")
        print("用时： " + str(time_) + "  s")
        sys.exit(0)
    except (ConnectionResetError, requests.exceptions.ConnectionError):
        down_novel(now__)


def make_dir(count):
    global name__
    name__ = book_names[int(count)]
    if not os.path.exists(Path + name__ + "/"):
        print("——————正在创建目录···——————")
        os.makedirs(Path + name__ + "/")
    else:
        pass


def run():
    name_()
    search_result = requests.post(url=url, headers=headers, data=data)
    choose_book(search_result)


def read():
    try:
        with open("log.txt", "r") as f5:
            print("上次下载的书籍为：" + f5.readlines()[-1])
    except FileNotFoundError:
        with open("log.txt", "w+") as f6:
            f6.close()


if __name__ == "__main__":
    read()
    run()
