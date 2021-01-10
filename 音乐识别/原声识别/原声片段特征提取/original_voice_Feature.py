import wave
import pyaudio
import librosa
import numpy as np
from pydub import AudioSegment
from 音乐识别.语音识别.讯飞API import get_audio
from 音乐识别.旋律识别.哼唱特征提取 import 哼唱提取特征

def MP3_To_Wav(mp3_path,wav_path):
    """
    MP3转换成wav格式
    :param mp3_path: MP3文件路径
    :param wav_path: wav文件路径
    :return:None
    """
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format='wav')
    return None

def get_second_part_wav(main_wav_path,start_time,end_time,part_wav_path):
    """
    音频切片,获得部分音频 单位是秒
    :param main_wav_path: 主音频路径
    :param start_time: 截取开始时间
    :param end_time: 截取截止时间
    :param part_wav_path: 生成截取音频路径
    :return:None
    """
    start_time = int(start_time)*1000
    end_time = int(end_time) * 1000

    sound = AudioSegment.from_mp3(main_wav_path)
    word = sound[start_time:end_time]

    word.export(part_wav_path,format="wav")
    return None

def display_music(path):
    """
    音乐的播放
    :param path: 音乐文件路径
    :return:None
    """
    chunk = 1024
    wf = wave.open(path, 'rb')
    p = pyaudio.PyAudio()
    # 打开声音输出流
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    # 写声音输出流到声卡进行播放
    while True:
        data = wf.readframes(chunk)
        if data == "":
            break
        stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()  # 关闭PyAudio

    return None

def get_Original_Voice_Feature(filename):
    """
    原声识别 特征提取 (提取节奏特征)
    :param filename:文件路径
    :return: 节奏特征列表 feature_list
    """
    # 1、音频预处理(？？？存在噪音等？？？)

    # 2、原声片段特征提取（提取节奏特征）
    # 歌曲的切片操作（识别效果最佳）
    # filepath = "D:/Python/data/sings_data/原声片段.wav"
    y, sr = librosa.load(filename, sr=None)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_frames = librosa.feature.delta(beat_frames,mode='nearest')  # mode='nearest'

    return beat_frames

if __name__ == "__main__":
    '''
    mp3_path = "D:/Python/data/MP3_data/Beyond - 光辉岁月.mp3"
    wav_path = "D:/Python/PyCharm/workspace/Learning/旋律识别/data/mp3_to_wave.wav"
    # MP3 转换成 Wav 格式
    MP3_To_Wav(mp3_path, wav_path)
    # 音频切片
    start_time = 40
    end_time = 100
    wav_part_path = "D:/Python/data/sings_data/原声片段.wav"
    get_second_part_wav(wav_path, start_time, end_time, wav_part_path)
    # 播放wav音频
    display_music("D:/Python/data/sings_data/原声片段.wav")
    '''
    # 1、原声哼唱录制
    filepath = "D:/Python/PyCharm/workspace/Learning/原声识别/data/recording.wav"
    get_audio.get_audio(filepath,time=40)

    # 2、原声片段 特征提取（原声识别——提取节奏特征）
    list = get_Original_Voice_Feature(filepath)
    print("节奏特征列表：",list)