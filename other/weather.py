import requests
import csv
import xlrd, xlwt
import random
import time
import socket
import http.client
# import urllib.request
from bs4 import BeautifulSoup


# 参考文章
# http://blog.csdn.net/Bo_wen_/article/details/50868339
# https://www.cnblogs.com/zhoujie/p/python18.html

def get_content(url):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }

    # timeout是设定的一个超时时间，取随机数是因为防止被网站认定为网络爬虫。
    timeout = random.choice(range(80,180))
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text


def get_data(html):
    soup = BeautifulSoup(html,'html.parser')
    ul_tag = soup.find('ul',class_='t clearfix')
    li_tags = ul_tag.find_all('li')

    weathers_arr = []

    for t in li_tags:
        weather_arr = []
        # 日期
        weather_arr.append(t.find('h1').text)
        # 天气状况
        weather_arr.append(t.find('p', class_='wea').text)
        # 最高温
        temperature_p = t.find('p', class_='tem')
        hightest = temperature_p.find('span')
        if hightest:
            temperature_highest = hightest.text  # 找到最高温
            temperature_highest = temperature_highest.replace('℃', '')  # 到了晚上网站会变，最高温度后面也有个℃
        weather_arr.append(temperature_highest)
        # 最低温
        temperature_lowest = temperature_p.find('i').text  # 找到最低温
        temperature_lowest = temperature_lowest.replace('℃', '')  # 最低温度后面有个℃，去掉这个符号
        weather_arr.append(temperature_lowest)

        weathers_arr.append(weather_arr)

    return weathers_arr


def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)


def set_style(name,height,bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6

    style.font = font
    # style.borders = borders

    return style


def write_excel(data, name):
    # 创建工作簿
    excel = xlwt.Workbook()
    # 创建表
    sheet1 = excel.add_sheet('天气预报',cell_overwrite_ok=True)
    # 第一行描述
    row0 = ['地区', '日期', '天气状况', '最高温', '最低温']
    # 第一列描述
    column0 = ['苏州', '徐州', '淮安']
    # 七日
    date = ['7日（今天）', '8日（明天）', '9日（后天）', '10日（周日）', '11日（周一）', '12日（周二）', '13日（周三）']

    # 生成第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman',220,True))

    # 生成第一列
    i, j = 1, 0
    while i < 7 * len(column0) and j < len(column0):
        sheet1.write_merge(i, i + 3, 0, 0, column0[j], set_style('Arial', 220, True))  # 第一列
        # sheet1.write_merge(i, i + 3, 7, 7)  # 最后一列"合计"
        i += 7
        j += 1

    # sheet1.write_merge(21, 21, 0, 1, u'合计', set_style('Times New Roman', 220, True))

    # 生成第二列
    i = 0
    while i < 7 * len(column0):
        for j in range(0, len(date)):
            sheet1.write(j + i + 1, 1, date[j])
            i += 7

    excel.save(name)  # 保存文件

if __name__ == '__main__':
    url = 'http://www.weather.com.cn/weather/101190401.shtml'
    html = get_content(url)
    result = get_data(html)
    # write_data(result, 'weather.csv')
    write_excel(result, 'weather.xlsx')