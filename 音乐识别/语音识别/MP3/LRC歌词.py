import os,sys
sys.path.append("D:/Python/PyCharm/workspace/智能音乐搜索")

import chardet

def detectCode(path):
    '''查看文件编码格式'''
    with open(path, 'rb') as file:
        data = file.read()
        dicts = chardet.detect(data)
    return dicts["encoding"]

def read_lrc(filepath):
    """
    解析LCR歌词文件
    :param filepath: LCR文件路径
    :return: 歌词信息
    """
    lyrics = '' # 歌词信息
    if not os.path.exists(filepath):
        print("文件不存在：",filepath)
        return lyrics
    # 创建字典,存放歌词和时间,key表示时间,value表示歌词
    lrc_dict = {}
    # 打开文件
    # 第二个参数为:'rb' 以二进制格式打开一个文件用于只读。这就避免了指定了encoding与文件实际编码不匹配而报错的问题
    with open(filepath, "r", encoding="{0}".format(detectCode(filepath))) as file:
        # 读取文件全部内容
        lrc_list = file.readlines()
        # 遍历所有元素,干掉方括号
        for i in lrc_list:
            # 取出方括号并切割歌词字符串
            lrc_word = i.replace("[", "]").strip().split("]")
            # 得到的结果: lrc_word = ['', '01:40.00', '', '00:16.00', '今天我寒夜里看雪飘过']
            for j in range(len(lrc_word) - 1):
                if lrc_word[j]:
                    lrc_dict[lrc_word[j]] = lrc_word[-1]
        # 遍历字典,对字典的key进行排序,
        for key in sorted(lrc_dict.keys()):
            # print(key, lrc_dict[key])
            # 筛选出歌词部分
            if len(key)>=8 and key[2]==':' and key[5]=='.': # 满足 xx:xx.xxx|xx:xx.xxx 格式
                # 筛选出歌词部分
                if ('：' not in lrc_dict[key]) and (':' not in lrc_dict[key]) and ('-' not in lrc_dict[key]) and ('/' not in lrc_dict[key]) and (''!=lrc_dict[key]):
                    lyrics += lrc_dict[key] + ','
    # 去除空格
    # lyrics = lyrics.replace(' ','')
    return lyrics

if __name__ == "__main__":
    # 歌词下载网站：http://www.9ku.com/geci/667937.htm
    f = open("D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/lrcPath.txt", "r", encoding='UTF-8')
    lrcPath = f.read()  # MP3路径
    f.close()
    lyrics = read_lrc(lrcPath)
    print("歌词：",lyrics)