import requests
import time
import json


def main():
    s = requests.Session()
    data = {
        "redirect": '/',
        "account": 'username',
        "password": 'passwd',
        "remember": 'true',
    }
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json, text/javascript, */*; q=0.01'
    }
    s.post('http://www.kanzhun.com/login.json', headers=headers, data=data)

    res = s.get('http://www.kanzhun.com/gsx3195.html?ka=com-blocker1-salary', headers=headers)
    print(res.text)
    time.sleep(1)

if __name__ == '__main__':
    main()

# 作者：yuanquan521
# 链接：http://www.jianshu.com/p/936848e348e3
# 來源：简书
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。