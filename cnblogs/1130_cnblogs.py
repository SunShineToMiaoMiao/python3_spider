
import logging;logging.basicConfig(level=logging.INFO)
import urllib.parse
import urllib.request
import re
from bs4 import BeautifulSoup

import os, datetime, time, json
from docx import Document
from docx.shared import Pt, RGBColor, Inches
# from docx.enum.text import WD_BREAK_TYPE, WD_BREAK, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

import keyword


# region 获取目录列表

'获取html'
def getHtml(url,values):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
    headers = {'User-Agent':user_agent}
    data = urllib.parse.urlencode(values)
    api = url + '?' + data
    logging.info('请求数据的api：%s' % api)
    response_result = urllib.request.urlopen(api).read()
    html = response_result.decode('utf-8')
    return html


'组织api'
def request_cnblogs(index):
    url = 'http://www.cnblogs.com/mvc/AggSite/PostList.aspx'

    value = {
        'CategoryId': 808,
        'CategoryType': 'SiteHome',
        'ItemListActionName': 'PostList',
        'PageIndex': index,
        'ParentCategoryId': 0,
        'TotalPostCount': 4000
    }
    rs = getHtml(url, value)
    return rs


def self_find_all(item, attr, c):
    return item.find_all(attr, attrs={'class':c}, limit=1)


'解析最外层'
def blog_parser(index):
    logging.info('提取出html中的所需要的所有div：-------')
    cnblogs = request_cnblogs(index)
    soup = BeautifulSoup(cnblogs, 'html.parser')
    all_div = soup.find_all('div',attrs={'class': 'post_item_body'}, limit=20)

    logging.info('共提取出%s个包含链接的div：-------' % len(all_div))
    blogs = []
    for item in all_div:
        blog = analyzeBlog(item)
        blogs.append(blog)
    return blogs


'解析每个内容div'
def analyzeBlog(item):
    rs = {}
    a_title = self_find_all(item, 'a', 'titlelnk')
    if a_title:
        # 博客标题
        rs['title'] = a_title[0].string
        rs['href'] = a_title[0]['href']
    p_summary = self_find_all(item, 'p', 'post_item_summary')
    if p_summary:
        rs['summary'] = p_summary[0].text
    footers = self_find_all(item, 'div', 'post_item_foot')
    footer = footers[0]
    rs['author'] = footer.a.string
    rs['author_url'] = footer.a['href']
    str2 = footer.text
    time = re.findall(r"发布于 .+? .+? ", str2)
    rs['create_time'] = time[0].replace('发布于 ', '')
    comment_str = self_find_all(footer, 'span', 'article_comment')[0].a.string
    rs['comment_num'] = re.search(r'\d+', comment_str).group()
    view_str = self_find_all(footer, 'span', 'article_view')[0].a.string
    rs['view_num'] = re.search(r'\d+', view_str).group()
    logging.info('解析到的单个div：%s' % rs)
    return rs


'创建目录'
def create_dir():
    dir = datetime.datetime.now().strftime('%Y%m%d%H%M')
    path = os.path.join('doc', dir)
    if os.path.exists(path):
        # os.remove(path)
        return path
    else:
        os.mkdir(path)
        return path


# '写入txt'
def save_json_txt(list_name, file_path):

    # 一定要加上ensure_ascii=False, 才能保存为汉字
    data = json.dumps(list_name, ensure_ascii=False)
    with open(file_path, 'w+', encoding='utf-8') as f:
        f.write(data)


'博客列表'
def save_blogs():
    blogs = []
    for i in range(1, 2):
        logging.info('请求：request for -----' + str(i))
        blogs = blog_parser(i)
        dir_path = create_dir()
        save_json_txt(blogs, os.path.join(dir_path, 'blog_' + str(i) +'.txt'))
        logging.info('第' + str(i) + '页已保存为txt文件')

    return 'success'


# '创建txt文件'
def save_str_txt(data, file_path):
    fp = open(file_path, 'w+', encoding='utf-8')
    try:
        logging.info('保存的数据：%s' % data)
        fp.write(data)
    finally:
        fp.close()





if __name__ == '__main__':
    save_blogs()













