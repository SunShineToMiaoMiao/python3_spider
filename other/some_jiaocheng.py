import urllib
import urllib.request, urllib.parse
# import urllib2

'''python 3.x中urllib库和urilib2库合并成了urllib库。

其中urllib2.urlopen()变成了urllib.request.urlopen()

urllib2.Request()变成了urllib.request.Request()'''



def get_html_by_request():
    url = 'http://zzk.cnblogs.com/s/blogpost'
    search_str = 'python 爬虫'
    # data = dict(search_str)

    # data = urllib.parse.urlencode(values)
    # req = urllib.request.Request(url, data)

    data = {'Keywords':search_str}
    data_req = urllib.parse.urlencode(data)
    request = urllib.request.Request(url, data_req)
    response = urllib.request.urlopen(request)
    response_rs = response.read()
    # api = '%s?%s' % (url, urllib.parse.urlencode(data))
    # request = urllib.request.Request(api)
    # response_rs = urllib.request.urlopen(request).read()

    print('完整url：%s' % request.full_url)
    print('请求类型：%s' % request.type)
    print('主机名：%s' % request.host)
    print('路径：%s' % request.selector)
    print(response_rs)

    # 设置代理
    proxy_support = urllib.request.ProxyHandler({'sock5': 'localhost:1080'})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)

    a = urllib.request.urlopen("http://www.jb51.net").read()
    print(a)


if __name__ == '__main__':
    get_html_by_request()