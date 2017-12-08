import logging;logging.basicConfig(level=logging.INFO)
import urllib.parse
import urllib.request
import http.cookiejar as cookielib
import re, requests
from bs4 import BeautifulSoup
from PIL import Image

import os, datetime, time, json
from docx import Document
from docx.shared import Pt, RGBColor, Inches
# from docx.enum.text import WD_BREAK_TYPE, WD_BREAK, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import keyword


# '根据img_url保存图片文件'
def save_img_file(img_url, dir_path):
    mirS = str(datetime.datetime.now().microsecond)
    f_str = str(time.strftime('%H_%M_%S', time.localtime()) + '__' + mirS + '.png')
    file_path = os.path.join(dir_path, f_str)
    con = urllib.request.urlopen(img_url).read()
    with open(file_path, 'wb') as f:
        f.write(con)
    return file_path

# '写入txt--str'
def save_str_txt(data, file_path):
    fp = open(file_path, 'w+', encoding='utf-8')
    try:
        fp.write(data)
    finally:
        fp.close()

    return file_path




# '创建目录'
def create_dir():
    dir = datetime.datetime.now().strftime('%Y%m%d%H%M')
    path = os.path.join('doc', dir)
    if os.path.exists(path):
        # os.remove(path)
        return path
    else:
        os.mkdir(path)
        return path

def get_html(url):

    response_result = urllib.request.urlopen(url).read()

    html = response_result.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    dir_path = create_dir()
    # 问题
    question = soup.find('h1',class_='QuestionHeader-title').text

    con = soup.find('div', attrs={'class':'List'})
    # list_tags = con.find_all('div', attrs={'class': 'List-item'})

    # logging.info('网页html：%s' % soup)
    # logging.info('listItem的个数：%s' % len(list_tags))

    answer_tags = con.find_all('div', attrs={'class':'ContentItem AnswerItem'})
    logging.info('问题《%s》共有%s个回答' % (question, len(answer_tags)))
    answer_arr = []
    index = 1
    for a in answer_tags:
        item = get_each_answers(a, index)
        answer_arr.append(item)
        index += 1

    save_str = '\n'.join(answer_arr)
    file_path = save_str_txt(save_str, os.path.join(dir_path, question + '.txt'))
    logging.info('已保存为txt，路径：%s' % file_path)


def get_each_answers(answer, index, praise_num, author_name):
    logging.info('记录第%s个回答' % index)

    dir_path = create_dir()
    each_str = ""

    # 回答赞数
    each_str += "\n=====第" + str(index) + "个回答，知乎用户："+ author_name +"，赞数：" + str(praise_num)\
        + "=============================" + "\n"

    # 回答内容
    # 找到所有子节点
    answer_tags = BeautifulSoup(answer, 'html.parser')
    child_tags = answer_tags.find_all(lambda x: x.name != '', recursive=False)
    # logging.info('child_tags[0]:%s' % len(child_tags[0]))
    if len(child_tags[0]) > 1:
        for t in child_tags[0].contents:
            tag_name = t.name

            if tag_name:
                # 判断是否有figure标签，若存在则下载图片
                if tag_name == 'figure':
                    img_url = t.find_all('img', class_='lazy')[0].attrs["data-actualsrc"]
                    img_name = save_img_file(img_url, dir_path)
                    logging.info('已保存第%s个回答的图片，路径为：%s' % (index, img_name))
                elif re.match('br', tag_name):
                    each_str += '\n'
                elif tag_name == 'p':
                    each_str += t.text + '\n'
                elif tag_name == 'blockquote':
                    if re.match('br', t.string):
                        each_str += '\n'
                    else:
                        each_str += t.text + '\n'
            else:
                each_str += t
    else:
        each_str += answer_tags.text

    return each_str


# 请求头部
header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
        'Host': 'www.zhihu.com'
    }

# 根据问题id获取回答的json数据
def get_html_by_json(question_id):

    question_url = 'https://www.zhihu.com/question/'+ str(question_id)
    header2 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
        'authorization': 'Bearer Mi4xaGJSY0FnQUFBQUFBa0lLQk4yRE9DeGNBQUFCaEFsVk5QbkFYV3dDcDBjOHgzdWUwWTZxUXZJYVFzQlpRNDBqNTVR|1512710718|7035ad267faf29579aba4a3049d2992667ba7142',
        'Referer': question_url
    }

    offset = 0

    logging.info('访问的【知乎问答】链接：%s' % question_url)
    while(offset < 100):
        logging.info('下一个txt文件：%s' % offset)

        # 长长一串是include参数
        api = 'https://www.zhihu.com/api/v4/questions/' \
              + str(question_id) + \
              '/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics' \
              '&offset='+str(offset)+'&limit=20&sort_by=default'
        response_json = requests.get(api,headers=header2).json().get('data')


        data_page = 0
        try:
            dir_path = create_dir()
            answer_arr = []

            while(data_page < 20):
                answer = response_json[data_page].get('content')
                answer_tag = '<div>'+ answer + '</div>'
                praise_num = response_json[data_page].get('voteup_count')
                zhihu_name = response_json[data_page].get('author').get('name')
                item = get_each_answers(answer_tag, (data_page+1), praise_num,zhihu_name)
                answer_arr.append(item)

                data_page = data_page + 1

            question = response_json[0].get('question').get('title')
            save_str = question_url + '\n'.join(answer_arr)
            logging.info('问题：%s' % question)
            file_path = save_str_txt(save_str, os.path.join(dir_path, question + '_'+ str(offset) + '.txt'))
            logging.info('已保存为txt，路径：%s' % file_path)

        except Exception as e:
            logging.error('错误：%s' % e)

        offset = offset + 20







if __name__ == '__main__':
    # login_zhihu('18896917562', 'wodeZH66')

    from login_zhihu import isLogin, login

    if isLogin():
        logging.info('已登录【知乎】')

        # url = 'https://www.zhihu.com/question/20538364'
        # get_html(url)
        question_id = 30692237
        logging.info('【知乎】根据问题id：%s获取回答的json数据' % str(question_id))
        get_html_by_json(question_id)
        # dir_path = create_dir()
        # save_img_file('https://pic2.zhimg.com/50/v2-e96ad249b86046f785cd754f9fc33201_hd.jpg', dir_path)

    else:
        login('18896917562', 'wodeZH66')

