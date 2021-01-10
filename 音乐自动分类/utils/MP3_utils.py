import glob,os
from pydub import AudioSegment

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

def get_MP3_ID3_Type(dict):
    if 'ID3V1' in dict:
        return 'ID3V1'
    elif 'ID3V2' in dict:
        return 'ID3V2'
    return "!!!非ID3V1或ID3V2!!!"

def MP3_To_Wav(mp3_path,wav_path):
    """
    MP3转换成wav格式
    :param mp3_path: MP3文件路径
    :param wav_path: wav文件路径
    :return: None
    """
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format='wav')
    return None