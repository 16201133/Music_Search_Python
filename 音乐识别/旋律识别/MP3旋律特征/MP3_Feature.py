import shutil
import glob,os
import numpy as np
import 音乐识别.旋律识别.哼唱特征提取.哼唱提取特征
from pydub import AudioSegment
from 音乐识别.语音识别.数据库 import MySQLUtil

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

def music_features(mp3_path):
    """
    提取 wav音乐文件的 特征
    :param filepath: wav音乐文件的路径
    :return: 音高特征序列 pitch_list
    """
    # 1、歌声、伴奏分离
    # 执行歌声分离(结果返回到路径 D:/Python/spleeter/output/audio_example 中)
    print("{} 正在执行歌声分离...".format(mp3_path))
    os.system("cd /d D:/Python/spleeter&python -m spleeter separate -p spleeter:2stems -o output -i D:/Python/spleeter/audio_example.mp3")
    # 2、提取基音周期(歌声)
    pitch_list = []  # 音高特征序列
    try:
        music_singer = "D:/Python/spleeter/output/audio_example/vocals.wav"     # 分离出来的 歌声路径
        pitch_list = 音乐识别.旋律识别.哼唱特征提取.哼唱提取特征.get_features(music_singer)  # 提取音高特征值
    except: # 没有找到 vocals.wav 返回结果时
        os.system("cd /d D:/Python/spleeter&python -m spleeter separate -p spleeter:2stems -o output -i D:/Python/spleeter/audio_example.mp3")

    return pitch_list

def list_To_Str(list):
    """
    将 音高特征 转换成 相对音高特征 作为旋律表示
    :param list:一维数组(float类型)
    :return: str 相对音高轮廓(U、S、D字符串表示)
    """
    str = ""
    for i in np.arange(len(list)-1):
        compare = list[i+1]-list[i]
        if compare>0:
            str += "U"
        elif compare < 0:
            str += "D"
        else:
            str += "S"
    return str

if __name__ == "__main__":
    # 读取一个文件夹下“所有MP3文件”的旋律特征，并插入数据库中
    path = "D:/Python/data/MP3_data/"
    file_type = "*.mp3"
    mp3List, notMp3List = listDirectory(path, file_type) # 获得MP3列表
    list_tuple = [] # 数据格式为 列表-元组 [(),()]
    for i in mp3List:
        ID3_Type = get_MP3_ID3_Type(i) # 获取MP3属于ID3的哪种类型
        mp3_path = i.get(ID3_Type) # 获得mp3的路径
        spleeter_path = "D:/Python/spleeter/audio_example.mp3"
        shutil.copyfile(mp3_path, spleeter_path)  # 将MP3复制到歌声分离工具Spleeter中（由于工具Spleeter中，MP3不能包含中文和空格等非法字符）
        # 对MP3音乐 进行歌声分离，得到 伴奏wav 和 歌声wav 两个文件
        # 获取MP3音乐文件的音高特征
        pitch_list = music_features(mp3_path)
        # 转换成“相对音高轮廓”
        str = list_To_Str(pitch_list)
        # 将音高特征存入“列表-元组”当中
        tuple = (str,mp3_path)
        list_tuple.append(tuple)
    # print("待插入的音高轮廓：",list_tuple)
    # 将 “列表-元组”格式的音高轮廓特征 插入数据库
    sql = "insert into melody (song_melody,song_address) values (%s,%s)"
    data = MySQLUtil.read_config() # 读取数据库配置信息
    db = MySQLUtil.DBUtil(data)    # 创建对象
    db.insert_melody_many(sql=sql,list_tuple=list_tuple)