import glob,os
from mutagen import File
from 音乐识别.语音识别.MP3 import LRC歌词

"""
存在的问题：
    https://www.cnblogs.com/BigFeng/p/6212853.html
    .MP3后缀结尾的文件并不一定是MP3文件,也可能是wav文件(所以需要从“编码格式”判断文件类型)
"""
def isMp3Format(mp3filePath):
    """
    函数功能：检验是否为MP3文件
    MP3编码格式： TAG_V2(ID3V2)，音频数据，TAG_V1(ID3V1)
        ID3V1：在文件结尾的位置，以TAG开头，包含了作者，作曲，专辑等信息，长度为128Byte
        ID3V2：在文件开始的位置，以ID3开头，包含了作者，作曲，专辑等信息，长度不固定，扩展了ID3V1 的信息量
    :param mp3filePath: mp3路径
    :return:None
    """
    # 标签(1表示ID3V1;2表示ID3V2;3标签其他;-1表示不是MP3文件)
    flag = -1
    # 读取文件内字符串
    f = open(mp3filePath, 'rb')
    fileStr = f.read() # bytes类型
    f.close()
    head3Str = fileStr[:3]
    # 判断开头是不是ID3(ID3V2)
    if head3Str == b"ID3":
        flag = 2
        return True,flag
    # 判断结尾有没有TAG(ID3V1)
    last32Str = fileStr[-32:]
    # print("sss:",last32Str[:3])
    if last32Str[:3] == b"TAG":
        flag = 1
        return True,flag
    # 判断第一帧是不是FFF开头, 转成数字
    # fixme应该循环遍历每个帧头，这样才能100%判断是不是mp3
    ascii = ord(fileStr[:1])
    if ascii == 255:
        flag = 3
        return True,flag
    return False,flag

def listDirectory(directory, file_type):
    """
    获取指定后缀 文件列表
    :param directory:文件夹路径
    :param file_type:文件类型
    :return: FileList(文件列表)
    """
    mp3List = []
    notMp3List = []
    os.chdir(directory)
    fileList = glob.glob(file_type)
    for i in fileList:
        bools,flag = isMp3Format(directory+i)
        if bools == True:
            dict = {}
            if flag == 1:
                dict.update({'ID3V1': (directory + i)})
            elif flag == 2:
                dict.update({'ID3V2': (directory + i)})
            else:
                dict.update({'frame': (directory + i)})
            mp3List.append(dict)
        else:
            notMp3List.append(directory+i)
    return mp3List,notMp3List

def GetMp3Info(dict):
    """
    获取MP3标签信息(歌名、歌手、歌词等)
    :param mp3_path: MP3文件路径
    :return:dict字典
    """
    if 'ID3V1' in dict:   # 解析MP3格式为ID3V1
        # print("解析MP3格式为ID3V1")
        return getID3V1(dict.get('ID3V1'))
    elif 'ID3V2' in dict: # 解析MP3格式为ID3V2
        # print("解析MP3格式为ID3V2")
        return getID3V2(dict.get('ID3V2'))
    else:
        print("？？？解析MP3存在问题Frame：",mp3List[0])
    return None

def getID3V1(filename):
    fp = open(filename, 'r')
    fp.seek(-128, 2)
    try:
        header = fp.read(3)   # TAG iniziale
    except:
        print("header读取错误")
    try:
        title = fp.read(30)   # 歌名
    except:
        title = ''
    try:
        artist = fp.read(30)  # 歌手
    except:
        print("长度：",filename[:24])
        artist = ''
    lyrics = ''               # 歌词还未写????????????????????
    address = filename        # 音乐地址

    # album = fp.read(30)  # 专辑
    # year = fp.read(4)    # 年代
    # comment = fp.read(28)# 注释
    # reserve = fp.read(1) # 保留字段
    # track = fp.read(1)   # 歌曲在专辑中位置
    # genre = fp.read(1)   # 歌曲风格索引值
    fp.close()
    return {'title': title, 'artist': artist, 'lyrics':lyrics, 'address':address}

def getID3V2(filename):
    '''
    参数详情参考网址：http://blog.sina.com.cn/s/blog_6556038f01016n1v.html
    :param filename:文件路径
    :return:字典
    '''
    afile = File(filename)
    try:
        title = afile.tags["TIT2"].text[0]   # 歌名
    except:
        title = ''
    try:
        artist = afile.tags["TPE1"].text[0]  # 主唱(歌手)
    except:
        artist = ''
    try:
        lyrics = afile.tags["TOLY"].text[0]  # 原歌词
    except:
        LRC_path = (filename[:28] + 'LRC/' + filename[32:]).replace('.mp3','.lrc')
        lyrics = LRC歌词.read_lrc(LRC_path)
    address = filename                       # 音乐地址
    # genre = afile.tags['TCON'].text[0]   # 音乐类型索引值
    # album = afile.tags["TALB"].text[0]   # 专辑
    # year = afile.tags['TORY'].text[0]    # 发行年份
    return {'title':title,'artist':artist,'lyrics':lyrics, 'address':address}


if __name__ == "__main__":
    path = "D:/Python/data/未导入数据库的歌曲与歌词/MP3/"
    file_type = "*.mp3"
    mp3List,notMp3List = listDirectory(path,file_type)
    print("MP3列表:",mp3List)
    for i in mp3List:
        print(GetMp3Info(i))
