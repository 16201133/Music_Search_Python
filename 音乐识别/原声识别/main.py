import os,sys
sys.path.append("D:/Python/PyCharm/workspace/智能音乐搜索")

from 音乐识别.语音识别.讯飞API import get_audio
from 音乐识别.原声识别.原声片段特征提取 import original_voice_Feature
from 音乐识别.原声识别.匹配算法 import 原声匹配
import 音乐识别.旋律识别.MP3旋律特征.MP3_Feature as MP3_Feature

if __name__ == "__main__":
    # 第一步：构建MP3原声特征库
    # 执行 MP3_original_voice_Feature.py 文件
    # 第二步：提取原声片段特征
    # 1、原声片段录音（原声识别）
    # filepath = "D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/原声识别/data/recording.wav" # 原声录制（有杂音）
    # filepath = "D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/原声识别/data/原声片段.wav"  # 原声片段
    # get_audio.get_audio(filepath, time=20) # 录音

    # 1、将HTML5录制的MP3音频转化成wav
    mp3Path = "D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/原声识别/data/recording.mp3"
    wavPath = "D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/原声识别/data/mp3_To_wave.wav"
    MP3_Feature.MP3_To_Wav(mp3Path, wavPath)
    filepath = wavPath

    # 2、特征提取
    list = original_voice_Feature.get_Original_Voice_Feature(filepath)

    # 第三步：匹配算法
    results = 原声匹配.Search_Match(list, top_num=5)  # 返回前5名
    print("原声识别结果：",results)
    # 打印输出结果
    # for i in results:
    #     print("id:{}，匹配度:{}，歌曲地址:{}".format(i['song_id'],i['song_rate'], i['song_address']))