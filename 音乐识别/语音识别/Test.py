import librosa

wavPath = "D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/语音识别/讯飞API/data/recording.mp3" # 光辉岁月
wavPath1 = "D:/Python/PyCharm/workspace/智能音乐搜索/音乐识别/语音识别/讯飞API/data/recording.wav" # 一次就好

y,sr = librosa.load(wavPath,sr=None)
print("光辉岁月：")
print(y,";",sr)

y1,sr1 = librosa.load(wavPath1,sr=None)
print("一次就好：")
print(y1,";",sr1)
