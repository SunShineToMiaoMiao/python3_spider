import logging; logging.basicConfig(level=logging.INFO)
import datetime, time
import os
import json
from urllib import request


# ################### 创建目录 ####################
# 默认文件存储的根目录为模块文件夹下的doc文件夹
def create_dir():
    time_dir = datetime.datetime.now().strftime('%Y%m%d%H%M')

    # 判断doc文件夹是否存在
    if not os.path.exists('doc'):
        os.mkdir('doc')

    path = os.path.join('doc', time_dir)

    # 新建抓取内容时保存的文件夹
    if os.path.exists(path):
        # os.remove(path)
        return path
    else:
        os.mkdir(path)
        return path


# ################### 写入txt--str格式 ###################
def save_str_txt(data, file_path):
    with open(file_path, 'w+', encoding='utf-8') as fp:
        fp.write(data)
    logging.info('【str格式的txt文件】保存成功，路径：%s' % file_path)


# ################### 写入txt--JSON格式 ###################
def save_json_txt(list_name, file_path):
    # 一定要加上ensure_ascii=False, 才能保存为汉字
    data = json.dumps(list_name, ensure_ascii=False)
    with open(file_path, 'w+', encoding='utf-8') as fp:
        fp.write(data)
    logging.info('【JSON格式的txt文件】保存成功，路径：%s' % file_path)


# ####################### 根据url下载图片 ############################
def download_img(url, dir_path):
    # 图片路径
    abs_path = os.path.abspath('.')
    mir_s = str(datetime.datetime.now().microsecond)
    f_str = str(time.strftime('%H_%M_%S', time.localtime()) + '__' + mir_s + '.png')
    file_path = os.path.join(os.path.join(abs_path, dir_path), f_str)

    # 下载文件
    con = request.urlretrieve(url, file_path)
    logging.info('【png图片】保存成功，绝对路径：%s' % con[0])
    return con[0]


if __name__ == '__main__':
    # request_img('http://upload-images.jianshu.io/upload_images/2917634-7667382cc63b833d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/700')
    dir_path = create_dir()
    f = download_img('http://upload-images.jianshu.io/upload_images/2917634-7667382cc63b833d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/700',dir_path)
    print(f)
