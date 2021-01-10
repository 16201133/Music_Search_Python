import librosa
import numpy as np
import os
import pandas as pd
from 音乐自动分类.utils import MP3_utils

def Feature_data():
    """
    获取genres数据集，转换成csv格式
    :return: heads 头标签；data_set 特征值数据；label_set 目标值数据
    """
    # 蓝调blues、古典classical、国家country、迪斯科disco、嘻哈hiphop、爵士乐jazz、金属metal、流行的pop、雷鬼reggae、rock
    genres = 'blues classical country disco hiphop jazz metal pop reggae rock'.split()  # 音乐流派类型

    data_set = []   # 特征值
    label_set = []  # 目标值

    label2id = {genre: i for i, genre in enumerate(genres)}

    heads = ['chroma_stft','rmse','spec_cent','spec_bw',
             'rolloff','zcr','mfcc1','mfcc2',
             'mfcc3','mfcc4','mfcc5','mfcc6',
             'mfcc7','mfcc8','mfcc9','mfcc10',
             'mfcc11','mfcc12','mfcc13','mfcc14',
             'mfcc15','mfcc16','mfcc17','mfcc18',
             'mfcc19','mfcc20','type'] # 26个特征值 + 1个目标值
    for g in genres:
        print("{}流派的歌曲正在提取特征...".format(g))
        for filename in os.listdir(f'D:/Python/data/music_data_set/genres/{g}/'): # 对其中每种流派每一首歌进行 特征提取
            songname = f'D:/Python/data/music_data_set/genres/{g}/{filename}'
            y, sr = librosa.load(songname, mono=True, duration=30)
            # 提取各种特征(共26个特征)
            chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
            rmse = librosa.feature.rms(y=y)
            spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
            spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
            rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
            zcr = librosa.feature.zero_crossing_rate(y)
            mfcc = librosa.feature.mfcc(y=y, sr=sr)

            # 求特征的平均值
            to_append = f'{np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'

            for e in mfcc:
                to_append += f' {np.mean(e)}'

            to_append += f' {label2id[g]}' # 在末尾添加 目标值

            data_set.append([float(i) for i in to_append.split(" ")]) # 特征值
            label_set.append(label2id[g]) # 目标值

    return heads,data_set,label_set

def MP3_data(path,filetype):
    """
    将 MP3原始数据 批量转化成 数字矩阵（用于测试）
    :return: None
    """
    data_set = []  # 特征值
    heads = ['name','chroma_stft', 'rmse', 'spec_cent', 'spec_bw',
             'rolloff', 'zcr', 'mfcc1', 'mfcc2',
             'mfcc3', 'mfcc4', 'mfcc5', 'mfcc6',
             'mfcc7', 'mfcc8', 'mfcc9', 'mfcc10',
             'mfcc11', 'mfcc12', 'mfcc13', 'mfcc14',
             'mfcc15', 'mfcc16', 'mfcc17', 'mfcc18',
             'mfcc19', 'mfcc20']         # 1个歌曲名称 + 26个特征值
    # 1、获取MP3列表
    mp3List, notMp3List = MP3_utils.listDirectory(path,filetype)
    # 2、遍历列表，转化成wav，再提取特征mp3_to_wave.wav

    for i in mp3List:
        ID3_Type = MP3_utils.get_MP3_ID3_Type(i)  # 获取MP3属于ID3的哪种类型
        mp3_path = i.get(ID3_Type)  # 获得mp3的路径
        wav_path = "D:/Python/PyCharm/workspace/Learning/音乐自动分类/data/mp3_to_wav.wav"
        MP3_utils.MP3_To_Wav(mp3_path,wav_path) # 将MP3转换成wav文件

        y, sr = librosa.load(wav_path, mono=True, duration=30)
        # 提取各种特征(共26个特征)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr) # 色度频率
        rmse = librosa.feature.rms(y=y) # 短时能量
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr) # 频谱质心
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr) # 谱带宽
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr) # 频谱滚降点（光谱衰落）
        zcr = librosa.feature.zero_crossing_rate(y) # 过零率： 这个特征已在语音识别和音乐信息检索领域得到广泛使用，是金属声音和摇滚乐的关键特征。
        mfcc = librosa.feature.mfcc(y=y, sr=sr) # 梅尔频率倒谱系数

        # name = f'{mp3_path[24:]} '
        name = [mp3_path[24:]]
        # 求特征的平均值
        to_append = f'{np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'

        for e in mfcc:
            to_append += f' {np.mean(e)}'

        to_append = [float(i) for i in to_append.split(" ")]
        to_append = name + to_append
        data_set.append(to_append)  # 特征值

    return heads,data_set

def write_into_csv(filepath,heads,data_set):
    """
    写入数据 到 GTZAN_data.csv
    :param filepath: 文件路径
    :param heads: 标签
    :param data_set: 特征数据
    :return: None
    """
    GTZAN = pd.DataFrame(columns=heads,data=data_set)
    GTZAN.to_csv(filepath)
    return None

if __name__ == "__main__":
    # 1、写入数据 到 GTZAN_data.csv
    # path = 'D:/Python/PyCharm/workspace/Learning/音乐自动分类/data/GTZAN_data.csv'
    # heads, data_set, label_set = Feature_data()
    # write_into_csv(path,heads,data_set)

    # 2、提取MP3特征，并写入predict_data.csv
    # MP3_path = "D:/Python/data/MP3_data/"
    # file_type = "*.mp3"
    # mp3_heads,mp3_data_set = MP3_data(MP3_path,file_type)
    # predict_path = "D:/Python/PyCharm/workspace/Learning/音乐自动分类/data/predict_data.csv"
    # write_into_csv(predict_path, mp3_heads, mp3_data_set)

    # 3、读取GTZAN_data.csv数据
    # path = 'D:/Python/PyCharm/workspace/Learning/音乐自动分类/data/GTZAN_data.csv'
    # data = pd.read_csv(path, index_col = [0])
    # print(data)

    # 4、读取predict_data.csv数据
    predict_path = "D:/Python/PyCharm/workspace/Learning/音乐自动分类/data/predict_data.csv"
    data = pd.read_csv(predict_path, index_col = [0])
    print(data)
