import time
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="\n\n%(asctime)s----- @Path: %(pathname)s, @File: %(filename)s, @Func: %(funcName)s[line:%(lineno)d] \n***%(levelname)s***: %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='apple' + str(time.strftime('%Y%m%d_%H%M%S', time.localtime())) + '.log',  # 指定日志文件名
                    # filename='apple.log',
                    filemode='w')  # 和file函数意义相同，指定日志文件的打开模式，'w'或'a'
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# 日志回滚
import logging
from logging.handlers import RotatingFileHandler
Rthandler = RotatingFileHandler('apple.log',maxBytes=1024*1024*10,backupCount=5)
Rthandler.setLevel(logging.ERROR)
rt_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)