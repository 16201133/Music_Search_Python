import librosa
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

def Main(mp3filePath): # 提供接口————未提取特征的歌曲 全部 插入数据表song_feature中
    # 第一步、判断是否为真实的 MP3 文件
    bools, flag = isMp3Format(mp3filePath)
    if bools == True:
        # 第二步、将MP3转换成wav文件
        wave_path = "D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/原声识别/data/mp3_To_wave.wav"
        MP3_To_Wav(mp3filePath, wave_path)  # 将MP3转换成wav文件
        # 第三步、提取节奏特征
        y, sr = librosa.load(wave_path, sr=None)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_frames = librosa.feature.delta(beat_frames)  # mode='nearest'
        str_beat_frames = ','.join(str(x) for x in beat_frames)  # 通过json转换成字符串，用于写入SQL数据库
        result = str_beat_frames
    else:
        result = "该文件不是MP3文件"

    return result

if __name__ == "__main__":
    """
        读取一个MP3文件的节奏特征（原声识别）
    """
    # 获取MP3路径
    f = open("D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/path.txt", "r",encoding='UTF-8')
    mp3filePath = f.read() # MP3路径
    f.close()
    # 第一步、判断是否为真实的 MP3 文件
    bools, flag = isMp3Format(mp3filePath)
    if bools == True:
        # 第二步、将MP3转换成wav文件
        wave_path = "D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/原声识别/data/mp3_To_wave.wav"
        MP3_To_Wav(mp3filePath, wave_path)  # 将MP3转换成wav文件
        # 第三步、提取节奏特征
        y, sr = librosa.load(wave_path, sr=None)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_frames = librosa.feature.delta(beat_frames)  # mode='nearest'
        str_beat_frames = ','.join(str(x) for x in beat_frames)  # 通过json转换成字符串，用于写入SQL数据库
        print("节奏特征序列：", str_beat_frames)
    else:
        print("该文件不是MP3文件")