import logging; logging.basicConfig(level=logging.INFO)

import urllib
# import urllib.parse
# import urllib.request
from urllib import request, parse
from urllib.error import URLError, HTTPError

import socket
import http.client
import random
import time
import re


# ################### 构造 Request headers ####################################
# User-Agent : 有些服务器或 Proxy 会通过该值来判断是否是浏览器发出的请求
# Content-Type : 在使用 REST 接口时，服务器会检查该值，用来确定 HTTP Body 中的内容该怎样解析。
# application/xml ： 在 XML RPC，如 RESTful/SOAP 调用时使用
# application/json ： 在 JSON RPC 调用时使用
# application/x-www-form-urlencoded ： 浏览器提交 Web 表单时使用
# 在使用服务器提供的 RESTful 或 SOAP 服务时， Content-Type 设置错误会导致服务器拒绝服务

# 如果在request header包含”Accept-Encoding”:”gzip, deflate”,
# 并且web服务器端支持，返回的数据是经过压缩的，这个好处是减少了网络流量，由客户端根据header，在客户端层解压，再解码。
# 获取的http response数据是原始数据，没有经过解压，所以这是乱码的根本原因。

HEADERS = {
    # "Host": "www.zhihu.com",
    # "Referer": "https://www.zhihu.com/",
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 加上后，会导致乱码
    # 'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'

    # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'X-Requested-With': 'XMLHttpRequest',
}

# ################### 设置超时 timeout ###################
# timeout是设定的一个超时时间，取随机数是因为防止被网站认定为网络爬虫。
# TIMEOUT = random.choice(range(80, 180))
TIMEOUT = random.choice(range(0, 5))


# ################### 使用urllib库访问url ###################
def request_html_by_urllib(url, self_headers=None, **kwargs):

    req_url = url
    req_headers = HEADERS

    # 有其他的headers，如host
    if self_headers:
        req_headers = dict(HEADERS, **self_headers)

    # 若用于请求的数据不为空，如含有“搜索用关键词”
    if kwargs:
        req_data = parse.urlencode(kwargs)
        req_url = '%s?%s' % (url, req_data)
        # req_url = parse.quote(req_url, safe='/:?=')

    # 构造请求
    req = request.Request(req_url, headers=req_headers)

    logging.info('访问链接url：%s' % req.full_url)
    logging.info('请求类型：%s' % req.type)
    logging.info('主机名：%s' % req.host)
    logging.info('路径：%s' % req.selector)

    while True:
        try:
            response_rs = request.urlopen(req)
            # response_html = response_rs.decode('utf-8')
            response_html = response_rs.read().decode('utf-8')
            break

        except socket.timeout as e:
            logging.error('***请求超时：%s***' % e)
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            logging.error('***socket错误：%s***' % e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            logging.error('***http.client.BadStatusLine错误：%s***' % e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            logging.error('***http.client.IncompleteRead错误：%s***' % e)
            time.sleep(random.choice(range(5, 15)))

        except HTTPError as e:
            # print('The server couldn\'t fulfill the request.')
            logging.error('***服务器未能完成请求***')
            logging.error('***错误码Error code: %s***' % e.code)

        except URLError as e:
            if hasattr(e, 'reason'):
                logging.error('***未链接到服务器***')
                logging.error('***原因: %s***' % e.reason)
            elif hasattr(e, 'code'):
                logging.error('***错误码Error code: %s***' % e.code)

    return response_html


# ####################### 处理提交数据中的中文字符 ############################
# def deal_request_data(**kwargs):
#     pattern = re.compile(u'[\u4e00-\u9fa5]+')
#     for k in kwargs:
#         if isinstance(kwargs[k],str):
#             has_chinese = pattern.search(kwargs[k])
#             if has_chinese:
#                 parse.quote(kwargs[k])
#
#     req_data = parse.urlencode(kwargs)
#     return req_data


