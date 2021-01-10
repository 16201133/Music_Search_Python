import os,sys
sys.path.append("D:/Python/PyCharm/workspace/智能音乐搜索")

from 音乐识别.语音识别.讯飞API import get_audio
from 音乐识别.旋律识别.哼唱特征提取 import 哼唱提取特征
from 音乐识别.旋律识别.旋律特征匹配算法 import 旋律匹配
import 音乐识别.旋律识别.MP3旋律特征.MP3_Feature as MP3_Feature

if __name__ == "__main__":
    # 第一步：构建MP3旋律特征数据库
    # 执行MP3旋律特征

    # 将HTML5录制的MP3音频转化成wav
    mp3Path = "D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/旋律识别/data/recording.mp3"
    wavPath = "D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/旋律识别/data/mp3_to_wave.wav"
    MP3_Feature.MP3_To_Wav(mp3Path,wavPath)
    filepath = wavPath

    # 第二步：用户哼唱输入,并进行预处理提取特征
    # 1、哼唱录制音频(保存到recording.wav)
    # filepath = "D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/旋律识别/data/recording.wav"
    # get_audio.get_audio(filepath,time=30)

    # 2、哼唱旋律特征提取
    # filepath = "D:/Python/data/sings_data/一次就好16k.wav"   # 哼唱录制的文件路径(一次就好16k.wav)
    # filepath = "D:/Python/data/sings_data/棉子-勇气原唱.wav"  # 哼唱录制的文件路径(？？？匹配度最高？？？)
    pitch_list = 哼唱提取特征.get_features(filepath)   # 获取音高特征 (待修改完善？？？)
    str1 = 哼唱提取特征.list_To_Str(pitch_list)        # 音高特征 转换成 相对音高轮廓(U、S、D字符串表示)

    # 第三步：旋律特征匹配
    list = 旋律匹配.Search_Match(str1, top_num=5) # 保留相似度前2位的歌曲
    print("旋律识别结果：", list)
    # for i in list:
    #     print("匹配度:{}，歌曲地址:{}".format(i['song_rate'], i['song_address']))
