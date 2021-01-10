import os,sys
sys.path.append("D:/Python/PyCharm/workspace/智能音乐搜索")

import shutil
import numpy as np
import 音乐识别.旋律识别.哼唱特征提取.哼唱提取特征

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

def Main(mp3filePath): # 提供接口————未提取特征的歌曲 全部 插入数据表song_feature中
    spleeter_path = "D:/Python/spleeter/audio_example.mp3"  # 用于歌声分离
    # 第一步、判断是否为真实的 MP3 文件
    bools, flag = isMp3Format(mp3filePath)
    # 第二步、歌声分离后，再获取音高特征序列
    if bools == True:
        shutil.copyfile(mp3filePath, spleeter_path)  # 将MP3复制到歌声分离工具Spleeter中（由于工具Spleeter中，MP3不能包含中文和空格等非法字符）
        # 对MP3音乐 进行歌声分离，得到 伴奏wav 和 歌声wav 两个文件
        # 再获取MP3音乐文件的音高特征
        pitch_list = music_features(mp3filePath)
        # 转换成“相对音高轮廓”
        str = list_To_Str(pitch_list)
        result = str
    else:
        result = "该文件不是MP3文件"
    return result

if __name__ == "__main__":
    """
      读取一个MP3文件的旋律特征
    """
    # 获取MP3路径
    f = open("D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/path.txt", "r", encoding='UTF-8')
    mp3filePath = f.read()  # MP3路径
    f.close()
    spleeter_path = "D:/Python/spleeter/audio_example.mp3"                 # 用于歌声分离
    # 第一步、判断是否为真实的 MP3 文件
    bools, flag = isMp3Format(mp3filePath)
    # 第二步、歌声分离后，再获取音高特征序列
    if bools == True:
        shutil.copyfile(mp3filePath, spleeter_path)  # 将MP3复制到歌声分离工具Spleeter中（由于工具Spleeter中，MP3不能包含中文和空格等非法字符）
        # 对MP3音乐 进行歌声分离，得到 伴奏wav 和 歌声wav 两个文件
        # 再获取MP3音乐文件的音高特征
        pitch_list = music_features(mp3filePath)
        # 转换成“相对音高轮廓”
        str = list_To_Str(pitch_list)
        print("音高特征序列：",str)
    else:
        print("该文件不是MP3文件")